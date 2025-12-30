# 🖥️ GUI Tools Guide - Vietnamese Marketing Automation

## 🚀 QUICK START - All GUIs at Once

### **One Command to Start Everything:**

```bash
cd /home/cid/projects-personal/agent-research/agentos
./start-all-guis.sh
```

**This starts:**
1. ✅ PostgreSQL (database)
2. ✅ pgAdmin (database GUI)
3. ✅ n8n (workflow automation GUI)
4. ✅ AgentOS API server (with interactive docs)

**Time:** 30 seconds  
**Access URLs:** Displayed after startup

---

## 📊 **Available GUIs**

### **1. FastAPI Interactive Docs** ⭐ **BUILT-IN**

**URL:** http://localhost:8080/docs

**What it does:**
- Test all API endpoints
- See request/response formats
- Try trend scanning, content generation
- Debug API issues

**How to use:**
1. Start AgentOS: `python main.py`
2. Open http://localhost:8080/docs
3. Click any endpoint → "Try it out"
4. Fill in parameters → "Execute"
5. See response immediately

**Example: Test Trend Scanning**
```
1. Go to: http://localhost:8080/docs
2. Find: POST /api/v1/trends/scan
3. Click: "Try it out"
4. Enter:
   {
     "product_categories": ["beauty"],
     "min_relevance_score": 0.6,
     "max_briefs": 3
   }
5. Click: "Execute"
6. See: Vietnamese content briefs generated!
```

---

### **2. n8n Workflow Automation** 🔄 **VISUAL**

**URL:** http://localhost:5678  
**Username:** admin  
**Password:** changeme123

**What it does:**
- Create visual workflows (drag & drop)
- Schedule automatic trend scanning
- Connect to AgentOS APIs
- Add approval notifications (Slack, email)
- Automate publishing to platforms

**How to use:**

#### **Create "Daily Trend Scan" Workflow:**

1. **Open n8n:** http://localhost:5678
2. **Click:** "Add workflow"
3. **Add nodes:**
   ```
   [Schedule] → [HTTP Request] → [Filter] → [Slack]
   ```

4. **Configure Schedule Node:**
   - Trigger: Cron
   - Expression: `0 8 * * *` (daily at 8am)

5. **Configure HTTP Request Node:**
   - Method: POST
   - URL: `http://host.docker.internal:8080/api/v1/trends/scan`
   - Body:
     ```json
     {
       "product_categories": ["beauty", "fashion"],
       "min_relevance_score": 0.6,
       "max_briefs": 5
     }
     ```

6. **Configure Filter Node:**
   - Condition: `{{ $json.briefs.length }} > 0`

7. **Configure Slack Node:**
   - Message: `Found {{ $json.briefs.length }} content opportunities!`

8. **Save & Activate!**

**Pre-built Workflows (Coming Soon):**
- Daily trend monitoring
- Batch approval workflow
- Auto-publishing pipeline
- Performance reporting

---

### **3. pgAdmin Database Management** 💾 **DATABASE**

**URL:** http://localhost:5050  
**Email:** admin@admin.com  
**Password:** admin

**What it does:**
- Browse database tables
- Run SQL queries
- View agent data
- Check vector embeddings
- Export/import data

**How to use:**

#### **Connect to Database:**

1. **Open pgAdmin:** http://localhost:5050
2. **Right-click:** Servers → Register → Server
3. **General tab:**
   - Name: `Marketing Automation`
4. **Connection tab:**
   - Host: `host.docker.internal` (Mac/Windows)
   - Host: `172.17.0.1` (Linux)
   - Port: `5432`
   - Database: `marketing_automation`
   - Username: `agno`
   - Password: `changeme123`
5. **Click:** Save

#### **View Tables:**

1. **Expand:** Marketing Automation → Databases → marketing_automation → Schemas → public → Tables
2. **Right-click table:** View/Edit Data → All Rows
3. **See:** Your data in spreadsheet format

#### **Run Queries:**

