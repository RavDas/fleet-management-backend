# Horizontal Pod Autoscaling (HPA) Setup Guide

## Overview
This guide enables automatic horizontal scaling for your Fleet Management microservices based on CPU and memory utilization. Your 3-node cluster (1 control + 2 workers) will automatically scale pods up/down to handle varying loads.

---

## Architecture

```
┌─────────────────────────────────────────┐
│   Kubernetes Metrics Server             │
│   (Collects resource metrics)           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│   HPA Controllers                       │
│   ├─ vehicle-service-hpa                │
│   ├─ maintenance-service-hpa            │
│   └─ driver-service-hpa                 │
└────────────────┬────────────────────────┘
                 │
                 ▼
       ┌─────────┴──────────┬─────────────┐
       ▼                    ▼             ▼
   Vehicle             Maintenance    Driver
   Service             Service        Service
  (2-5 pods)          (2-4 pods)     (2-6 pods)
   
   Distributed across 2 Worker Nodes
```

---

## Prerequisites

### 1. Verify Metrics Server is Installed
Metrics Server collects CPU/memory data from nodes. Most managed clusters have it pre-installed.

```bash
# Check if metrics-server is running
kubectl get deployment metrics-server -n kube-system

# If not found, install it
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Wait for it to start (30-60 seconds)
kubectl wait --for=condition=ready pod -l k8s-app=metrics-server -n kube-system --timeout=60s
```

### 2. Verify Resource Requests Are Set
HPA requires resource requests to calculate CPU/memory percentages.

```bash
# Check if deployments have resource requests
kubectl get deployment vehicle-service -o yaml | grep -A 5 "resources:"

# Expected output:
# resources:
#   requests:
#     cpu: 250m
#     memory: 256Mi
```

If resources are missing, apply the updated deployments:
```bash
kubectl apply -f infrastructure/ansible/k8s/vehicle-service-deployment.yaml
kubectl apply -f infrastructure/ansible/k8s/maintenance-service-deployment.yaml
kubectl apply -f infrastructure/ansible/k8s/driver-service-deployment.yaml
```

---

## HPA Configuration Overview

| Service | Min Pods | Max Pods | CPU Threshold | Memory Threshold | Scale-Up Speed |
|---------|----------|----------|---------------|------------------|----------------|
| **Vehicle** | 2 | 5 | 70% | 80% | Fast (100% every 15s) |
| **Maintenance** | 2 | 4 | 75% | 80% | Fast (100% every 15s) |
| **Driver** | 2 | 6 | 70% | 80% | Fast (100% every 15s) |

**Scale-Down Policy:** Conservative (50% every 300s = 5 mins) to avoid rapid cycling

---

## Deployment Steps

### Step 1: Apply Updated Deployments (with resource requests)
```bash
kubectl apply -f infrastructure/ansible/k8s/vehicle-service-deployment.yaml
kubectl apply -f infrastructure/ansible/k8s/maintenance-service-deployment.yaml
kubectl apply -f infrastructure/ansible/k8s/driver-service-deployment.yaml

# Verify pods restarted with new resource specs
kubectl get pods -l app=vehicle-service,app=maintenance-service,app=driver-service
```

### Step 2: Deploy HPA Resources
```bash
# Create HPA for all services
kubectl apply -f infrastructure/ansible/k8s/hpa/vehicle-service-hpa.yaml
kubectl apply -f infrastructure/ansible/k8s/hpa/maintenance-service-hpa.yaml
kubectl apply -f infrastructure/ansible/k8s/hpa/driver-service-hpa.yaml

# Verify HPA resources created
kubectl get hpa
```

Expected output:
```
NAME                        REFERENCE                      TARGETS                      MINPODS   MAXPODS   REPLICAS   AGE
vehicle-service-hpa         Deployment/vehicle-service     <unknown>/70%, <unknown>/80% 2         5         2          10s
maintenance-service-hpa     Deployment/maintenance-service <unknown>/70%, <unknown>/80% 2         4         2          10s
driver-service-hpa          Deployment/driver-service      <unknown>/70%, <unknown>/80% 2         6         2          10s
```

