# Marketing Automation - Kubernetes Deployment Guide

Complete deployment guide for the Vietnamese Marketing Automation system using Kubernetes and FluxCD GitOps.

## Architecture Overview

**Technology Stack:**
- **AI Agent Framework:** Agno (AgentOS runtime)
- **Workflow Orchestration:** n8n
- **LLM:** Claude 4.0 Sonnet (Anthropic)
- **Vietnamese TTS:** Vbee
- **Video Generation:** Simplified, HeyGen, D-ID, Runway (multi-tool strategy)
- **Database:** PostgreSQL 16 with pgvector
- **GitOps:** FluxCD
- **Monitoring:** Prometheus, Grafana, Loki

**Monthly Cost:** $352-387 (well under $500 budget)

## Prerequisites

1. **Kubernetes Cluster (DigitalOcean Kubernetes)**
   ```bash
   # Create DOKS cluster via CLI
   doctl kubernetes cluster create marketing-automation \
     --region sgp1 \
     --version 1.29.1-do.0 \
     --node-pool "name=worker-pool;size=s-4vcpu-8gb;count=2;auto-scale=true;min-nodes=2;max-nodes=4"
   ```

2. **Tools Installation**
   ```bash
   # kubectl
   brew install kubectl

   # FluxCD CLI
   brew install fluxcd/tap/flux

   # kubeseal (for sealed secrets)
   brew install kubeseal

   # doctl (DigitalOcean CLI)
   brew install doctl
   ```

3. **Domain Name**
   - Purchase domain: `marketing.your-domain.com`
   - Point DNS A record to LoadBalancer IP (will be created during deployment)

## Step 1: Bootstrap FluxCD

```bash
# Configure kubectl to use your cluster
doctl kubernetes cluster kubeconfig save marketing-automation

# Verify cluster access
kubectl get nodes

# Bootstrap FluxCD with GitHub repo
export GITHUB_TOKEN=<your-github-personal-access-token>
export GITHUB_USER=<your-github-username>

flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=marketing-automation \
  --branch=main \
  --path=clusters/production \
  --personal
```

FluxCD is now installed and watching your GitHub repository!

## Step 2: Prepare Secrets

All secrets must be encrypted using SealedSecrets before committing to Git.

### Create Secret File

Create a temporary file `secrets-raw.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: marketing-automation
type: Opaque
stringData:
  POSTGRES_PASSWORD: "your-strong-postgres-password"
  postgres-exporter-dsn: "postgresql://postgres_exporter:exporter-password@postgres-service:5432/marketing_automation?sslmode=disable"
---
apiVersion: v1
kind: Secret
metadata:
  name: api-keys-secret
  namespace: marketing-automation
type: Opaque
stringData:
  ANTHROPIC_API_KEY: "sk-ant-api03-..."
  SIMPLIFIED_API_KEY: "simplified_..."
  HEYGEN_API_KEY: "heygen_..."
  DID_API_KEY: "did_..."
  RUNWAY_API_KEY: "runway_..."
  VBEE_API_KEY: "vbee_..."
  FACEBOOK_ACCESS_TOKEN: "fb_..."
  FACEBOOK_PAGE_ID: "123456789"
  TIKTOK_ACCESS_TOKEN: "tiktok_..."
  TIKTOK_CLIENT_KEY: "tiktok_client_..."
  SHOPEE_PARTNER_ID: "shopee_partner_id"
  SHOPEE_PARTNER_KEY: "shopee_partner_key"
  SHOPEE_SHOP_ID: "12345"
  YOUTUBE_CLIENT_ID: "youtube_..."
  YOUTUBE_CLIENT_SECRET: "youtube_secret_..."
  YOUTUBE_REFRESH_TOKEN: "youtube_refresh_..."
  TICKERTRENDS_API_KEY: "tickertrends_..."
  N8N_ENCRYPTION_KEY: "$(openssl rand -hex 32)"
---
apiVersion: v1
kind: Secret
metadata:
  name: slack-webhook-secret
  namespace: marketing-automation
type: Opaque
stringData:
  SLACK_WEBHOOK_URL: "https://hooks.slack.com/services/..."
  SLACK_CRITICAL_WEBHOOK_URL: "https://hooks.slack.com/services/..."
```

### Seal Secrets

```bash
# Install SealedSecret controller (FluxCD will do this automatically)
# Wait for it to be ready
kubectl wait --for=condition=ready pod -l name=sealed-secrets-controller -n kube-system --timeout=300s

# Seal the secrets
kubeseal --format=yaml < secrets-raw.yaml > k8s/base/sealed-secrets.yaml

# Delete the raw secrets file
rm secrets-raw.yaml

# Commit sealed secrets to git (it's encrypted, safe to commit)
git add k8s/base/sealed-secrets.yaml
git commit -m "Add sealed secrets"
git push
```

