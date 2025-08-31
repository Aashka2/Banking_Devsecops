# Secure Banking Dashboard — DevSecOps MVP

A minimal **banking-style dashboard** with a **secure, cloud-ready DevOps pipeline**. Built to impress MNCs (e.g., JPMorgan) by demonstrating **CI/CD, containerization, Kubernetes, and security scanning**.

---

## Features (MVP)
- Flask API with endpoints: `/api/login`, `/api/balance`, `/api/transactions`, `/api/fraud-alerts`
- React single-page dashboard (login, balance, transactions, alerts)
- Dockerized frontend and backend
- `docker-compose` for local run
- Kubernetes manifests (Deployments, Services, Ingress, Namespace)
- GitHub Actions CI/CD with:
  - Unit tests (pytest)
  - Docker build & push
  - Trivy vulnerability scan
  - `kubectl apply` deployment (requires kubeconfig secret)

---

## Quick Start (Local with Docker Compose)

```bash
# 1) From the project root:
docker compose up --build

# Frontend: http://localhost:8080
# Backend health: http://localhost:5000/api/health
# Login with: demo@bank.com / demo123
```

---

## CI/CD (GitHub Actions)
1. Create a repo and push this project.
2. In **Repository → Settings → Secrets and variables → Actions**, add:
   - `DOCKERHUB_USERNAME` — your Docker Hub username
   - `DOCKERHUB_TOKEN` — a Docker Hub access token
   - `KUBE_CONFIG_DATA` — base64 of your kubeconfig for the target cluster
3. Push to `main`. The workflow will:
   - Run tests
   - Build & push images: `${DOCKERHUB_USERNAME}/banking-backend:latest` and `${DOCKERHUB_USERNAME}/banking-frontend:latest`
   - Scan both images with **Trivy**
   - `kubectl apply -f k8s/` to deploy (namespace: `devsecops`)

> Tip: Replace image tags with commit SHA in a real pipeline for immutability.

---

## Kubernetes (Preview)
```bash
kubectl apply -f k8s/namespace.yaml
# Replace placeholder with your DockerHub username
sed -i 's|DOCKERHUB_USERNAME|<your-dockerhub-username>|g' k8s/*deployment.yaml
kubectl -n devsecops apply -f k8s/
kubectl -n devsecops get svc,deploy,ingress
```

- **Access**: If using an ingress controller (NGINX), point a DNS or use the ingress external IP.  
- The frontend Nginx proxies `/api/*` → backend service (`backend:5000`), so your browser can call `/api/...` directly.

---

## Security & Observability (Next Steps)
- Add **Bandit** (Python static analysis) & **Hadolint** (Dockerfile lint) to CI
- Add **OPA/Conftest** to enforce policies (no root containers, resource limits)
- Add **Prometheus + Grafana** via Helm for metrics and dashboards
- Use **Terraform** to provision EKS/GKE (Phase 2)

---

## Repo Structure
```
backend/             # Flask API
frontend/            # React + Vite, served by Nginx
k8s/                 # Kubernetes manifests (namespace, deployments, services, ingress)
.github/workflows/   # CI/CD pipeline
docker-compose.yml   # Local dev
```

---

## Why this impresses MNCs
- **Domain-aligned** (banking UI, fraud rule)
- **DevSecOps** (tests, scans, containers, K8s)
- **Cloud-ready** (just add kubeconfig & secrets to deploy)
