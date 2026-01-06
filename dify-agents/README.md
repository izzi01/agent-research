# 🤖 Dify Agent DSL Files - Vietnamese Marketing Automation

This directory contains **Dify-compatible DSL files** converted from Python AgentOS agents. You can **import these directly into Dify** to recreate the agents without writing code.

---

## 📦 Files Included

| File | Agent Name | Purpose | Icon |
|------|------------|---------|------|
| `01-trend-monitor-agent.yml` | **TrendMonitor** | Scan TikTok trends | 🔥 |
| `02-content-strategist-agent.yml` | **ContentStrategist** | Create content briefs | 📝 |
| `03-text-creator-agent.yml` | **TextCreator** | Generate social copy | ✍️ |
| `04-orchestrator-workflow.yml` | **Orchestrator** | Full automation workflow | 🚀 |

---

## 🚀 How to Import to Dify

### **Method 1: Import Agent DSL**

1. **Open Dify Studio**
   ```
   http://localhost:3001
   ```

2. **Import Agent**
   - Click **"+ Create App"**
   - Choose **"Import DSL"** (top right)
   - Select file: `01-trend-monitor-agent.yml`
   - Click **"Import"**
   - Agent is now created! ✅

3. **Configure API Endpoints**
   - Update tool URLs to match your AgentOS:
   ```yaml
   # Change this:
   url: "http://host.docker.internal:8080/api/v1/trends/tiktok"
   
   # To your actual URL:
   url: "http://your-agentos-domain.com/api/v1/trends/tiktok"
   ```

4. **Test Agent**
   - Click **"Preview"**
   - Test command: `"Quét xu hướng TikTok"`
   - Verify agent calls the tool

5. **Publish**
   - Click **"Publish"**
   - Get shareable link
   - Share with team!

---

### **Method 2: Import Workflow**

1. **Open Dify Studio**
2. Click **"+ Create App"** → **"Import DSL"**
3. Select: `04-orchestrator-workflow.yml`
4. Workflow nodes are created automatically
5. Connect to your AgentOS backend
6. Test workflow
7. Publish!

---

## 🔧 Configuration Required

After importing, update these settings:

### **1. API URLs**

All agents need your AgentOS backend URL:

```yaml
# In each agent file, update:
url: "http://host.docker.internal:8080"
# To:
url: "http://your-agentos-url:8080"
```

**Quick Find & Replace:**
```bash
# Replace all URLs at once
sed -i 's|host.docker.internal:8080|your-domain.com:8080|g' *.yml
```

---

### **2. LLM Model**

Each agent uses GLM-4 by default. Change if needed:

```yaml
model_config:
  provider: "zhipuai"  # Options: "openai", "anthropic", "zhipuai"
  model: "glm-4-flash"  # Options: "gpt-4o-mini", "claude-3.5-sonnet"
  parameters:
    temperature: 0.7
    max_tokens: 2000
```

**To use OpenAI:**
```yaml
model_config:
  provider: "openai"
  model: "gpt-4o-mini"
```

**To use Claude:**
```yaml
model_config:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
```

---

### **3. Environment Variables**

Some agents use variables. Set in Dify:

```yaml
variables:
  - name: "min_relevance_score"
    default: 0.6  # Change to your preference
  
  - name: "product_categories"
    default: ["beauty", "fashion", "food"]  # Add your categories
```

---

## 📋 Agent Details

### **1. TrendMonitor Agent** 🔥

**Purpose:** Scan TikTok for viral trends

**Tools:**
- `fetch_tiktok_trends` - GET trends from TikTok API
- `analyze_trend_relevance` - Calculate relevance score
- `store_trend` - Save to database

**Example Commands:**
```
"Quét xu hướng TikTok mới nhất"
"Tìm xu hướng beauty có tiềm năng cao"
"Phân tích hashtag #BeautyHacks"
```

**Expected Response:**
```json
{
  "hashtag": "#BeautyHacks",
  "views": 67000000,
  "engagement_rate": 9.2,
  "growth_rate": 320,
  "relevance_score": 0.85,
  "recommended_action": "create_content"
}
```

---

### **2. ContentStrategist Agent** 📝

**Purpose:** Create Vietnamese content briefs from trends

**Tools:**
- `search_products` - Find matching products
- `generate_vietnamese_hashtags` - Create hashtags
- `create_content_brief` - Generate full brief

**Example Commands:**
```
"Tạo content brief cho trend #BeautyHacks"
"Match xu hướng này với sản phẩm beauty"
"Gợi ý nội dung cho sản phẩm son môi"
```

**Expected Response:**
```json
{
  "trend_id": "#BeautyHacks",
  "vietnamese_hook": "Chị em ơi! Trend làm đẹp này đang gây bão...",
  "content_angle": "Product Review + Tutorial",
  "hashtags": ["#BeautyHacks", "#LàmĐẹp", ...],
  "success_metrics": {
    "target_views": 50000,
    "expected_revenue_vnd": 25900000
  }
}
```

---

### **3. TextCreator Agent** ✍️

**Purpose:** Generate platform-specific Vietnamese copy