### Update k8s/base/kustomization.yaml

Add sealed-secrets.yaml to resources:

```yaml
resources:
  - 00-namespace.yaml
  - 01-configmap.yaml
  - sealed-secrets.yaml  # Add this line
  - 03-postgres.yaml
  - 04-agentos.yaml
  - 05-n8n.yaml
  - 06-approval-ui.yaml
  - 07-ingress.yaml
```

Remove `02-secrets.yaml` from kustomization (it's just a template).

## Step 3: Update Configuration

### Update ConfigMap Domain

Edit `k8s/base/01-configmap.yaml`:

```yaml
data:
  N8N_HOST: "marketing.your-actual-domain.com"  # CHANGE THIS
  WEBHOOK_URL: "https://marketing.your-actual-domain.com/n8n"  # CHANGE THIS
  APPROVAL_UI_URL: "https://marketing.your-actual-domain.com"  # CHANGE THIS
```

### Update ClusterIssuer Email

Edit `clusters/production/infrastructure.yaml`:

```yaml
spec:
  acme:
    email: your-real-email@example.com  # CHANGE THIS
```

### Update Container Registry

Edit `k8s/base/04-agentos.yaml` and `k8s/base/06-approval-ui.yaml`:

```yaml
image: your-dockerhub-username/agentos:latest  # CHANGE THIS
image: your-dockerhub-username/approval-ui:latest  # CHANGE THIS
```

Or use DigitalOcean Container Registry:

```yaml
image: registry.digitalocean.com/your-registry/agentos:latest
image: registry.digitalocean.com/your-registry/approval-ui:latest
```

## Step 4: Build and Push Container Images

### AgentOS Container

```bash
cd agentos/

# Build image
docker build -t your-registry/agentos:latest .

# Push to registry
docker push your-registry/agentos:latest
```

### Approval UI Container

```bash
cd approval-ui/

# Build image
docker build -t your-registry/approval-ui:latest .

# Push to registry
docker push your-registry/approval-ui:latest
```

## Step 5: Commit and Deploy

```bash
# Add all changes
git add .

# Commit
git commit -m "Deploy marketing automation to Kubernetes"

# Push to GitHub
git push origin main
```

FluxCD will automatically:
1. Detect changes in GitHub
2. Apply infrastructure (cert-manager, nginx-ingress, sealed-secrets)
3. Deploy base application (PostgreSQL, AgentOS, n8n, Approval UI)
4. Deploy monitoring stack (Prometheus, Grafana, Loki)

## Step 6: Monitor Deployment

```bash
# Watch FluxCD reconciliation
flux get all

# Check Kustomization status
flux get kustomizations

# Watch pods come up
kubectl get pods -n marketing-automation -w

# Check HelmRelease status
flux get helmreleases -A

# View logs for debugging
kubectl logs -n marketing-automation deployment/agentos -f
```

## Step 7: Configure DNS

```bash
# Get LoadBalancer IP
kubectl get svc -n ingress-nginx ingress-nginx-controller

# Output:
# NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP
# ingress-nginx-controller   LoadBalancer   10.245.0.100    123.45.67.89

# Point DNS A record to EXTERNAL-IP
# marketing.your-domain.com -> 123.45.67.89
```

Wait 5-10 minutes for DNS propagation and Let's Encrypt certificate issuance.

## Step 8: Access Services

Once deployment is complete and DNS is configured:

- **Approval UI:** https://marketing.your-domain.com
- **n8n Workflow Editor:** https://marketing.your-domain.com/n8n
- **Grafana Dashboards:** https://grafana.marketing.your-domain.com
- **AgentOS API:** https://marketing.your-domain.com/api

## Step 9: Initialize Database

```bash
# Port-forward to AgentOS
kubectl port-forward -n marketing-automation deployment/agentos 8080:8080

# Run database migrations
curl -X POST http://localhost:8080/admin/migrate

# Load product catalog
curl -X POST http://localhost:8080/admin/import-products \
  -H "Content-Type: application/json" \
  -d @product-catalog.json
```

## Monitoring and Alerts

### Access Grafana

```bash
# Get Grafana admin password
kubectl get secret -n marketing-automation kube-prometheus-stack-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode

# Port-forward to Grafana (or use ingress URL)
kubectl port-forward -n marketing-automation svc/kube-prometheus-stack-grafana 3000:80
```

Open http://localhost:3000 or https://grafana.marketing.your-domain.com

**Available Dashboards:**
1. **Business Metrics** - Content generation, approval rates, platform posts, costs
2. **System Health** - CPU, memory, pod health, errors
3. **Agent Performance** - Agent execution times, success rates, queue lengths

### Configure Slack Alerts

Alerts are already configured in `k8s/monitoring/alertmanager-rules.yaml`.

Ensure you've set Slack webhook URLs in the sealed secrets.

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl get pods -n marketing-automation

# Describe problematic pod
kubectl describe pod -n marketing-automation <pod-name>

# Check logs
kubectl logs -n marketing-automation <pod-name>
```

### Certificate not issued

```bash
# Check cert-manager logs
kubectl logs -n cert-manager deployment/cert-manager

# Check certificate status
kubectl describe certificate -n marketing-automation marketing-tls

# Check certificate request
kubectl describe certificaterequest -n marketing-automation
```

### FluxCD not syncing

```bash
# Check FluxCD system pods
kubectl get pods -n flux-system

# Check source sync
flux get sources git

# Force reconciliation
flux reconcile kustomization marketing-automation-base --with-source
```

## Scaling

### Horizontal Scaling (Auto-scaling configured)

AgentOS will automatically scale from 1 to 5 replicas based on CPU/memory usage.

Manual scaling:

```bash
# Scale AgentOS manually
kubectl scale deployment -n marketing-automation agentos --replicas=3

# Scale Approval UI
kubectl scale deployment -n marketing-automation approval-ui --replicas=3
```

### Vertical Scaling (Increase node size)

```bash
# Resize DigitalOcean node pool
doctl kubernetes cluster node-pool update marketing-automation worker-pool \
  --size s-8vcpu-16gb
```

## Backup and Recovery

### PostgreSQL Backup

```bash
# Create backup
kubectl exec -n marketing-automation postgres-0 -- \
  pg_dump -U agno marketing_automation > backup-$(date +%Y%m%d).sql

# Restore from backup
kubectl exec -i -n marketing-automation postgres-0 -- \
  psql -U agno marketing_automation < backup-20250122.sql
```

### n8n Workflow Backup

n8n workflows are stored in PostgreSQL, backed up with database backups.

Alternatively, export workflows via n8n UI: Settings → Import/Export

## Cost Optimization

**Current monthly cost:** $352-387

**To reduce costs:**
1. **Reduce video tool usage** - Remove Runway ($12/month savings)
2. **Use smaller nodes** - Switch to s-2vcpu-4gb ($20/month savings)
3. **Reduce agent replicas** - Set HPA minReplicas=1 ($15/month savings)
4. **Optimize LLM usage** - Cache repeated queries ($5-10/month savings)

## Security Best Practices

1. **Rotate secrets regularly** - Update sealed secrets every 90 days
2. **Enable Pod Security Standards** - Restrict privileged containers
3. **Network Policies** - Limit pod-to-pod communication
4. **RBAC** - Use service accounts with minimal permissions
5. **Image scanning** - Scan container images for vulnerabilities
6. **Audit logging** - Enable Kubernetes audit logs

## Support and Maintenance

### Update Application

```bash
# Build new image version
docker build -t your-registry/agentos:v1.2.0 .
docker push your-registry/agentos:v1.2.0

# Update deployment
kubectl set image deployment/agentos -n marketing-automation \
  agentos=your-registry/agentos:v1.2.0

# Or update via GitOps (recommended)
# Edit k8s/base/04-agentos.yaml
# Change image tag to v1.2.0
# Commit and push to GitHub
```

### View Metrics

```bash
# Check Prometheus targets
kubectl port-forward -n marketing-automation svc/kube-prometheus-stack-prometheus 9090:9090

# Open http://localhost:9090/targets
```

### View Logs

```bash
# Tail AgentOS logs
kubectl logs -n marketing-automation deployment/agentos -f

# Query Loki logs via Grafana Explore
# Or use logcli
kubectl port-forward -n marketing-automation svc/loki 3100:3100
```

## Next Steps

1. **Implement Agent Logic** - Define TrendMonitor, ContentStrategist, TextCreator, VideoGenerator agents
2. **Create n8n Workflows** - Build workflow for trend monitoring → content generation → approval → publishing
3. **Setup Platform Integrations** - Configure Facebook, TikTok, Shopee API credentials
4. **Test End-to-End** - Run full workflow from trend detection to platform posting
5. **Tune Performance** - Optimize agent execution times, video generation queue
6. **Add Business Logic** - Product catalog RAG, Vietnamese cultural filters

---

**Questions?** Check Agno docs at https://docs.agno.com or n8n docs at https://docs.n8n.io

**Need help?** Open GitHub issue or contact your DevOps team.