1. **Click:** Tools → Query Tool
2. **Enter:**
   ```sql
   -- See all content briefs
   SELECT * FROM content_briefs ORDER BY created_at DESC LIMIT 10;
   
   -- See trend analysis
   SELECT * FROM trends WHERE relevance_score > 0.6;
   
   -- Check agent executions
   SELECT agent_name, status, COUNT(*) as executions
   FROM agent_logs
   GROUP BY agent_name, status;
   ```
3. **Click:** Execute (F5)

---

### **4. Grafana Monitoring** 📈 **PRODUCTION**

**URL:** https://grafana.marketing.your-domain.com (after K8s deployment)

**What it does:**
- Real-time metrics dashboards
- Business KPIs (content generated, revenue)
- System health (CPU, memory, errors)
- Agent performance (execution times, success rates)
- Custom alerts

**Pre-built Dashboards:**

#### **Dashboard 1: Business Metrics**
- Content pieces generated (daily chart)
- Approval rate (gauge: approved/rejected)
- Platform posts (breakdown by Facebook, TikTok, Shopee)
- Video generation costs (stacked area chart)
- LLM token usage (line chart)
- Revenue projections (bar chart)

#### **Dashboard 2: System Health**
- Pod status (healthy/unhealthy)
- CPU usage (time series per pod)
- Memory usage (heatmap)
- API error rate (gauge with threshold)
- Request rate (requests/sec)
- Pod restarts (alert if >0)

#### **Dashboard 3: Agent Performance**
- Agent execution duration (histogram)
- Success rate by agent (bar chart)
- Queue lengths (real-time gauge)
- Slowest operations (table)
- Failed executions (log viewer)

**How to access (K8s):**

```bash
# Port-forward to Grafana
kubectl port-forward -n marketing-automation svc/kube-prometheus-stack-grafana 3000:80

# Open
http://localhost:3000

# Get password
kubectl get secret -n marketing-automation kube-prometheus-stack-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode
```

---

### **5. Prometheus Metrics Explorer** 📊 **METRICS**

**URL:** http://localhost:8080/metrics (raw)  
**URL:** http://localhost:9090 (Prometheus UI - K8s only)

**What it does:**
- Raw metrics data
- Query metrics with PromQL
- Create custom graphs
- Set up alerts

**Available Metrics:**

```prometheus
# Agent executions
agent_executions_total{agent_name="TrendMonitor", status="completed"}

# Content approvals
content_approval_total{decision="approved"}

# Platform posts
platform_posts_total{platform="facebook", status="success"}

# Trends monitored
trends_monitored_total{source="tiktok"}

# LLM usage
llm_tokens_used_total{provider="zhipu", model="glm-4.6", type="output"}
```

**Example Queries:**

```promql
# Approval rate
sum(content_approval_total{decision="approved"}) / 
sum(content_approval_total)

# Agent success rate
sum(rate(agent_executions_total{status="completed"}[5m])) / 
sum(rate(agent_executions_total[5m]))

# Average execution time
histogram_quantile(0.95, 
  rate(agent_execution_duration_seconds_bucket[5m])
)
```

---

## 🎯 **RECOMMENDED SETUP BY USE CASE**

### **For Development:**

```bash
# Start all GUIs
./start-all-guis.sh

# Then access:
# - FastAPI Docs: http://localhost:8080/docs (test APIs)
# - n8n: http://localhost:5678 (create workflows)
# - pgAdmin: http://localhost:5050 (check data)
```

### **For Testing:**

```bash
# Just FastAPI Docs
python main.py
# Open: http://localhost:8080/docs

# Test all endpoints interactively
```

### **For Production (K8s):**

```bash
# Grafana for monitoring
https://grafana.marketing.your-domain.com

# n8n for workflows
https://marketing.your-domain.com/n8n

# Lens/K9s for K8s management
```

---

## 📱 **Mobile Access (Optional)**

