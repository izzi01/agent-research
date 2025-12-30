# 🎯 GETTING STARTED - Vietnamese Marketing Automation

## ⚡ TWO WAYS TO START

### **OPTION A: INSTANT TEST (2 Minutes)** 👈 START HERE ⚡

No API keys, no database, just test immediately!

```bash
cd /home/cid/projects-personal/agent-research/agentos
./start.sh
```

**Or manually:**
```bash
# 1. Create venv + install deps (30 seconds with UV!)
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 2. Run test (uses mock data)
python test_textcreator.py
```

✅ **You'll see Vietnamese content generated for Facebook, TikTok, and Shopee!**

---

### **OPTION B: FULL SETUP (30 Minutes)**

Get the complete system running with real APIs.

#### **What You'll Need:**

1. **Z.AI GLM API Key** (15 minutes to get)
   - Visit: https://open.bigmodel.cn/
   - Sign up → Create API key
   - **Cost:** ~$10-15/month

2. **PostgreSQL Database** (5 minutes)
   ```bash
   docker run -d \
     --name postgres-pgvector \
     -e POSTGRES_USER=agno \
     -e POSTGRES_PASSWORD=changeme123 \
     -e POSTGRES_DB=marketing_automation \
     -p 5432:5432 \
     pgvector/pgvector:pg16
   ```

3. **Configure Environment** (2 minutes)
   ```bash
   nano .env
   # Replace: ZHIPU_API_KEY=YOUR_GLM_API_KEY_HERE
   # With your actual key
   ```

4. **Start Server** (1 minute)
   ```bash
   python main.py
   ```

---

## 📋 COMPLETE REQUIREMENTS CHECKLIST

### **Already Have (✅ Verified):**
- [x] Python 3.12.3 (requirement: 3.8+)
- [x] UV package manager
- [x] Project code (cloned)
- [x] Environment template (.env.example)

### **Need to Install:**
- [ ] Python dependencies: `uv pip install -r requirements.txt` (~30 seconds)
  - ~500MB download

### **Need to Obtain (For Full Features):**

#### **Required (Core Functionality):**
- [ ] **Z.AI GLM API Key** 
  - Get from: https://open.bigmodel.cn/
  - Time: 15 minutes
  - Cost: ~$10-15/month
  - Used for: Vietnamese content generation

- [ ] **PostgreSQL Database**
  - Option A: Docker (5 minutes) - FREE
  - Option B: DigitalOcean Managed - $15/month
  - Used for: Agent storage, vector search

#### **Optional (Add Later):**
- [ ] **TickerTrends API** - $80/month (for real TikTok trends)
- [ ] **Vbee TTS** - FREE tier (for Vietnamese voiceover)
- [ ] **Video Tools** - $144.70/month (for video generation)
  - Simplified: $64/month
  - HeyGen: $64/month
  - D-ID: $4.70/month
  - Runway: $12/month
- [ ] **Platform APIs** - FREE (for publishing)
  - Facebook Graph API
  - TikTok Content Posting API
  - Shopee Open API
  - YouTube Data API

---

## 💰 COST BREAKDOWN

### **Minimum to Start:**
```
PostgreSQL (Docker)     $0 (local)
GLM-4.6 API            $10-15/month
─────────────────────────────────
TOTAL:                 $10-15/month
```

### **Full System (All Features):**
```
Infrastructure          $80/month (Kubernetes)
GLM-4.6 API            $10-15/month
TickerTrends           $80/month
Video Tools            $144.70/month
Vbee TTS               $0 (FREE tier)
─────────────────────────────────
TOTAL:                 $344.70/month
```

**Budget:** $500/month → **$155 buffer (31%)**

---

## 🎯 RECOMMENDED START PATH

### **Day 1: Test Locally (Today!)** ⚡

```bash
# This works RIGHT NOW:
cd /home/cid/projects-personal/agent-research/agentos
./start.sh
# Choose 'y' to run test
```

**Goal:** See Vietnamese content generated, verify quality

**Time:** 2 minutes ⚡

**Cost:** $0

---

### **Day 2: Get API Keys**

1. Sign up for Z.AI GLM: https://open.bigmodel.cn/
2. Create API key
3. Update `.env` file:
   ```bash
   ZHIPU_API_KEY=your-actual-key-here
   ```

**Goal:** Enable real AI generation (not mock data)

**Time:** 15-20 minutes

**Cost:** $10-15/month

---

### **Day 3: Start Full Server**

```bash
# 1. Start PostgreSQL
docker run -d --name postgres-pgvector \
  -e POSTGRES_USER=agno \
  -e POSTGRES_PASSWORD=changeme123 \
  -e POSTGRES_DB=marketing_automation \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# 2. Start API server
python main.py

# 3. Test API
curl http://localhost:8080/health
```

**Goal:** Full API server running locally

**Time:** 10-15 minutes

