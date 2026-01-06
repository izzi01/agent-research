# Migration Guide: Next.js + CopilotKit → Dify

## 🎯 Why Migrate to Dify?

**Current Issues:**
- Complex Next.js + CopilotKit setup
- Requires maintaining frontend code
- OpenAI API dependency
- Multiple deployment targets

**Dify Benefits:**
- ✅ Built-in chat UI (no Next.js needed!)
- ✅ Visual workflow builder
- ✅ Multi-LLM support (OpenAI, Claude, GLM-4, local models)
- ✅ HTTP API tools (call your FastAPI directly)
- ✅ Human-in-the-loop workflows
- ✅ Single deployment (Docker Compose)

---

## 📊 Architecture Comparison

### Current (Complex)
```
┌─────────────────┐
│   Next.js UI    │ (approval-ui/)
│   + CopilotKit  │
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────┐
│ FastAPI Backend │ (agentos/)
│   AgentOS       │
└─────────────────┘
```

### Proposed (Simple)
```
┌─────────────────┐
│   Dify Platform │ ← Built-in UI + Workflows
└────────┬────────┘
         │ HTTP API Calls
         ↓
┌─────────────────┐
│ FastAPI Backend │ (keep existing!)
│   AgentOS       │
└─────────────────┘
```

**What you keep:**
- ✅ AgentOS FastAPI backend (no changes!)
- ✅ All Python agents (TrendMonitor, ContentStrategist, TextCreator)
- ✅ Database, workflows, business logic

**What you replace:**
- ❌ Next.js approval-ui → Dify Chat UI
- ❌ CopilotKit → Dify Agent
- ❌ Custom API routes → Dify HTTP Tool

---

## 🚀 Step-by-Step Migration

### **Step 1: Install Dify (5 minutes)**

```bash
# Clone Dify
cd /home/cid/projects-personal/agent-research
git clone https://github.com/langgenius/dify.git

# Start Dify with Docker Compose
cd dify/docker
docker-compose up -d

# Access Dify
# Open: http://localhost:3001
```

**Services Started:**
- Dify Web UI: http://localhost:3001
- Dify API: http://localhost:5001
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

### **Step 2: Configure AgentOS API in Dify**

1. **Open Dify Studio** → http://localhost:3001

2. **Create New App** → Choose "Agent" type

3. **Add API Tools**:

   **Tool 1: Get Pending Briefs**
   ```yaml
   Name: get_pending_briefs
   Method: GET
   URL: http://host.docker.internal:8080/api/v1/approvals/pending
   Description: Lấy danh sách nội dung đang chờ phê duyệt
   
   Response Schema:
   {
     "count": "number",
     "briefs": "array"
   }
   ```

   **Tool 2: Approve Brief**
   ```yaml
   Name: approve_brief
   Method: POST
   URL: http://host.docker.internal:8080/api/v1/approvals/submit
   Headers:
     Content-Type: application/json
   
   Body Parameters:
   - brief_id: string (required)
   - approved: boolean (true)
   - feedback: string (optional)
   
   Description: Phê duyệt một bản dự thảo nội dung
   ```

   **Tool 3: Reject Brief**
   ```yaml
   Name: reject_brief
   Method: POST
   URL: http://host.docker.internal:8080/api/v1/approvals/submit
   Headers:
     Content-Type: application/json
   
   Body Parameters:
   - brief_id: string (required)
   - approved: boolean (false)
   - feedback: string (required)
   
   Description: Từ chối một bản dự thảo nội dung
   ```

   **Tool 4: Scan Trends**
   ```yaml
   Name: scan_trends
   Method: POST
   URL: http://host.docker.internal:8080/api/v1/trends/scan
   Headers:
     Content-Type: application/json
   
   Body Parameters:
   - product_categories: array of strings
   - min_relevance_score: number (default: 0.6)
   - max_briefs: number (default: 10)
   
   Description: Quét xu hướng TikTok và tạo nội dung
   ```

---

### **Step 3: Configure Agent Prompt**

In Dify Agent → **Instructions**:

