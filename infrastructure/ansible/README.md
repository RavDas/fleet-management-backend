# Fleet Management Ansible Configuration

Ansible playbooks for automated infrastructure setup and configuration management.

## 📋 Contents

- `k8-cluster-setup.yaml` - Kubernetes cluster setup (control plane + workers)
- `hosts.ini` - Ansible inventory file

## 🚀 Quick Start

### Prerequisites

```bash
# Install Ansible
sudo apt update
sudo apt install ansible -y

# Or on macOS
brew install ansible

# Verify installation
ansible --version
```

### SSH Setup

Ensure you have SSH access to all nodes:

```bash
# Test connectivity
ansible all -i hosts.ini -m ping

# If using SSH keys
ssh-copy-id ubuntu@<control-plane-ip>
ssh-copy-id ubuntu@<worker1-ip>
ssh-copy-id ubuntu@<worker2-ip>
```

## ⚙️ Configuration

### 1. Update Inventory File (`hosts.ini`)

Edit `hosts.ini` with your actual server IPs:

```ini
[control]
control ansible_host=YOUR_CONTROL_IP ansible_user=ubuntu

[workers]
worker1 ansible_host=YOUR_WORKER1_IP ansible_user=ubuntu
worker2 ansible_host=YOUR_WORKER2_IP ansible_user=ubuntu

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

**Important:** Replace the IP addresses with your actual EC2 instances or VMs.

### 2. Update Playbook Variables (`k8-cluster-setup.yaml`)

Edit the `vars` section in the playbook:

```yaml
vars:
  kube_version: "1.31.0"           # Kubernetes version
  pod_network_cidr: "10.244.0.0/16" # Pod network CIDR (for Flannel)
  control_plane_ip: "YOUR_CONTROL_PLANE_PRIVATE_IP"  # ⚠️ Must match control node private IP
```

**Critical:** The `control_plane_ip` must be the **private IP** of your control plane node.

## 🎯 Running the Playbook

### Check Connectivity

```bash
# Ping all nodes
ansible all -i hosts.ini -m ping

# Check disk space
ansible all -i hosts.ini -m shell -a "df -h"

# Check memory
ansible all -i hosts.ini -m shell -a "free -m"
```

### Dry Run (Check Mode)

```bash
ansible-playbook -i hosts.ini k8-cluster-setup.yaml --check
```

### Execute Playbook

```bash
# Run the full cluster setup
ansible-playbook -i hosts.ini k8-cluster-setup.yaml

# With verbose output
ansible-playbook -i hosts.ini k8-cluster-setup.yaml -v

# With extra verbosity (debugging)
ansible-playbook -i hosts.ini k8-cluster-setup.yaml -vvv
```

### Run Specific Parts

```bash
# Only setup control plane
ansible-playbook -i hosts.ini k8-cluster-setup.yaml --limit control

# Only setup workers
ansible-playbook -i hosts.ini k8-cluster-setup.yaml --limit workers

# Only run specific tasks (using tags, if defined)
ansible-playbook -i hosts.ini k8-cluster-setup.yaml --tags "install"
```

## 📦 What the Playbook Does

### Phase 1: All Nodes (Control + Workers)

1. ✅ **System Update** - Updates all packages
2. ✅ **Disable Swap** - Required for Kubernetes
3. ✅ **Kernel Modules** - Loads overlay and br_netfilter
4. ✅ **Network Configuration** - Configures sysctl for Kubernetes
5. ✅ **Install Dependencies** - curl, apt-transport-https, etc.
6. ✅ **Add Kubernetes Repo** - Official Kubernetes APT repository
7. ✅ **Install K8s Components** - kubelet, kubeadm, kubectl
8. ✅ **Install containerd** - Container runtime
9. ✅ **Configure containerd** - SystemdCgroup and CRI settings

### Phase 2: Control Plane Only

1. ✅ **Initialize Cluster** - `kubeadm init`
2. ✅ **Setup kubeconfig** - For kubectl access
3. ✅ **Generate Join Command** - Saves to `join-command.sh`
4. ✅ **Install Flannel CNI** - Pod networking

### Phase 3: Worker Nodes

1. ✅ **Join Cluster** - Using the join command from control plane
2. ✅ **Configure kubelet** - Automatic via join command

## 🔍 Post-Installation Verification

### On Control Plane Node

SSH into the control plane and verify:

```bash
# Check cluster status
kubectl get nodes

# Should show all nodes in Ready state
# NAME      STATUS   ROLES           AGE   VERSION
# control   Ready    control-plane   5m    v1.31.0
# worker1   Ready    <none>          3m    v1.31.0
# worker2   Ready    <none>          3m    v1.31.0

# Check system pods
kubectl get pods -n kube-system

# Check cluster info
kubectl cluster-info

# Check component status
kubectl get cs
```

### From Your Local Machine

Copy kubeconfig from control plane:

```bash
# Copy kubeconfig to local machine
scp ubuntu@<control-plane-ip>:~/.kube/config ~/.kube/config-fleet