**Cost:** $0 (using local PostgreSQL)

---

### **Day 4-5: Deploy to Production (Optional)**

Follow `README-DEPLOYMENT.md` to deploy to Kubernetes.

**Goal:** Production-ready system with monitoring

**Time:** 30-60 minutes

**Cost:** +$80/month (cloud infrastructure)

---

## 🚀 QUICK COMMANDS REFERENCE

### **Test Without Any Setup:**
```bash
./start.sh
```

### **Start Development Server:**
```bash
# 1. Start PostgreSQL (one-time)
docker run -d --name postgres-pgvector \
  -e POSTGRES_USER=agno \
  -e POSTGRES_PASSWORD=changeme123 \
  -e POSTGRES_DB=marketing_automation \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# 2. Start API server
python main.py
```

### **Test API Endpoints:**
```bash
# Health check
curl http://localhost:8080/health

# Scan trends
curl -X POST http://localhost:8080/api/v1/trends/scan \
  -H "Content-Type: application/json" \
  -d '{"product_categories": ["beauty"], "min_relevance_score": 0.6, "max_briefs": 3}'

# Generate copy
curl -X POST "http://localhost:8080/api/v1/content/generate-copy?brief_id=%23BeautyHacks&platforms=facebook"
```

### **Interactive API Docs:**
```bash
# Start server, then visit:
open http://localhost:8080/docs
```

---

## 🆘 COMMON ISSUES & SOLUTIONS

### **"Module not found" error**
```bash
# Solution: Install dependencies
source .venv/bin/activate  # If using venv
uv pip install -r requirements.txt
```

### **"Database connection failed"**
```bash
# Solution: Start PostgreSQL
docker run -d --name postgres-pgvector \
  -e POSTGRES_USER=agno \
  -e POSTGRES_PASSWORD=changeme123 \
  -e POSTGRES_DB=marketing_automation \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# Verify it's running
docker ps | grep postgres
```

### **"Invalid API key"**
```bash
# Solution: Check .env file
cat .env | grep ZHIPU_API_KEY

# Should show actual key, not placeholder:
# ZHIPU_API_KEY=glm-xxxxxxxxxxxxx  ✅
# ZHIPU_API_KEY=YOUR_GLM_API_KEY_HERE  ❌
```

### **"Port already in use"**
```bash
# Solution: Kill existing process
lsof -ti:8080 | xargs kill -9

# Or use different port
uvicorn main:app --port 8081
```

---

## 📚 DOCUMENTATION MAP

**Start Here:**
- 📄 `GETTING-STARTED.md` (this file) - What you need to begin
- 📄 `agentos/QUICK-START.md` - Step-by-step setup with UV
- 📄 `GUI-TOOLS-GUIDE.md` - **Visual tools for easy management** 🖥️

**Understanding the System:**
- 📄 `AGNO-IMPLEMENTATION-SUMMARY.md` - What has been built
- 📄 `agentos/README.md` - Architecture and technical details

**Running Locally:**
- 📄 `agentos/HOW-TO-RUN.md` - Detailed running instructions
- 📄 `agentos/test_textcreator.py` - Test script (no server needed)

**Deploying to Production:**
- 📄 `README-DEPLOYMENT.md` - Complete Kubernetes guide
- 📄 `KUBERNETES-DEPLOYMENT-SUMMARY.md` - Infrastructure overview

**Specific Features:**
- 📄 `TEXTCREATOR-SUMMARY.md` - Platform-specific copy generation
- 📄 `GLM-INTEGRATION-SUMMARY.md` - GLM-4.6 model details
- 📄 `UV-VS-PIP.md` - UV performance benchmarks

---

## ✅ YOUR NEXT ACTION

**Run this command RIGHT NOW:**

```bash
cd /home/cid/projects-personal/agent-research/agentos
./start.sh
```

This will:
1. ✅ Check your Python version
2. ✅ Install UV if needed
3. ✅ Create virtual environment (<1 second)
4. ✅ Install dependencies (~30 seconds) ⚡
5. ✅ Ask if you want to run test script
6. ✅ Show Vietnamese content generation!

**Time:** 2 minutes ⚡

**Cost:** $0

**Result:** You'll see the system working immediately! 🎉

---

## 🎯 SUCCESS CRITERIA

### **You're ready when you can:**
- [x] Run `./start.sh` and see Vietnamese output ⚡
- [ ] Start API server with `python main.py`
- [ ] Access http://localhost:8080/docs
- [ ] Generate content via API calls
- [ ] See metrics at http://localhost:8080/metrics

### **You have full system when:**
- [ ] PostgreSQL running with pgvector
- [ ] GLM API key configured
- [ ] All 3 agents working (TrendMonitor, ContentStrategist, TextCreator)
- [ ] REST API responding
- [ ] Prometheus metrics collecting

---

**Ready?** Run `./start.sh` and let's begin! ⚡🚀
