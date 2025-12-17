# Fleet Management Kubernetes Deployment Guide

## Overview
This guide walks through deploying the Fleet Management microservices (Vehicle, Maintenance, Driver) to Kubernetes with PostgreSQL backend, Istio service mesh, and security configurations.

---

## Architecture
```
┌─────────────────────────────────────────────────────┐
│          Istio IngressGateway (Port 80)             │
├─────────────────────────────────────────────────────┤
│  Fleet Gateway (Routes traffic based on URL path)   │
├──────────┬──────────────┬──────────────┬────────────┤
│          │              │              │            │
▼          ▼              ▼              ▼            
Vehicle   Maintenance   Driver       (Keycloak)     
Service   Service       Service      (Auth Server)  
Port:8080 Port:5001     Port:6001                   
│          │              │                          
└──────────┼──────────────┴──────────────┬───────────┘
           │                             │
           ▼─────────────────────────────▼
        PostgreSQL Database (Port 5432)
        ├── vehicle_db
        ├── maintenance_db
        └── driver_db
```

---

## Prerequisites
- Kubernetes cluster (1.23+) with kubectl configured
- Istio installed (`istioctl` available)
- Docker images built and available:
  - `vehicle-service:latest`
  - `maintenance-service:latest`
  - `driver-service:latest`

---

## Deployment Order (CRITICAL)

### Step 1: Create Namespace and Label for Istio Injection
```bash
kubectl create namespace default  # or use your namespace
kubectl label namespace default istio-injection=enabled --overwrite
```

### Step 2: Create Secrets and ConfigMaps
**Why first:** Deployments reference these; they must exist before pods start.

```bash
# Create all Secrets
kubectl apply -f infrastructure/ansible/k8s/secrets/postgres-credentials.yaml
kubectl apply -f infrastructure/ansible/k8s/secrets/vehicle-service-secrets.yaml
kubectl apply -f infrastructure/ansible/k8s/secrets/maintenance-service-secrets.yaml
kubectl apply -f infrastructure/ansible/k8s/secrets/driver-service-secrets.yaml

# Create all ConfigMaps
kubectl apply -f infrastructure/ansible/k8s/configmaps/vehicle-service-config.yaml
kubectl apply -f infrastructure/ansible/k8s/configmaps/maintenance-service-config.yaml
kubectl apply -f infrastructure/ansible/k8s/configmaps/driver-service-config.yaml

# Verify
kubectl get secrets,configmaps
```

### Step 3: Deploy PostgreSQL
**Why before services:** Services depend on database connectivity.

```bash
# Create PostgreSQL initialization config
kubectl apply -f infrastructure/ansible/k8s/postgres-init-config.yaml

# Create PersistentVolumeClaim for data persistence
kubectl apply -f infrastructure/ansible/k8s/postgres-pvc.yaml

# Deploy PostgreSQL
kubectl apply -f infrastructure/ansible/k8s/postgres-deployment.yaml
kubectl apply -f infrastructure/ansible/k8s/postgres-service.yaml

# Wait for PostgreSQL to be ready (2-3 minutes)
kubectl wait --for=condition=ready pod -l app=postgres --timeout=300s

# Verify databases were created
kubectl exec -it $(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}') -- \
  psql -U postgres -c "\l"
```

### Step 4: Deploy Microservices
```bash
# Vehicle Service
kubectl apply -f infrastructure/ansible/k8s/vehicle-service-deployment.yaml
kubectl apply -f infrastructure/ansible/k8s/vehicle-service-service.yaml

# Maintenance Service
kubectl apply -f infrastructure/ansible/k8s/maintenance-service-deployment.yaml
kubectl apply -f infrastructure/ansible/k8s/maintenance-service-service.yaml

# Driver Service
kubectl apply -f infrastructure/ansible/k8s/driver-service-deployment.yaml
kubectl apply -f infrastructure/ansible/k8s/driver-service-service.yaml

# Wait for all services to be ready
kubectl wait --for=condition=ready pod -l app=vehicle-service --timeout=300s
kubectl wait --for=condition=ready pod -l app=maintenance-service --timeout=300s
kubectl wait --for=condition=ready pod -l app=driver-service --timeout=300s

# Verify
kubectl get pods,svc
```

### Step 5: Deploy Istio Resources
**Why after services:** VirtualServices reference existing Services.