**Tools:**
- `generate_facebook_copy` - Facebook posts
- `generate_tiktok_copy` - TikTok captions
- `generate_shopee_copy` - Shopee descriptions
- `validate_copy` - Check requirements

**Example Commands:**
```
"Tạo Facebook copy cho brief này"
"Viết TikTok caption cho sản phẩm son môi"
"Tạo 3 A/B variants cho Facebook"
```

**Expected Response:**
```json
{
  "platform": "facebook",
  "copy": {
    "body": "Chị em ơi! Deal hot đây! 🔥...",
    "hashtags": ["#SaleSốc", "#SonLì"],
    "call_to_action": "Inbox shop để đặt hàng!"
  },
  "metadata": {
    "character_count": 156,
    "emoji_count": 3,
    "hashtag_count": 5
  }
}
```

---

### **4. Orchestrator Workflow** 🚀

**Purpose:** Full automation from trend → approval → publish

**Flow:**
```
Start
  ↓
Scan TikTok Trends
  ↓
Create Content Briefs (for each trend)
  ↓
Generate Copy (for each brief)
  ↓
Submit for Approval
  ↓
Wait for Human Decision
  ↓
Publish Approved Content
  ↓
End (Summary Report)
```

**Schedule:** Daily at 8 AM Vietnam time (GMT+7)

---

## 🎯 Quick Start Guide

### **Step 1: Import All 3 Agents** (10 min)

```bash
# Import in this order:
1. 01-trend-monitor-agent.yml
2. 02-content-strategist-agent.yml
3. 03-text-creator-agent.yml
```

### **Step 2: Update AgentOS URLs** (2 min)

In each agent, change:
```yaml
url: "http://host.docker.internal:8080"
# To your actual URL
```

### **Step 3: Test Each Agent** (5 min)

```
TrendMonitor: "Quét xu hướng beauty"
ContentStrategist: "Tạo brief cho trend #BeautyHacks"
TextCreator: "Tạo Facebook copy"
```

### **Step 4: Import Workflow** (5 min)

```bash
# Import:
04-orchestrator-workflow.yml

# Configure schedule:
Daily at 8 AM Vietnam time
```

### **Step 5: Run Full Automation** (1 min)

Click **"Run"** → Workflow executes all steps automatically!

---

## 🔄 Alternative: Manual Agent Creation

If DSL import doesn't work, create agents manually:

### **TrendMonitor (Manual)**

1. Create Agent
2. Add HTTP Tool:
   ```
   Name: fetch_tiktok_trends
   URL: http://your-backend/api/v1/trends/tiktok
   Method: GET
   ```
3. Add Python Code Tool (from DSL file)
4. Set Instructions (copy from DSL)
5. Test!

---

## 📊 Comparison: Python vs Dify

| Feature | Python Agents | Dify Agents | Winner |
|---------|---------------|-------------|--------|
| **Setup Time** | 2 hours | 10 min | ✅ Dify |
| **Code Required** | ~500 lines | 0 lines | ✅ Dify |
| **Customization** | High | Medium | Python |
| **Visual Debugging** | No | ✅ Yes | ✅ Dify |
| **Team Collaboration** | Hard | ✅ Easy | ✅ Dify |
| **Deployment** | Docker | ✅ 1-click | ✅ Dify |
| **Maintenance** | High | ✅ Low | ✅ Dify |

**Recommendation:** Use Dify for faster iteration and easier management!

---

## 🆘 Troubleshooting

### **Import Failed**

**Error:** "Invalid DSL format"

**Solution:**
```bash
# Check YAML syntax
python -m yaml 01-trend-monitor-agent.yml

# Validate with online tool:
https://www.yamllint.com/
```

---

### **Agent Can't Call Tools**

**Error:** "Tool execution failed"

**Solution:**
1. Check AgentOS is running:
   ```bash
   curl http://localhost:8080/health
   ```

2. Update tool URLs in agent
3. Test tool individually in Dify

---

### **Copy Generation Fails**

**Error:** "Character limit exceeded"

**Solution:**
Update in `03-text-creator-agent.yml`:
```yaml
parameters:
  max_tokens: 3000  # Increase this
```

---

## 📚 Resources

- **Dify DSL Docs:** https://docs.dify.ai/guides/workflow/dsl
- **Agent Import Guide:** https://docs.dify.ai/guides/agent/import-export
- **Workflow Tutorial:** https://docs.dify.ai/guides/workflow

---

## ✅ Verification Checklist

After importing, verify:

- [ ] All 3 agents created in Dify
- [ ] Agent icons show correctly (🔥, 📝, ✍️)
- [ ] Tools are configured with correct URLs
- [ ] LLM model is selected
- [ ] Test commands work
- [ ] Agents can call AgentOS backend
- [ ] Orchestrator workflow connects all agents
- [ ] Schedule is set (if using workflow)

---

## 🎉 Success!

You've successfully converted Python agents to Dify!

**Next Steps:**
1. Test each agent individually
2. Import orchestrator workflow
3. Run full automation
4. Share with team
5. Monitor results in Dify dashboard

**Questions?** Check `/home/cid/projects-personal/agent-research/DIFY-GETTING-STARTED.md`

---

**Made with ❤️ for Vietnamese content creators**

**Last Updated:** 2025-12-28