```
Bạn là trợ lý AI chuyên phê duyệt nội dung tiếp thị tiếng Việt cho TikTok.

NHIỆM VỤ CỦA BẠN:
1. Hiển thị các bản dự thảo nội dung đang chờ phê duyệt
2. Phân tích chất lượng nội dung tiếng Việt
3. Đề xuất phê duyệt hoặc từ chối dựa trên:
   - Chất lượng hook tiếng Việt (độ dài, hấp dẫn)
   - Số lượng hashtag (tối ưu: 4-8 hashtags)
   - Dự báo lượt xem (cao: >40K, trung bình: 20-40K, thấp: <20K)
   - Tiềm năng doanh thu (VNĐ)
4. Hỗ trợ phê duyệt hàng loạt nhiều nội dung cùng lúc

QUY TẮC PHÂN TÍCH:
- Hook ngắn (<50 ký tự) → "⚠️ Cần cải thiện hook - quá ngắn"
- Lượt xem dự kiến >40,000 → "✅ ĐỀ XUẤT PHÊ DUYỆT - Tiềm năng rất cao"
- Lượt xem 20,000-40,000 → "⭐ Tiềm năng trung bình - cân nhắc phê duyệt"
- Lượt xem <20,000 → "📉 Tiềm năng thấp - nên từ chối"
- Hashtag <3 → "⚠️ Cần thêm hashtag"
- Hashtag >10 → "⚠️ Quá nhiều hashtag"

CÁCH TRẢ LỜI:
- Luôn hiển thị số liệu cụ thể (lượt xem, doanh thu VNĐ, số hashtag)
- Đưa ra lý do rõ ràng khi đề xuất
- Sử dụng tiếng Việt thân thiện, chuyên nghiệp
- Khi người dùng hỏi "cho tôi xem nội dung", gọi get_pending_briefs
- Khi người dùng nói "phê duyệt tất cả tiềm năng cao", lọc brief có >40K views và approve từng cái

CÔNG CỤ CÓ SẴN:
- get_pending_briefs: Lấy danh sách nội dung đang chờ
- approve_brief: Phê duyệt một nội dung
- reject_brief: Từ chối một nội dung
- scan_trends: Quét xu hướng mới từ TikTok

LƯU Ý:
- Luôn kiểm tra brief_id trước khi approve/reject
- Yêu cầu feedback khi từ chối
- Đề xuất cải thiện nếu nội dung gần đạt yêu cầu
```

---

### **Step 4: Configure LLM Model**

Dify supports multiple models:

**Option 1: GLM-4 (Chinese, cheap)**
```
Provider: Zhipu AI
Model: glm-4-flash
API Key: your_glm_api_key
```

**Option 2: OpenAI (best quality)**
```
Provider: OpenAI
Model: gpt-4-turbo
API Key: your_openai_key
```

**Option 3: Local Model (free)**
```
Provider: Ollama (run locally)
Model: llama3.1:8b or qwen2.5:14b
```

**Option 4: Claude (Anthropic)**
```
Provider: Anthropic
Model: claude-3.5-sonnet
API Key: your_anthropic_key
```

---

### **Step 5: Test the Agent**

1. **Open Agent Chat** → Click "Publish" → "Run"

2. **Test Commands**:
   ```
   User: "Cho tôi xem các nội dung đang chờ phê duyệt"
   → Agent calls get_pending_briefs
   
   User: "Phê duyệt brief_123"
   → Agent calls approve_brief with brief_id="brief_123"
   
   User: "Từ chối brief_456 vì hook chưa hấp dẫn"
   → Agent calls reject_brief with feedback
   
   User: "Quét xu hướng beauty và fashion"
   → Agent calls scan_trends
   
   User: "Phê duyệt tất cả nội dung có tiềm năng cao"
   → Agent filters briefs >40K views, approves all
   ```

---

### **Step 6: Create Dashboard View (Optional)**

Dify also has a **Workflow** mode for dashboards:

1. Create **Workflow** (not Agent)
2. Add **HTTP Request** nodes
3. Add **Variable** nodes for filters
4. Add **LLM** node for analysis
5. Create **API endpoint** for the workflow
6. Build simple HTML dashboard that calls Dify API

---

## 🎨 Dify UI Features You Get for Free

### **Built-in Chat Interface**
- ✅ Message history
- ✅ Streaming responses
- ✅ File uploads
- ✅ Voice input
- ✅ Mobile responsive

### **Agent Features**
- ✅ Tool calling (HTTP, database, plugins)
- ✅ Knowledge base (RAG)
- ✅ Context memory
- ✅ Multi-turn conversations