```bash
# Create Istio Gateway
kubectl apply -f infrastructure/ansible/k8s/istio/gateway.yaml

# Create VirtualServices and DestinationRules
kubectl apply -f infrastructure/ansible/k8s/istio/vehicle-virtualservice.yaml
kubectl apply -f infrastructure/ansible/k8s/istio/vehicle-destinationrule.yaml
kubectl apply -f infrastructure/ansible/k8s/istio/maintenance-virtualservice.yaml
kubectl apply -f infrastructure/ansible/k8s/istio/maintenance-destinationrule.yaml
kubectl apply -f infrastructure/ansible/k8s/istio/driver-virtualservice.yaml
kubectl apply -f infrastructure/ansible/k8s/istio/driver-destinationrule.yaml

# Verify Istio resources
kubectl get gateway,virtualservice,destinationrule
```

---

## Configuration Summary

### Database Configuration
All microservices connect to PostgreSQL at `postgres:5432` (K8s service DNS):

| Service | Database | Port | Connection |
|---------|----------|------|------------|
| Vehicle | vehicle_db | 5432 | From Secret: postgres-credentials |
| Maintenance | maintenance_db | 5432 | From Secret: postgres-credentials |
| Driver | driver_db | 5432 | From Secret: postgres-credentials |

**Credentials:** Injected from `postgres-credentials` Secret:
- Username: `postgres`
- Password: `postgres` (change in production!)

### Service Ports
| Service | Container Port | Kubernetes Service Port |
|---------|-----------------|------------------------|
| Vehicle | 8080 | 80 (via Istio) |
| Maintenance | 5001 | 80 (via Istio) |
| Driver | 6001 | 80 (via Istio) |

### Environment Variables Injected

**Vehicle Service:**
- From ConfigMap: `ASPNETCORE_ENVIRONMENT`, `ASPNETCORE_URLS`, `CORS_ORIGINS`, `Authentication__JwtBearer__RequireHttpsMetadata`
- From Secret: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `KEYCLOAK_AUTHORITY`

**Maintenance Service:**
- From ConfigMap: `FLASK_ENV`, `FLASK_APP`, `PORT`, `HOST`, `CORS_ORIGINS`, `ITEMS_PER_PAGE`, `LOG_LEVEL`, `AUTH_DISABLED`
- From Secret: `DATABASE_URL`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`

**Driver Service:**
- From ConfigMap: `SPRING_PROFILES_ACTIVE`, `SERVER_PORT`, `JPA_SHOW_SQL`, `OIDC_REALM`, `OIDC_VALIDATE_ISSUER`
- From Secret: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `OIDC_ISSUER_URI`

---

## Verification Steps

### 1. Check all pods are running
```bash
kubectl get pods
# Expected output: All pods in Running state with 2/2 ready (1 app + 1 Istio sidecar)
```

### 2. Check services are accessible
```bash
kubectl get svc
# Expected: ClusterIP services for postgres, vehicle-service, maintenance-service, driver-service
```

### 3. Check Istio resources
```bash
kubectl get gateway,virtualservice
```

### 4. Get Istio IngressGateway details
```bash
kubectl -n istio-system get svc istio-ingressgateway
# Get the EXTERNAL-IP (or use minikube service for local testing)
```

### 5. Test connectivity
```bash
# Port-forward for local testing (if no external IP)
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80

# Then test endpoints
curl http://localhost:8080/vehicle/health
curl http://localhost:8080/maintenance/health
curl http://localhost:8080/driver/health
```

### 6. Check database connectivity
```bash
# Connect to postgres pod
kubectl exec -it postgres-<pod-id> -- psql -U postgres

# Inside psql, check databases exist
\l

# Check tables in each database
\c vehicle_db
\dt

\c maintenance_db
\dt

\c driver_db
\dt
```

### 7. View logs
```bash
# Vehicle Service
kubectl logs -l app=vehicle-service -c vehicle-service

# Maintenance Service
kubectl logs -l app=maintenance-service -c maintenance-service

# Driver Service
kubectl logs -l app=driver-service -c driver-service

# PostgreSQL
kubectl logs -l app=postgres -c postgres
```

---

## Troubleshooting

### Pod won't start: ImagePullBackOff
**Issue:** Docker image not found
**Solution:**
```bash
# Build and push images to registry
docker build -t your-registry/vehicle-service:latest -f src/vehicleService/Dockerfile src/vehicleService
docker push your-registry/vehicle-service:latest

# Update image in deployment
kubectl set image deployment/vehicle-service vehicle-service=your-registry/vehicle-service:latest
```

### Pod stuck in Init:0/1 or CrashLoopBackOff
**Issue:** Service can't connect to database
**Solution:**
```bash
# Check pod logs
kubectl logs <pod-name> -c <container-name>

