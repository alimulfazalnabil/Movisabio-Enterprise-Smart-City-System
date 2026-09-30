# MoviSabio Enterprise Platform & AITCS: Deployment & Operations Runbook

This runbook outlines the standard procedures for provisioning, deploying, scaling, and recovering the unified MoviSabio Enterprise Smart City and AITCS platform across multi-region Azure Kubernetes Service (AKS) clusters.

---

## 1. Prerequisites & Cluster Setup

Ensure the following command-line tools are installed and configured with administrative access to your Azure AKS clusters:
* `kubectl` (v1.28+)
* `helm` (v3.14+)
* `argocd` CLI (v2.10+)

### Namespace Creation
```bash
kubectl create namespace movisabio-production
kubectl create namespace argocd
