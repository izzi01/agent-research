# 🚀 Dify Quick Reference Card - Vietnamese Content Approval

**1-Page Cheat Sheet for Fast Setup**

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Access Dify
http://localhost:3001

# 2. Create Agent
Click "+ Create App" → "Agent"
Name: "Vietnamese Content Approval"

# 3. Add 4 Tools (see below)

# 4. Add Prompt (see below)

# 5. Choose LLM Model

# 6. Test & Publish
```

---

## 🔧 4 API Tools Configuration

### **Tool 1: Get Pending** 📋
```yaml
Name: get_pending_briefs
Method: GET
URL: http://host.docker.internal:8080/api/v1/approvals/pending
```

### **Tool 2: Approve** ✅
```yaml
Name: approve_brief
Method: POST
URL: http://host.docker.internal:8080/api/v1/approvals/submit
Body: {"brief_id":"{{brief_id}}","approved":true,"feedback":"{{feedback}}"}
```

### **Tool 3: Reject** ❌
```yaml
Name: reject_brief
Method: POST
URL: http://host.docker.internal:8080/api/v1/approvals/submit
Body: {"brief_id":"{{brief_id}}","approved":false,"feedback":"{{feedback}}"}
```

### **Tool 4: Scan** 🔍
```yaml
Name: scan_trends
Method: POST
URL: http://host.docker.internal:8080/api/v1/trends/scan
Body: {"product_categories":{{categories}},"min_relevance_score":{{score}},"max_briefs":{{max}}}
```

---

## 📝 Vietnamese Prompt (Short Version)

```
Bạn là trợ lý AI phê duyệt nội dung TikTok tiếng Việt.

CÔNG CỤ:
- get_pending_briefs: Xem nội dung chờ duyệt
- approve_brief: Phê duyệt
- reject_brief: Từ chối
- scan_trends: Quét xu hướng

QUY TẮC ĐÁNH GIÁ:
- 🔥 Views > 40K: Tiềm năng cao → Đề xuất PHÊ DUYỆT
- ⭐ Views 20-40K: Trung bình → Cân nhắc
- 📉 Views < 20K: Thấp → Từ chối
- ✅ Hashtag 4-8: Tối ưu
- ❌ Hook < 30 ký tự: Quá ngắn

HÀNH ĐỘNG:
- "Cho tôi xem" → Gọi get_pending_briefs
- "Phê duyệt brief_X" → Gọi approve_brief
- "Từ chối brief_Y vì..." → Gọi reject_brief
- "Quét xu hướng beauty" → Gọi scan_trends

Trả lời bằng tiếng Việt, rõ ràng, có số liệu.
```

---

## 🤖 LLM Model Options

| Provider | Model | Cost/1M Tokens | Speed | Vietnamese |
|----------|-------|----------------|-------|------------|
| **GLM-4** | glm-4-flash | $0.14 | ⚡⚡⚡ | ✅ Good |
| **OpenAI** | gpt-4o-mini | $0.15 | ⚡⚡ | ✅ Great |
| **Ollama** | qwen2.5:14b | FREE | ⚡⚡ | ✅ Good |
| **Claude** | claude-3.5-sonnet | $3.00 | ⚡ | ✅ Great |

**Recommended:** GLM-4-Flash (cheap + fast + good Vietnamese)

---

## 🧪 Test Commands

```
1. "Cho tôi xem các nội dung đang chờ phê duyệt"
   → Should call get_pending_briefs

2. "Phân tích brief_123"
   → Should analyze and recommend

3. "Phê duyệt brief_123"
   → Should call approve_brief

4. "Từ chối brief_456 vì hook chưa hấp dẫn"
   → Should call reject_brief with feedback

5. "Quét xu hướng beauty và fashion"
   → Should call scan_trends

6. "Phê duyệt tất cả nội dung tiềm năng cao"
   → Should filter >40K views and approve all
```

---

## 🔍 Troubleshooting

### Can't connect to AgentOS
```bash
# Use this URL in tools:
http://host.docker.internal:8080

# Test connection:
docker exec -it dify-api curl http://host.docker.internal:8080/health
```

### Agent doesn't call tools
```
1. Make prompt examples clearer
2. Use explicit commands: "Use get_pending_briefs tool"
3. Increase temperature to 0.8
```

### Slow responses
```
Switch to:
- GLM-4-Flash (fastest)
- gpt-4o-mini (fast & cheap)
- Local Ollama (instant)
```

### Vietnamese characters broken
```yaml
# Add to all tool headers:
Content-Type: application/json; charset=utf-8
Accept-Charset: utf-8
```

---

## 📊 Access URLs

| Service | URL |
|---------|-----|
| **Dify UI** | http://localhost:3001 |
| **Dify API** | http://localhost:5001 |
| **AgentOS** | http://localhost:8080 |
| **AgentOS Docs** | http://localhost:8080/docs |

---

## 🎯 Essential Dify Features

### Publish & Share
```
1. Click "Publish" → Get shareable link
2. API Access → Create API key
3. Embed → Copy widget code
```

### Monitoring
```
1. Monitoring tab → View usage stats
2. Logs tab → Debug tool calls
3. Export → Download conversation logs
```

### Advanced
```
1. Add Knowledge Base → Upload PDFs
2. Enable Memory → Remember conversations
3. Add Variables → Store preferences
4. Create Workflow → Visual flow control
```

---

## 💡 Pro Tips

1. **Use `host.docker.internal`** instead of `localhost` if Dify is in Docker
2. **Test tools individually** before testing agent
3. **Start with simple prompt**, add complexity later
4. **Monitor logs** when debugging tool calls
5. **Use GLM-4** for cost savings (30x cheaper than GPT-4)
6. **Enable memory** for better context
7. **Create workflows** for complex logic flows

---

## 📞 Support Links

- **Dify Docs:** https://docs.dify.ai/
- **GitHub:** https://github.com/langgenius/dify
- **Discord:** https://discord.gg/FngNHpbcY7
- **GLM-4 API:** https://open.bigmodel.cn/

---

## ✅ Checklist

- [ ] Dify running at localhost:3001
- [ ] AgentOS running at localhost:8080
- [ ] Created Agent app in Dify
- [ ] Added 4 API tools
- [ ] Configured Vietnamese prompt
- [ ] Selected LLM model (GLM-4 recommended)
- [ ] Tested all 6 commands
- [ ] Published agent
- [ ] Got shareable link
- [ ] Shared with team

---

**🎉 You're ready! Start approving content in Vietnamese! 🚀**