# Verify PostgreSQL is ready
kubectl get pod -l app=postgres

# Test database connectivity from a pod
kubectl run -it --rm debug --image=postgres:16-alpine --restart=Never -- \
  psql -h postgres -U postgres -c "SELECT 1;"
```

### Connection refused on localhost:5432
**Issue:** Using localhost instead of service name
**Solution:** Deployments use `postgres` (K8s service DNS), not `localhost`
- Update environment variables to point to `postgres` service
- Check Secrets and ConfigMaps have correct values

### Istio routing not working
**Issue:** Requests not reaching services through gateway
**Solution:**
```bash
# Check gateway configuration
kubectl describe gateway fleet-gateway

# Check virtual services
kubectl describe vs vehicle-virtualservice

# Verify pod has sidecar proxy injected
kubectl get pods -o jsonpath='{.items[0].spec.containers[*].name}'
# Should show: vehicle-service, istio-proxy

# Check proxy config
kubectl logs <pod-name> -c istio-proxy | grep -i route
```

---

## Production Checklist

- [ ] **Secrets:** Replace default passwords with secure values
- [ ] **TLS:** Enable HTTPS/mTLS in Istio DestinationRules
- [ ] **Persistence:** Use cloud provider storage classes instead of local PVC
- [ ] **High Availability:** Set replicas > 1 in Deployments
- [ ] **Resource Limits:** Review and adjust CPU/memory limits
- [ ] **Health Probes:** Verify liveness/readiness probes are correct
- [ ] **Image Registry:** Use private registry and image pull secrets
- [ ] **Keycloak:** Ensure Keycloak is accessible from cluster
- [ ] **Monitoring:** Set up Prometheus/Grafana with Istio metrics
- [ ] **Network Policies:** Restrict pod-to-pod communication
- [ ] **RBAC:** Create service accounts with minimal permissions

---

## Cleanup
```bash
# Delete all Istio resources
kubectl delete -f infrastructure/ansible/k8s/istio/ --ignore-not-found

# Delete all services
kubectl delete -f infrastructure/ansible/k8s/*-service.yaml --ignore-not-found

# Delete all deployments
kubectl delete -f infrastructure/ansible/k8s/*-deployment.yaml --ignore-not-found

# Delete ConfigMaps and Secrets
kubectl delete -f infrastructure/ansible/k8s/configmaps/ --ignore-not-found
kubectl delete -f infrastructure/ansible/k8s/secrets/ --ignore-not-found

# Delete PostgreSQL resources
kubectl delete -f infrastructure/ansible/k8s/postgres-* --ignore-not-found
```

---

## File Reference

```
infrastructure/ansible/k8s/
├── secrets/
│   ├── postgres-credentials.yaml        # Shared DB credentials
│   ├── vehicle-service-secrets.yaml     # Vehicle service secrets
│   ├── maintenance-service-secrets.yaml # Maintenance service secrets
│   └── driver-service-secrets.yaml      # Driver service secrets
├── configmaps/
│   ├── vehicle-service-config.yaml      # Vehicle service config
│   ├── maintenance-service-config.yaml  # Maintenance service config
│   └── driver-service-config.yaml       # Driver service config
├── postgres-init-config.yaml            # PostgreSQL init script
├── postgres-pvc.yaml                    # PostgreSQL persistent storage
├── postgres-deployment.yaml             # PostgreSQL deployment
├── postgres-service.yaml                # PostgreSQL service
├── vehicle-service-deployment.yaml      # Vehicle service deployment
├── vehicle-service-service.yaml         # Vehicle service service
├── maintenance-service-deployment.yaml  # Maintenance service deployment
├── maintenance-service-service.yaml     # Maintenance service service
├── driver-service-deployment.yaml       # Driver service deployment
├── driver-service-service.yaml          # Driver service service
└── istio/
    ├── gateway.yaml                     # Istio ingress gateway
    ├── vehicle-virtualservice.yaml      # Vehicle service routing
    ├── vehicle-destinationrule.yaml     # Vehicle service traffic policy
    ├── maintenance-virtualservice.yaml  # Maintenance service routing
    ├── maintenance-destinationrule.yaml # Maintenance service traffic policy
    ├── driver-virtualservice.yaml       # Driver service routing
    └── driver-destinationrule.yaml      # Driver service traffic policy
```

---

## Next Steps
1. **Test endpoints** through Istio IngressGateway
2. **Enable mTLS** by updating DestinationRules
3. **Set up monitoring** with Prometheus + Grafana
4. **Configure CI/CD** to automate deployments
5. **Implement GitOps** with ArgoCD or Flux