### **n8n Mobile:**
- n8n has a mobile-friendly UI
- Access http://localhost:5678 from phone (same network)
- Approve workflows on the go

### **Grafana Mobile App:**
- Download: https://grafana.com/grafana/download
- Connect to your Grafana instance
- View dashboards on phone

---

## 🔧 **Advanced: Build Custom Approval UI**

Want a custom Vietnamese content approval dashboard? Here's the tech stack:

### **Recommended Stack:**

```bash
# Frontend
- React + TypeScript
- Tailwind CSS (styling)
- React Query (API calls)
- Zustand (state management)

# Backend
- Already built! (FastAPI endpoints)

# Features to build:
1. Content brief cards with Vietnamese preview
2. Batch approve/reject buttons
3. Feedback form for revisions
4. Video preview player
5. Platform selector
6. Analytics dashboard
```

### **Quick Scaffold:**

```bash
# Create React app
npx create-react-app approval-ui --template typescript
cd approval-ui

# Install dependencies
npm install @tanstack/react-query zustand axios
npm install -D tailwindcss

# Start development
npm start
# Open: http://localhost:3000
```

**Implementation time:** 3-4 days  
**See:** `k8s/base/06-approval-ui.yaml` for deployment config

---

## 🆘 **Troubleshooting GUIs**

### **"Can't access GUI on localhost"**

```bash
# Check if service is running
docker ps | grep <service>

# Check logs
docker logs <service>

# Restart service
docker restart <service>
```

### **"n8n can't connect to AgentOS"**

```bash
# Use host.docker.internal (Mac/Windows)
http://host.docker.internal:8080/api/v1/trends/scan

# Or use 172.17.0.1 (Linux)
http://172.17.0.1:8080/api/v1/trends/scan
```

### **"pgAdmin can't connect to PostgreSQL"**

```bash
# Use host.docker.internal (Mac/Windows)
Host: host.docker.internal

# Or use 172.17.0.1 (Linux)
Host: 172.17.0.1
```

### **"Port already in use"**

```bash
# Find what's using the port
lsof -i :8080

# Kill it
lsof -ti:8080 | xargs kill -9

# Or use different port
```

---

## 📚 **GUI Comparison**

| GUI | Best For | Difficulty | Required |
|-----|----------|------------|----------|
| **FastAPI Docs** | API testing | ⭐ Easy | ✅ Yes |
| **n8n** | Workflows | ⭐⭐ Medium | ✅ Recommended |
| **pgAdmin** | Database | ⭐⭐ Medium | Optional |
| **Grafana** | Monitoring | ⭐⭐⭐ Advanced | Production |
| **Custom UI** | Approvals | ⭐⭐⭐⭐ Hard | Optional |

---

## ✅ **Next Steps**

### **Today:**
```bash
# Start all GUIs
./start-all-guis.sh

# Explore:
1. FastAPI Docs: Test trend scanning
2. n8n: Create first workflow
3. pgAdmin: Browse tables
```

### **This Week:**
```bash
# Build n8n workflows:
1. Daily trend scanner
2. Slack notifications
3. Auto-publishing (when ready)
```

### **Next Month:**
```bash
# Production setup:
1. Deploy to K8s
2. Configure Grafana dashboards
3. Set up alerts
4. (Optional) Build custom Approval UI
```

---

## 🎉 **Summary**

**You have access to:**
- ✅ **FastAPI Docs** - Test APIs (http://localhost:8080/docs)
- ✅ **n8n** - Visual workflows (http://localhost:5678)
- ✅ **pgAdmin** - Database GUI (http://localhost:5050)
- ✅ **Grafana** - Monitoring (K8s deployment)
- ✅ **Prometheus** - Metrics (K8s deployment)

**Start them all:**
```bash
./start-all-guis.sh
```

**Stop them all:**
```bash
./stop-all-guis.sh
```

**Total setup time:** 30 seconds ⚡

---

**Ready?** Run `./start-all-guis.sh` and explore! 🚀