### **Workflow Features**
- ✅ Visual flow builder
- ✅ Conditional logic
- ✅ Variables & parameters
- ✅ Error handling
- ✅ Debugging tools

### **Analytics**
- ✅ Token usage tracking
- ✅ Conversation logs
- ✅ Cost monitoring
- ✅ Performance metrics

---

## 📊 Feature Comparison

| Feature | Current (Next.js) | Dify |
|---------|------------------|------|
| **Chat UI** | Custom build | ✅ Built-in |
| **AI Integration** | CopilotKit | ✅ Native |
| **Multi-LLM** | OpenAI only | ✅ 10+ providers |
| **No-code Tools** | ❌ None | ✅ Visual builder |
| **API Testing** | Postman | ✅ Built-in |
| **Deployment** | Vercel + Docker | ✅ Single Docker |
| **Setup Time** | 2 days | ✅ 30 minutes |
| **Maintenance** | High | ✅ Low |

---

## 💰 Cost Comparison

### Current Stack
```
OpenAI API (CopilotKit): $0.03/1K tokens (gpt-4)
Next.js Hosting: $20/month (Vercel Pro)
Docker Registry: $5/month
Total: ~$25-50/month
```

### Dify + Local Model
```
Dify: Free (self-hosted)
Ollama (local): Free
AgentOS Backend: $0 (existing)
Total: $0/month
```

### Dify + GLM-4
```
Dify: Free (self-hosted)
GLM-4-Flash: $0.001/1K tokens (30x cheaper than GPT-4!)
AgentOS Backend: $0 (existing)
Total: ~$2-5/month
```

---

## 🔄 Migration Checklist

- [ ] Install Dify with Docker Compose
- [ ] Create Agent app in Dify
- [ ] Configure 4 HTTP tools (get, approve, reject, scan)
- [ ] Set Vietnamese prompt
- [ ] Choose LLM model (GLM-4 recommended)
- [ ] Test all API calls
- [ ] Publish agent
- [ ] Get shareable link
- [ ] Stop Next.js approval-ui
- [ ] Remove approval-ui from deployments
- [ ] Update documentation

**Time Estimate:** 1-2 hours (vs. 2 days for Next.js setup!)

---

## 🚀 RAGFlow Alternative

If you prefer **RAGFlow** (better for document-heavy workflows):

### When to Use RAGFlow
- ✅ Need advanced RAG (Retrieval Augmented Generation)
- ✅ Working with lots of documents/PDFs
- ✅ Need chunking strategies
- ✅ Multiple knowledge bases

### When to Use Dify
- ✅ **Agent-based workflows** (your use case!)
- ✅ API integrations
- ✅ Simple chat interface
- ✅ Visual workflow builder

**Recommendation for your project:** **Use Dify** (better fit for approval workflows)

---

## 📝 Quick Start Commands

```bash
# 1. Stop Next.js UI
cd /home/cid/projects-personal/agent-research/approval-ui
# Ctrl+C if running

# 2. Clone and start Dify
cd /home/cid/projects-personal/agent-research
git clone https://github.com/langgenius/dify.git
cd dify/docker
docker-compose up -d

# 3. Keep AgentOS running
cd /home/cid/projects-personal/agent-research/agentos
source .venv/bin/activate
python main.py

# 4. Configure Dify
# Open http://localhost:3001
# Create account
# Create Agent
# Add tools (see Step 2 above)
# Test!
```

---

## 🎯 Final Recommendation

**REPLACE:**
```
approval-ui/ (Next.js + CopilotKit)
  - 11 TypeScript files
  - 1000+ lines of code
  - npm dependencies
  - Custom UI components
  - OpenAI API required
```

**WITH:**
```
Dify Agent
  - Visual configuration
  - No code needed
  - Built-in UI
  - Multi-LLM support
  - 30 min setup
```

**KEEP:**
```
agentos/ (FastAPI backend)
  - All Python agents
  - Business logic
  - Database
  - No changes needed!
```

---

## 🔗 Resources

- **Dify Docs**: https://docs.dify.ai/
- **Dify GitHub**: https://github.com/langgenius/dify
- **RAGFlow**: https://github.com/infiniflow/ragflow
- **GLM-4 API**: https://open.bigmodel.cn/

---

**VERDICT:** ✅ **YES, migrate to Dify!** Much easier to maintain and iterate.