# Use it
export KUBECONFIG=~/.kube/config-fleet
kubectl get nodes
```

## 🛠️ Troubleshooting

### Playbook Fails: "Unable to connect"

```bash
# Check SSH connectivity
ssh ubuntu@<node-ip>

# Check ansible connectivity
ansible all -i hosts.ini -m ping

# Try with password authentication
ansible-playbook -i hosts.ini k8-cluster-setup.yaml --ask-pass
```

### Nodes Not Ready

```bash
# SSH to control plane
ssh ubuntu@<control-plane-ip>

# Check node status
kubectl get nodes -o wide

# Check kubelet logs
sudo journalctl -u kubelet -f

# Check containerd
sudo systemctl status containerd
```

### Workers Not Joining

```bash
# Check the join-command.sh file was created
cat join-command.sh

# Manually join a worker
ssh ubuntu@<worker-ip>
sudo bash /path/to/join-command.sh

# Check kubelet on worker
sudo systemctl status kubelet
```

### Flannel CNI Issues

```bash
# Check flannel pods
kubectl get pods -n kube-system | grep flannel

# Restart flannel if needed
kubectl delete pods -n kube-system -l app=flannel

# Check CNI logs
kubectl logs -n kube-system -l app=flannel
```

### Rerunning the Playbook

The playbook is designed to be idempotent, but if cluster is already initialized:

```bash
# Reset all nodes first
ansible all -i hosts.ini -m shell -a "sudo kubeadm reset -f" --become

# Then rerun
ansible-playbook -i hosts.ini k8-cluster-setup.yaml
```

## 🔒 Security Considerations

### Before Running in Production

1. **SSH Keys**: Use SSH key-based authentication, not passwords
2. **Firewall Rules**: Configure security groups/firewall rules:
   - Control Plane: 6443 (API), 2379-2380 (etcd), 10250-10252
   - Workers: 10250 (kubelet), 30000-32767 (NodePorts)
3. **Network Isolation**: Use private IPs, VPN, or bastion host
4. **User Permissions**: Don't use root user; use sudo
5. **Secrets Management**: Consider Ansible Vault for sensitive data

### Using Ansible Vault

Encrypt sensitive inventory file:

```bash
# Encrypt hosts.ini
ansible-vault encrypt hosts.ini

# Run with vault password
ansible-playbook -i hosts.ini k8-cluster-setup.yaml --ask-vault-pass

# Edit encrypted file
ansible-vault edit hosts.ini
```

## 📊 Infrastructure Requirements

### Minimum Requirements (Per Node)

- **OS**: Ubuntu 20.04+ (tested) / Debian-based Linux
- **CPU**: 2 cores (control: 2+, workers: 1+)
- **RAM**: 2GB (control: 4GB+, workers: 2GB+)
- **Disk**: 20GB
- **Network**: Private network connectivity between nodes

### Recommended AWS Instance Types

- **Control Plane**: t3.medium (2 vCPU, 4GB RAM)
- **Workers**: t3.small (2 vCPU, 2GB RAM)

## 🔄 Common Operations

### Add More Worker Nodes

1. Add new node to `hosts.ini`:
```ini
[workers]
worker1 ansible_host=...
worker2 ansible_host=...
worker3 ansible_host=NEW_IP ansible_user=ubuntu
```

2. Run playbook on new node only:
```bash
ansible-playbook -i hosts.ini k8-cluster-setup.yaml --limit worker3
```

### Upgrade Kubernetes Version

1. Update `kube_version` in playbook
2. Run upgrade procedure (not automated - manual process recommended)

### Remove a Node

```bash
# On control plane
kubectl drain <node-name> --ignore-daemonsets
kubectl delete node <node-name>

# On the node being removed
sudo kubeadm reset -f
```

## 📚 Additional Resources

- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- [Ansible Documentation](https://docs.ansible.com/)
- [kubeadm Setup Guide](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/)
- [Flannel CNI](https://github.com/flannel-io/flannel)

## 🆘 Getting Help

### Check Playbook Syntax

```bash
ansible-playbook --syntax-check k8-cluster-setup.yaml
```

### List All Tasks

```bash
ansible-playbook -i hosts.ini k8-cluster-setup.yaml --list-tasks
```

### List All Hosts

```bash
ansible all -i hosts.ini --list-hosts
```

## 📝 Notes

- **Join Command**: The playbook saves `join-command.sh` locally - keep it secure!
- **Idempotency**: Most tasks are idempotent except cluster init
- **Logs**: Control plane init log saved to `/root/kubeinit.log`
- **CNI**: Currently uses Flannel - can be customized to Calico, Weave, etc.
- **Container Runtime**: Uses containerd (recommended for K8s 1.24+)

## ⚠️ Important Files Generated

After running the playbook:

- `join-command.sh` - Token for joining workers (expires in 24h)
- `/root/kubeinit.log` - Cluster initialization log (on control plane)
- `~/.kube/config` - Kubectl configuration (on control plane)

**Security Note**: The join command contains sensitive tokens. Protect `join-command.sh` and regenerate if needed:

```bash
# On control plane
kubeadm token create --print-join-command
```