### Step 3: Wait for Metrics to Become Available
```bash
# Wait 1-2 minutes for metrics-server to collect data
sleep 120

# Check HPA status again
kubectl get hpa
# TARGETS should now show actual percentages like "10%/70%, 15%/80%"
```

---

## Monitoring & Verification

### 1. Check HPA Status
```bash
# Watch HPA in real-time
kubectl get hpa -w

# Detailed HPA status
kubectl describe hpa vehicle-service-hpa

# Example output:
# Metrics:
#   resource cpu on pods  (avg: 5%/70%):
#   resource memory on pods  (avg: 20%/80%):
# Min replicas: 2
# Max replicas: 5
# Deployment pods: 2 current / 2 desired
```

### 2. Monitor Pod Scaling
```bash
# Watch pods scale in real-time
kubectl get pods -l app=vehicle-service -w

# Get replica counts
kubectl get deployment vehicle-service -o wide
```

### 3. Check Node Resource Availability
```bash
# View node resource utilization
kubectl top nodes

# View individual pod resource usage
kubectl top pods -l app=vehicle-service
kubectl top pods -l app=maintenance-service
kubectl top pods -l app=driver-service
```

### 4. View HPA Events
```bash
# See scaling events
kubectl get events --field-selector involvedObject.kind=HorizontalPodAutoscaler

# Detailed events for a specific HPA
kubectl describe hpa vehicle-service-hpa | grep -A 20 "Events:"
```

---

## Load Testing (Optional)

### Generate Load to Trigger Scaling

**Option 1: Using Apache Bench**
```bash
# Get the service endpoint
INGRESS_IP=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Generate load against vehicle service (10,000 requests, 100 concurrent)
ab -n 10000 -c 100 http://${INGRESS_IP}/vehicle/health

# Watch scaling happen
kubectl get hpa -w
kubectl get pods -l app=vehicle-service -w
```

**Option 2: Using a Load Pod**
```bash
# Create a busybox pod and run a load loop
kubectl run load-test --image=busybox --restart=Never -- \
  sh -c "while true; do wget -O - http://vehicle-service/health; done"

# Watch scaling
kubectl get hpa vehicle-service-hpa -w

# Stop the test
kubectl delete pod load-test
```

---

## Scaling Behavior Explained

### Scale-Up Behavior
- **Trigger:** CPU > 70% OR Memory > 80%
- **Speed:** Immediately doubles pods (100%) every 15 seconds
- **Example:** 2 → 4 → 8 pods (capped at max)
- **Stabilization:** None (scales up immediately)

### Scale-Down Behavior
- **Trigger:** CPU < 70% AND Memory < 80% for 5 minutes
- **Speed:** Reduces pods by 50% every 15 seconds (after 5 min wait)
- **Example:** 4 → 2 pods (respect minReplicas)
- **Stabilization:** 5 minutes to prevent rapid cycling

### Why Conservative Scale-Down?
- Avoids "thrashing" (rapid up/down cycling)
- Gives your application time to stabilize
- Better user experience than constant pod recreation

---

## Troubleshooting

### HPA shows "unknown" metrics
**Problem:**
```
NAME              REFERENCE          TARGETS        MINPODS MAXPODS REPLICAS
vehicle-service   Deployment/...     <unknown>/70%  2       5       2
```

**Solution:**
```bash
# Check if metrics-server is running
kubectl get deployment metrics-server -n kube-system

# Check metrics-server logs
kubectl logs -n kube-system -l k8s-app=metrics-server -f

# Verify pods have resource requests
kubectl get pod vehicle-service-xxx -o yaml | grep -A 5 "resources:"

# If metrics-server is down, reinstall:
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### HPA not scaling despite high load
**Problem:** Pods not increasing even when CPU > 70%

**Solution:**
```bash
# 1. Check if HPA has permission (should be in Deployment)
kubectl describe hpa vehicle-service-hpa

