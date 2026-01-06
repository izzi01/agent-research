# 🚀 Getting Started with Dify - Vietnamese Content Approval System

**Project:** Vietnamese Marketing Automation  
**Backend:** AgentOS (FastAPI) - Already Running  
**Frontend:** Dify Agent (No-Code UI)

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Access Dify](#access-dify)
3. [Create Your First Agent](#create-your-first-agent)
4. [Configure AgentOS API Tools](#configure-agentos-api-tools)
5. [Set Up Vietnamese Prompt](#set-up-vietnamese-prompt)
6. [Configure LLM Model](#configure-llm-model)
7. [Test Your Agent](#test-your-agent)
8. [Advanced Features](#advanced-features)
9. [Deployment & Sharing](#deployment--sharing)
10. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites ✅

Before starting, ensure you have:

- ✅ Dify deployed and running
- ✅ AgentOS backend running at `http://localhost:8080`
- ✅ An LLM API key (OpenAI, GLM-4, or local Ollama)
- ✅ Web browser (Chrome, Firefox, or Safari)

**Test Backend Connection:**
```bash
# Check if AgentOS is running
curl http://localhost:8080/health

# Expected response:
# {"status":"healthy","timestamp":"2025-12-28T..."}
```

---

## 2. Access Dify 🌐

### **Option A: Local Deployment**
```
URL: http://localhost:3001
```

### **Option B: Cloud Deployment**
```
URL: https://your-dify-domain.com
```

### **First Time Setup:**

1. **Open Dify in browser**
2. **Create admin account:**
   - Email: your-email@example.com
   - Password: (choose a strong password)
   - Company: (optional)
3. **Click "Create Workspace"**
4. **You're in!** 🎉

---

## 3. Create Your First Agent 🤖

### **Step 1: Create New App**

1. Click **"+ Create App"** (top right)
2. Choose **"Agent"** (not Chatbot or Workflow)
3. Name: `Vietnamese Content Approval Assistant`
4. Description: `AI agent for approving Vietnamese TikTok content`
5. Icon: 🎨 (optional)
6. Click **"Create"**

### **Step 2: Agent Type**

- Select: **"Agent"** mode
- This allows the AI to call tools/APIs automatically

---

## 4. Configure AgentOS API Tools 🔧

Now we'll add 4 API tools to connect Dify with your AgentOS backend.

### **How to Add a Tool:**

1. In Agent Studio, scroll to **"Tools"** section
2. Click **"+ Add Tool"**
3. Choose **"Custom API"**
4. Fill in the details below

---

### **Tool 1: Get Pending Briefs** 📋

**Purpose:** Fetch all content briefs waiting for approval

```yaml
Tool Name: get_pending_briefs
Description: Lấy danh sách các nội dung đang chờ phê duyệt từ AgentOS
Method: GET
URL: http://host.docker.internal:8080/api/v1/approvals/pending

Headers:
  Content-Type: application/json

Parameters: (none)

Response Schema:
{
  "count": "number",
  "briefs": "array"
}

Test Example:
# Click "Test" button to verify connection
# Expected: Returns list of pending briefs
```

**💡 Note:** Use `host.docker.internal` if Dify is in Docker, or `localhost` if running natively.

---

### **Tool 2: Approve Brief** ✅

**Purpose:** Approve a content brief by ID

```yaml
Tool Name: approve_brief
Description: Phê duyệt một bản dự thảo nội dung
Method: POST
URL: http://host.docker.internal:8080/api/v1/approvals/submit

Headers:
  Content-Type: application/json

Body Parameters:
  - brief_id (string, required): ID của bản dự thảo
  - approved (boolean, required): true
  - feedback (string, optional): Nhận xét

Body Template:
{
  "brief_id": "{{brief_id}}",
  "approved": true,
  "feedback": "{{feedback}}"
}

Response Schema:
{
  "brief_id": "string",
  "approved": "boolean",
  "approved_at": "string"
}

Test Example:
{
  "brief_id": "trend_123",
  "approved": true,
  "feedback": "Nội dung tốt"
}
```

---

### **Tool 3: Reject Brief** ❌

**Purpose:** Reject a content brief with feedback

```yaml
Tool Name: reject_brief
Description: Từ chối một bản dự thảo nội dung
Method: POST
URL: http://host.docker.internal:8080/api/v1/approvals/submit

Headers:
  Content-Type: application/json

Body Parameters:
  - brief_id (string, required): ID của bản dự thảo
  - approved (boolean, required): false
  - feedback (string, required): Lý do từ chối

Body Template:
{
  "brief_id": "{{brief_id}}",
  "approved": false,
  "feedback": "{{feedback}}"
}

Response Schema:
{
  "brief_id": "string",
  "approved": "boolean",
  "approved_at": "string"
}

Test Example:
{
  "brief_id": "trend_456",
  "approved": false,
  "feedback": "Hook chưa hấp dẫn, cần viết lại"
}
```

---

### **Tool 4: Scan Trends** 🔍

**Purpose:** Trigger TikTok trend scanning and content generation

```yaml
Tool Name: scan_trends
Description: Quét xu hướng TikTok và tạo bản dự thảo nội dung mới
Method: POST
URL: http://host.docker.internal:8080/api/v1/trends/scan

Headers:
  Content-Type: application/json

Body Parameters:
  - product_categories (array, required): Danh mục sản phẩm ["beauty", "fashion", "food"]
  - min_relevance_score (number, optional): Điểm liên quan tối thiểu (0.0-1.0)
  - max_briefs (number, optional): Số lượng brief tối đa

Body Template:
{
  "product_categories": {{product_categories}},
  "min_relevance_score": {{min_relevance_score}},
  "max_briefs": {{max_briefs}}
}

Response Schema:
{
  "workflow_id": "string",
  "status": "string",
  "trends_discovered": "number",
  "content_briefs_created": "number",
  "briefs": "array"
}

Test Example:
{
  "product_categories": ["beauty", "fashion"],
  "min_relevance_score": 0.6,
  "max_briefs": 5
}
```

---

## 5. Set Up Vietnamese Prompt 🇻🇳

### **Navigate to Instructions**

1. In Agent Studio, find **"Instructions"** or **"Prompt"** section
2. Paste the following Vietnamese prompt:

```
Bạn là trợ lý AI chuyên phê duyệt nội dung tiếp thị tiếng Việt cho TikTok.

## VAI TRÒ CỦA BẠN
Bạn giúp nhà tiếp thị phê duyệt hoặc từ chối các bản dự thảo nội dung TikTok được tạo tự động bởi hệ thống AI.

## NHIỆM VỤ CHÍNH

1. **Xem danh sách nội dung:**
   - Khi người dùng hỏi "cho tôi xem nội dung" hoặc "nội dung nào đang chờ"
   - Gọi công cụ `get_pending_briefs`
   - Hiển thị danh sách rõ ràng, dễ đọc

2. **Phân tích chất lượng:**
   - Đánh giá hook tiếng Việt (độ hấp dẫn, độ dài)
   - Kiểm tra số lượng hashtag (tối ưu: 4-8 hashtags)
   - Xem xét dự báo lượt xem
   - Đánh giá tiềm năng doanh thu

3. **Đưa ra đề xuất:**
   - Dựa trên tiêu chí phân tích
   - Luôn giải thích lý do
   - Cung cấp số liệu cụ thể

4. **Thực hiện hành động:**
   - Phê duyệt: Gọi `approve_brief` với brief_id
   - Từ chối: Gọi `reject_brief` với brief_id và lý do
   - Quét xu hướng mới: Gọi `scan_trends`

## QUY TẮC PHÂN TÍCH

### Đánh giá Hook (Vietnamese Hook):
- ❌ Hook < 30 ký tự: "Quá ngắn, cần mở rộng"
- ✅ Hook 30-80 ký tự: "Độ dài tốt"
- ⚠️ Hook > 100 ký tự: "Quá dài, nên rút gọn"
- ❌ Hook không có dấu hỏi/cảm thán: "Thiếu sức hút"
- ✅ Hook có yếu tố gây tò mò: "Hấp dẫn"

### Đánh giá Hashtags:
- ❌ Hashtag < 3: "Quá ít, cần thêm hashtag"
- ✅ Hashtag 4-8: "Số lượng tối ưu"
- ⚠️ Hashtag > 10: "Quá nhiều, nên giảm"

### Đánh giá Tiềm Năng (Target Views):
- 🔥 > 40,000 views: "TIỀM NĂNG CAO - Đề xuất PHÊ DUYỆT"
- ⭐ 20,000 - 40,000 views: "Tiềm năng trung bình - Cân nhắc"
- 📉 < 20,000 views: "Tiềm năng thấp - Nên từ chối"

### Đánh giá Doanh Thu:
- 💰 > 2,000,000 VNĐ: "Doanh thu cao"
- 💵 500,000 - 2,000,000 VNĐ: "Doanh thu trung bình"
- 📊 < 500,000 VNĐ: "Doanh thu thấp"

## CÁCH TRẢ LỜI

### Khi hiển thị nội dung:
```
📋 DANH SÁCH NỘI DUNG ĐANG CHỜ PHÊ DUYỆT:

1️⃣ ID: brief_123
   📝 Hook: "Bí quyết giảm cân sau 7 ngày mà không cần ăn kiêng!"
   📊 Dự kiến: 45,000 lượt xem | 3.5% tương tác | 2.5M VNĐ
   🏷️ Hashtags: #giamcan #beauty #skincare (7 tags)
   ✅ ĐỀ XUẤT: PHÊ DUYỆT - Tiềm năng cao

2️⃣ ID: brief_456
   📝 Hook: "Skincare"
   📊 Dự kiến: 15,000 lượt xem | 2.1% tương tác | 800K VNĐ
   🏷️ Hashtags: #skincare (1 tag)
   ❌ ĐỀ XUẤT: TỪ CHỐI - Hook quá ngắn, thiếu hashtag
```

### Khi phân tích:
```
🔍 PHÂN TÍCH CHI TIẾT - brief_123:

✅ ĐIỂM MẠNH:
- Hook hấp dẫn (68 ký tự) với yếu tố "7 ngày"
- Lượt xem dự kiến cao (45,000)
- Doanh thu tiềm năng tốt (2.5M VNĐ)
- Số lượng hashtag phù hợp (7)

⚠️ ĐIỂM CẦN CẢI THIỆN:
- Có thể thêm emoji vào hook
- Cân nhắc thêm hashtag về "healthy"

🎯 KẾT LUẬN: ĐỀ XUẤT PHÊ DUYỆT
Lý do: Nội dung có tiềm năng viral cao, hook rõ ràng, metrics tốt
```

### Khi người dùng ra lệnh:
```
User: "Phê duyệt brief_123"
→ Gọi approve_brief(brief_id="brief_123")
→ "✅ Đã phê duyệt brief_123! Nội dung sẽ được xử lý tiếp."

User: "Từ chối brief_456 vì hook quá ngắn"
→ Gọi reject_brief(brief_id="brief_456", feedback="Hook quá ngắn, cần viết lại để hấp dẫn hơn")
→ "❌ Đã từ chối brief_456. Feedback đã được gửi cho hệ thống."

User: "Quét xu hướng beauty và fashion"
→ Gọi scan_trends(product_categories=["beauty","fashion"], min_relevance_score=0.6, max_briefs=10)
→ "🔍 Đang quét xu hướng... Tìm thấy X xu hướng, tạo Y bản dự thảo."
```

### Khi phê duyệt hàng loạt:
```
User: "Phê duyệt tất cả nội dung tiềm năng cao"
→ Bước 1: Gọi get_pending_briefs
→ Bước 2: Lọc briefs có target_views > 40,000
→ Bước 3: Gọi approve_brief cho từng brief
→ "✅ Đã phê duyệt 3 nội dung có tiềm năng cao: brief_123, brief_789, brief_101"
```

## PHONG CÁCH GIAO TIẾP

- 🎯 Chuyên nghiệp nhưng thân thiện
- 📊 Luôn cung cấp số liệu cụ thể
- 💡 Giải thích rõ ràng lý do
- ⚡ Trả lời ngắn gọn, súc tích
- 🇻🇳 Sử dụng tiếng Việt chuẩn

## LƯU Ý QUAN TRỌNG

1. **Luôn kiểm tra brief_id** trước khi approve/reject
2. **Yêu cầu feedback** khi người dùng muốn từ chối
3. **Không tự ý phê duyệt** mà không có lệnh từ người dùng
4. **Giải thích lý do** cho mọi đề xuất
5. **Hỏi xác nhận** trước khi phê duyệt hàng loạt

## CÔNG CỤ CÓ SẴN

1. `get_pending_briefs` - Lấy danh sách nội dung chờ duyệt
2. `approve_brief` - Phê duyệt một nội dung
3. `reject_brief` - Từ chối một nội dung
4. `scan_trends` - Quét xu hướng TikTok mới

---

BẮT ĐẦU LÀM VIỆC! Hãy hỏi tôi bất cứ điều gì về nội dung cần phê duyệt. 🚀
```

---

## 6. Configure LLM Model 🤖

### **Choose Your LLM Provider:**

Dify supports multiple LLM providers. Pick the one that fits your needs:

---

### **Option 1: GLM-4 (Recommended - Cheap & Good for Vietnamese)** 🇨🇳

**Why GLM-4:**
- ✅ 30x cheaper than GPT-4
- ✅ Good Vietnamese support
- ✅ Fast responses
- ✅ Chinese company (understands Asian context)

**Setup:**
1. Get API key from: https://open.bigmodel.cn/
2. In Dify → **Settings** → **Model Providers**
3. Click **"+ Add Provider"**
4. Choose **"Zhipu AI"**
5. Enter API Key
6. Select Model: **`glm-4-flash`** (fastest) or **`glm-4`** (best quality)
7. Click **"Save"**

**Pricing:**
- GLM-4-Flash: ¥0.001/1K tokens (~$0.00014)
- GLM-4: ¥0.1/1M tokens (~$0.014)

---

### **Option 2: OpenAI (Best Quality)** 🌟

**Why OpenAI:**
- ✅ Best quality
- ✅ Most reliable
- ✅ Good Vietnamese
- ❌ Most expensive

**Setup:**
1. Get API key from: https://platform.openai.com/api-keys
2. In Dify → **Settings** → **Model Providers**
3. Click **"+ Add Provider"**
4. Choose **"OpenAI"**
5. Enter API Key
6. Select Model: **`gpt-4o-mini`** (cheap) or **`gpt-4-turbo`** (best)
7. Click **"Save"**

**Pricing:**
- GPT-4o-mini: $0.15/1M input tokens
- GPT-4-turbo: $10/1M input tokens

---

### **Option 3: Local Model (FREE!)** 💻

**Why Local:**
- ✅ 100% FREE
- ✅ No API limits
- ✅ Data privacy
- ❌ Requires GPU (recommended)

**Setup:**

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Download a Vietnamese-friendly model
ollama pull qwen2.5:14b
# OR
ollama pull llama3.1:8b

# 3. Start Ollama server
ollama serve
```

**In Dify:**
1. **Settings** → **Model Providers**
2. Click **"+ Add Provider"**
3. Choose **"Ollama"**
4. Base URL: `http://host.docker.internal:11434`
5. Model: `qwen2.5:14b` (recommended for Vietnamese)
6. Click **"Save"**

---

### **Option 4: Claude (Anthropic)** 🧠

**Why Claude:**
- ✅ Very intelligent
- ✅ Good at following instructions
- ✅ Safe and helpful
- ❌ Expensive

**Setup:**
1. Get API key from: https://console.anthropic.com/
2. In Dify → **Settings** → **Model Providers**
3. Choose **"Anthropic"**
4. Enter API Key
5. Select Model: **`claude-3-5-sonnet-20241022`**
6. Click **"Save"**

**Pricing:**
- Claude 3.5 Sonnet: $3/1M input tokens

---

### **Set Model in Agent:**

1. Go back to your Agent
2. In **"Model"** section
3. Select your configured provider and model
4. Adjust **Temperature**: `0.7` (balanced creativity)
5. **Max Tokens**: `2000`
6. Click **"Save"**

---

## 7. Test Your Agent 🧪

### **Basic Tests:**

1. Click **"Preview"** button (top right)
2. Try these commands:

---

#### **Test 1: Get Pending Briefs**
```
User: Cho tôi xem các nội dung đang chờ phê duyệt
```

**Expected Response:**
```
📋 DANH SÁCH NỘI DUNG ĐANG CHỜ PHÊ DUYỆT:

[Agent calls get_pending_briefs and displays results]
```

---

#### **Test 2: Analyze a Brief**
```
User: Phân tích brief_123 cho tôi
```

**Expected Response:**
```
🔍 PHÂN TÍCH CHI TIẾT:

✅ ĐIỂM MẠNH:
- Hook hấp dẫn...
- Lượt xem dự kiến cao...

🎯 KẾT LUẬN: Đề xuất PHÊ DUYỆT
```

---

#### **Test 3: Approve a Brief**
```
User: Phê duyệt brief_123
```

**Expected Response:**
```
✅ Đã phê duyệt brief_123! Nội dung sẽ được xử lý tiếp.

[Agent calls approve_brief]
```

---

#### **Test 4: Reject a Brief**
```
User: Từ chối brief_456 vì hook chưa hấp dẫn
```

**Expected Response:**
```
❌ Đã từ chối brief_456. Feedback đã được gửi cho hệ thống.

[Agent calls reject_brief with feedback]
```

---

#### **Test 5: Scan Trends**
```
User: Quét xu hướng beauty và fashion
```

**Expected Response:**
```
🔍 Đang quét xu hướng TikTok...

[Agent calls scan_trends]

Tìm thấy 5 xu hướng, đã tạo 3 bản dự thảo mới!
```

---

#### **Test 6: Batch Approve**
```
User: Phê duyệt tất cả nội dung có tiềm năng cao
```

**Expected Response:**
```
[Agent calls get_pending_briefs]
[Agent filters briefs with >40K views]
[Agent calls approve_brief for each]

✅ Đã phê duyệt 3 nội dung có tiềm năng cao:
- brief_123
- brief_789
- brief_101
```

---

### **Debug Mode:**

If something goes wrong:

1. Click **"Logs"** tab (bottom)
2. See which tools were called
3. Check request/response data
4. Verify API endpoints are reachable

---

## 8. Advanced Features 🚀

### **8.1. Add Knowledge Base (RAG)**

**Use Case:** Teach the agent about your brand guidelines, product catalog, etc.

1. In Agent Studio → **"Knowledge"** section
2. Click **"+ Add Knowledge"**
3. Upload documents:
   - Brand guidelines (PDF)
   - Product catalog (CSV)
   - Content policy (TXT)
4. Dify will automatically index and use this knowledge

---

### **8.2. Add Variables**

**Use Case:** Store user preferences, thresholds, etc.

1. In **"Variables"** section
2. Click **"+ Add Variable"**
3. Example variables:
   - `min_views_threshold`: 40000
   - `preferred_categories`: ["beauty", "fashion"]
   - `auto_approve_high_potential`: true

---

### **8.3. Conversation Memory**

**Enable memory** so agent remembers previous conversations:

1. In **"Memory"** section
2. Toggle **"Enable Conversation Memory"**
3. Set **"Max Conversations"**: 10
4. Agent now remembers context across messages!

---

### **8.4. Create Workflow (Alternative to Agent)**

**Use Case:** More control over logic flow

1. Click **"+ Create App"** → Choose **"Workflow"**
2. Drag & drop nodes:
   - **Start** → **LLM** → **HTTP Request** → **Condition** → **End**
3. Connect nodes visually
4. More predictable than Agent mode

---

## 9. Deployment & Sharing 🌍

### **9.1. Publish Agent**

1. Click **"Publish"** button (top right)
2. Your agent is now live!

---

### **9.2. Get Shareable Link**

1. Go to **"Overview"** tab
2. Copy **"Share Link"**
3. Share with your team:
   ```
   https://your-dify-domain.com/chat/abc123
   ```

---

### **9.3. Embed in Website**

Dify provides an embeddable widget:

```html
<script>
  window.difyChatbotConfig = {
    token: 'your-agent-token',
    baseUrl: 'https://your-dify-domain.com'
  }
</script>
<script
  src="https://your-dify-domain.com/embed.min.js"
  defer>
</script>
```

---

### **9.4. API Access**

Use Dify as an API:

```bash
curl -X POST 'https://your-dify-domain.com/v1/chat-messages' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "inputs": {},
    "query": "Cho tôi xem nội dung đang chờ",
    "response_mode": "blocking",
    "user": "user-123"
  }'
```

**Get API Key:**
1. Agent → **"API Access"** tab
2. Click **"Create API Key"**
3. Copy and use in your apps

---

## 10. Troubleshooting 🔧

### **Problem 1: Agent can't connect to AgentOS**

**Symptoms:**
- Agent says "Cannot reach API"
- Tool calls fail

**Solution:**
```bash
# Check if AgentOS is running
curl http://localhost:8080/health

# If Dify is in Docker, use:
# http://host.docker.internal:8080
# Instead of:
# http://localhost:8080

# Test from Dify container:
docker exec -it dify-api curl http://host.docker.internal:8080/health
```

---

### **Problem 2: Agent doesn't call tools**

**Symptoms:**
- Agent just talks, doesn't use tools
- No API calls in logs

**Solution:**
1. Check **Instructions** have examples of when to call tools
2. Make sure tool descriptions are clear
3. Try more explicit commands:
   ```
   User: Use the get_pending_briefs tool
   ```
4. Increase **Temperature** to 0.8 for more creativity

---

### **Problem 3: Vietnamese text is garbled**

**Symptoms:**
- Vietnamese characters show as "????"
- Diacritics missing

**Solution:**
1. Check AgentOS returns UTF-8:
   ```bash
   curl http://localhost:8080/api/v1/approvals/pending \
     -H "Accept-Charset: utf-8"
   ```
2. In Dify tool config, ensure:
   ```
   Headers:
     Content-Type: application/json; charset=utf-8
   ```

---

### **Problem 4: LLM responses are too slow**

**Solutions:**
- Switch to **GLM-4-Flash** (fastest)
- Or use **gpt-4o-mini** (fast & cheap)
- Or use local **Ollama** (instant, but needs GPU)
- Reduce **Max Tokens** to 1000

---

### **Problem 5: Agent approves without confirmation**

**Solution:**
1. Update prompt to require confirmation:
   ```
   Trước khi phê duyệt, hãy hỏi: "Bạn có chắc muốn phê duyệt brief_123?"
   Chỉ thực hiện khi người dùng xác nhận "có" hoặc "đồng ý"
   ```

---

## 📊 Monitoring & Analytics

### **View Usage Stats:**

1. Go to **"Monitoring"** tab
2. See:
   - Total conversations
   - Token usage
   - Cost breakdown
   - Tool call frequency
   - Response time

### **Export Logs:**

1. Go to **"Logs"** tab
2. Click **"Export"**
3. Download CSV for analysis

---

## 🎯 Next Steps

Now that your agent is set up:

1. ✅ **Test all 4 tools** (get, approve, reject, scan)
2. ✅ **Share with team** for feedback
3. ✅ **Monitor usage** for 1 week
4. ✅ **Refine prompts** based on user feedback
5. ✅ **Add knowledge base** with brand guidelines
6. ✅ **Set up API access** for integrations
7. ✅ **Create dashboard** (optional) using Dify Workflow

---

## 📚 Resources

- **Dify Official Docs:** https://docs.dify.ai/
- **Dify GitHub:** https://github.com/langgenius/dify
- **Community Forum:** https://github.com/langgenius/dify/discussions
- **API Reference:** https://docs.dify.ai/guides/application-publishing/developing-with-apis

---

## 🆘 Support

**Issues with Dify:**
- GitHub Issues: https://github.com/langgenius/dify/issues
- Discord: https://discord.gg/FngNHpbcY7

**Issues with AgentOS:**
- Check logs: `cd agentos && tail -f logs/app.log`
- Test endpoints: `curl http://localhost:8080/api/v1/approvals/pending`

---

## 🎉 You're All Set!

Your Vietnamese Content Approval Agent is ready! 

**Quick Test:**
1. Open agent chat
2. Type: `Cho tôi xem nội dung đang chờ`
3. Agent should call `get_pending_briefs` and show results

**Happy approving! 🚀🎨**