# 2. Verify metrics are being collected
kubectl top pods -l app=vehicle-service

# 3. Check HPA events for errors
kubectl describe hpa vehicle-service-hpa | tail -20

# 4. Ensure resource requests are correct
kubectl get deployment vehicle-service -o yaml | grep -A 8 "resources:"

# 5. Check current replica count vs actual load
kubectl get hpa vehicle-service-hpa
```

### Pods not scaling down
**Problem:** Too many replicas running despite low load

**Solution:**
```bash
# This is normal behavior - HPA waits 5 minutes before scaling down
# Check the event log to confirm
kubectl describe hpa vehicle-service-hpa | grep -i "scale"

# To force immediate test: manually delete a pod and watch it recreate
kubectl delete pod -l app=vehicle-service --all

# This simulates recovery and tests the HPA behavior
```

---

## Production Recommendations

### 1. Adjust Thresholds Based on Actual Load
Monitor your services for 1-2 weeks and adjust:
- CPU threshold: 60-80% (higher = fewer pods, lower = more pods)
- Memory threshold: 75-85% (similar logic)

```bash
# Edit HPA to adjust thresholds
kubectl edit hpa vehicle-service-hpa
# Change: averageUtilization: 70 → your_value
```

### 2. Account for Database Connections
Each pod instance opens PostgreSQL connections. Monitor connection pool:
```bash
# Check current connections to database
kubectl exec -it postgres-xxx -- psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Adjust PostgreSQL max_connections if needed (default 100)
# Rough calculation: (max_pods × 2 requests per pod) < max_connections
# Vehicle (5 pods × 2) + Maintenance (4 pods × 2) + Driver (6 pods × 2) = 30 connections (safe)
```

### 3. Set Resource Limits Appropriately
Current: 500m CPU, 512Mi memory per pod
- Test with real load to optimize
- Too high: Wastes resources
- Too low: Triggers premature scaling

### 4. Monitor with Prometheus + Grafana
```bash
# Install Prometheus for long-term metrics
kubectl apply -f https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.60.0/bundle.yaml

# View HPA metrics in Grafana dashboards
# Key metrics: container_cpu_usage_seconds_total, container_memory_usage_bytes
```

### 5. Use Pod Disruption Budgets (PDB)
Ensure HPA respects graceful shutdown:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: vehicle-service-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: vehicle-service
```

---

## File Reference

```
infrastructure/ansible/k8s/
├── vehicle-service-deployment.yaml   # Updated with resource requests
├── maintenance-service-deployment.yaml
├── driver-service-deployment.yaml
└── hpa/
    ├── vehicle-service-hpa.yaml
    ├── maintenance-service-hpa.yaml
    └── driver-service-hpa.yaml
```

---

## Quick Commands

```bash
# Deploy all HPA
kubectl apply -f infrastructure/ansible/k8s/hpa/

# Monitor all HPA
kubectl get hpa -w

# Get HPA details for a service
kubectl describe hpa vehicle-service-hpa

# View current replica counts
kubectl get deployment -o wide | grep -E "vehicle|maintenance|driver"

# View resource usage
kubectl top nodes
kubectl top pods -l app=vehicle-service

# Delete HPA (reverts to manual replica management)
kubectl delete hpa --all

# Update HPA (e.g., change max replicas)
kubectl patch hpa vehicle-service-hpa -p '{"spec":{"maxReplicas":10}}'
```

---

## Next Steps
1. ✅ Deploy HPA configurations
2. ✅ Monitor for 24 hours to ensure metrics collection works
3. ⚠️ Perform load testing to verify scaling behavior
4. 📊 Adjust thresholds based on actual workload patterns
5. 🔐 Implement resource quotas per namespace
6. 📈 Set up monitoring dashboards (Prometheus/Grafana)

