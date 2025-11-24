# How to Run TextCreator Agent - Step-by-Step Guide

Complete guide to run the **TextCreator agent** and generate Vietnamese social media copy.

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Run Standalone Agent (Simplest)

```bash
# 1. Navigate to agentos directory
cd /home/cid/projects/agent-research/agentos/

# 2. Install dependencies (if not done yet)
pip install -r requirements.txt

# 3. Set database URL (use in-memory for testing)
export DATABASE_URL="postgresql://agno:password@localhost:5432/marketing_automation"

# 4. Run the agent directly
python agents/text_creator.py
```

**Expected Output:**
```
==============================================================
VIETNAMESE COPY GENERATION RESULTS
==============================================================

📱 FACEBOOK
------------------------------------------------------------

Variant: default (casual)

Hôm nay mình review cho các bạn cây son lì này nha! 💄

Thật ra lúc đầu mình cũng hơi nghi ngờ vì giá chỉ 259K thôi. Nhưng dùng rồi mình phải công nhận: màu đẹp, lên môi mịn, không khô môi như mấy em son lì khác 😍

Quan trọng là giữ màu được 4-5 tiếng luôn nè! Ăn uống nhẹ vẫn còn màu 80% 💖

Các bạn thích thì vào shop mình xem nhé!

Hashtags: #ReviewSảnPhẩm #SonLì #LàmĐẹp #BeautyTips
CTA: Comment 'Đẹp' để mình gửi link shop nha!

📊 Metadata:
  Characters: 312 / 80
  Within limit: ❌
  Hashtags: 4 (valid: ✅)
  Emojis: 4 - Good emoji usage
```

---

### Option 2: Run via FastAPI Server (Production-like)

**Step 1: Start PostgreSQL (required)**

```bash
# Start PostgreSQL with pgvector
docker run -d \
  --name postgres-pgvector \
  -e POSTGRES_USER=agno \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=marketing_automation \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# Verify it's running
docker ps | grep postgres-pgvector
```

**Step 2: Configure Environment**

```bash
cd /home/cid/projects/agent-research/agentos/

# Copy environment template
cp .env.example .env

# Edit .env with your API keys (optional for testing)
nano .env
```

Minimum required in `.env`:
```bash
DATABASE_URL=postgresql://agno:password@localhost:5432/marketing_automation
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here  # Optional for mock data
```

**Step 3: Start the Server**

```bash
# Run the FastAPI server
python main.py
```

**Expected Output:**
```
INFO:     Starting AgentOS application...
INFO:     ✅ Workflow initialized successfully
INFO:     ✅ TextCreator agent initialized successfully
INFO:     🚀 AgentOS is ready!
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

**Server is now running at:** http://localhost:8080

---

## 📝 Testing the TextCreator Agent

### Test 1: Generate Copy via API

**Step 1: Create a Content Brief (simulate approval workflow)**

```bash
# Scan trends and create briefs
curl -X POST http://localhost:8080/api/v1/trends/scan \
  -H "Content-Type: application/json" \
  -d '{
    "product_categories": ["beauty"],
    "min_relevance_score": 0.6,
    "max_briefs": 1
  }'
```

**Expected Response:**
```json
{
  "workflow_id": "workflow_2025-11-24...",
  "status": "completed",
  "trends_discovered": 5,
  "content_briefs_created": 1,
  "briefs": [
    {
      "trend_id": "#BeautyHacks",
      "vietnamese_hook": "Chị em ơi! Trend làm đẹp này đang gây bão...",
      ...
    }
  ]
}
```

**Step 2: Approve the Brief**

```bash
# Get pending approvals
curl http://localhost:8080/api/v1/approvals/pending

# Approve the brief
curl -X POST http://localhost:8080/api/v1/approvals/submit \
  -H "Content-Type: application/json" \
  -d '{
    "brief_id": "#BeautyHacks",
    "approved": true,
    "feedback": "Looks great!"
  }'
```

**Step 3: Generate Vietnamese Copy**

```bash
# Generate copy for Facebook and TikTok
curl -X POST "http://localhost:8080/api/v1/content/generate-copy?brief_id=%23BeautyHacks&platforms=facebook&platforms=tiktok&generate_variants=false"
```

**Expected Response:**
```json
{
  "brief_id": "#BeautyHacks",
  "platforms": ["facebook", "tiktok"],
  "generated_at": "2025-11-24T10:30:00",
  "status": "ready_for_publish",
  "copy": {
    "facebook": [
      {
        "platform": "facebook",
        "variant": "default",
        "tone": "casual",
        "copy": {
          "body": "Hôm nay mình review cho các bạn cây son lì này nha! 💄\n\nThật ra lúc đầu...",
          "hashtags": ["#ReviewSảnPhẩm", "#SonLì", "#LàmĐẹp"],
          "call_to_action": "Comment 'Đẹp' để mình gửi link shop nha!"
        },
        "metadata": {
          "character_count": 312,
          "character_limit": 80,
          "within_limit": false,
          "hashtag_validation": {"valid": true, "count": 4},
          "emoji_analysis": {"emoji_count": 4, "optimal": true}
        }
      }
    ],
    "tiktok": [
      {
        "platform": "tiktok",
        "copy": {
          "body": "Trend làm đẹp hot nhất tuần này! 🔥\n\nThử ngay beauty hack với son lì...",
          "hashtags": ["#BeautyHacks", "#LàmĐẹp", "#TikTokShop"],
          "call_to_action": "Lướt qua shop ngay! 👇"
        }
      }
    ]
  }
}
```

---

### Test 2: Generate A/B Testing Variants

```bash
# Generate 3 variants for A/B testing
curl -X POST "http://localhost:8080/api/v1/content/generate-copy?brief_id=%23BeautyHacks&platforms=facebook&generate_variants=true"
```

**Expected Response:**
```json
{
  "copy": {
    "facebook": [
      {
        "variant_id": "facebook_v1_default",
        "variant": "default",
        "tone": "casual",
        "copy": {...}
      },
      {
        "variant_id": "facebook_v2_promotional",
        "variant": "promotional",
        "tone": "enthusiastic",
        "copy": {...}
      },
      {
        "variant_id": "facebook_v3_storytelling",
        "variant": "storytelling",
        "tone": "professional",
        "copy": {...}
      }
    ]
  }
}
```

---

### Test 3: Direct Python Usage (No Server)

Create a test script `test_textcreator.py`:

```python
from agents.text_creator import TextCreator
import os

# Initialize agent
agent = TextCreator(
    db_url=os.getenv("DATABASE_URL", "postgresql://agno:password@localhost:5432/marketing_automation")
)

# Sample content brief
brief = {
    "trend_id": "#BeautyHacks",
    "vietnamese_hook": "Chị em ơi! Trend làm đẹp này đang gây bão TikTok! 💄✨",
    "content_angle": "Product Review + Tutorial",
    "products": ["PROD001"],
    "hashtags": ["#BeautyHacks", "#LàmĐẹp", "#TikTokShop"]
}

# Generate copy for multiple platforms
results = agent.run_copy_generation(
    brief=brief,
    platforms=["facebook", "tiktok", "shopee"],
    generate_variants=False
)

# Print results
print("\n🎯 GENERATED VIETNAMESE COPY:\n")
for platform, copies in results["copy"].items():
    copy = copies[0]  # First variant
    print(f"📱 {platform.upper()}:")
    print(f"{copy['copy']['body']}\n")
    print(f"Hashtags: {' '.join(copy['copy']['hashtags'])}")
    print(f"CTA: {copy['copy']['call_to_action']}")
    print(f"Characters: {copy['metadata']['character_count']}")
    print("-" * 60)
```

Run it:
```bash
python test_textcreator.py
```

---

## 🎯 Platform-Specific Copy Examples

### Facebook Copy
**Characteristics:**
- Longer form (300-500 chars optimal)
- Conversational, story-driven
- Emojis: 3-5
- Hashtags at end (4-8 hashtags)

**Example:**
```
Hôm nay mình review cho các bạn cây son lì này nha! 💄

Thật ra lúc đầu mình cũng hơi nghi ngờ vì giá chỉ 259K thôi. Nhưng dùng rồi mình phải công nhận: màu đẹp, lên môi mịn, không khô môi như mấy em son lì khác 😍

Quan trọng là giữ màu được 4-5 tiếng luôn nè! Ăn uống nhẹ vẫn còn màu 80% 💖

Các bạn thích thì vào shop mình xem nhé!

#ReviewSảnPhẩm #SonLì #LàmĐẹp #BeautyTips
```

### TikTok Copy
**Characteristics:**
- Short, punchy (200-300 chars)
- Hook in first line
- Emojis: 4-6
- Trending hashtags (8-10)

**Example:**
```
Trend làm đẹp hot nhất tuần này! 🔥

Thử ngay beauty hack với son lì bền màu 24h 💄✨

Kết quả: Môi căng mọng, màu chuẩn, không khô! Giá chỉ 259K thôi nha 😍

Link shop ở dưới, các bạn múa tay lên nào! 💖

#BeautyHacks #LàmĐẹp #TikTokShop #ReviewSảnPhẩm #SonLì
```

### Shopee Copy
**Characteristics:**
- Product-focused, structured
- Bullet points for features
- SEO keywords
- Professional tone
- Clear pricing and promotions

**Example:**
```
SON LÌ BỀN MÀU 24H - CHÍNH HÃNG 💄

🌟 ĐẶC ĐIỂM NỔI BẬT:
• Màu sắc chuẩn, bền màu 24 giờ
• Công thức lì mượt, không khô môi
• An toàn, không chứa chì
• Phù hợp mọi loại môi

✨ CAM KẾT:
✓ Hàng chính hãng 100%
✓ Hoàn tiền nếu hàng giả
✓ Đổi trả trong 7 ngày
✓ Freeship đơn từ 50K

ĐẶT NGAY HÔM NAY! 🛒
```

---

## 🔍 API Endpoints Reference

### 1. Generate Copy
```bash
POST /api/v1/content/generate-copy
Query Params:
  - brief_id: string (e.g., "#BeautyHacks")
  - platforms: string[] (e.g., ["facebook", "tiktok"])
  - generate_variants: boolean (default: false)
```

### 2. Health Check
```bash
GET /health
# Returns: {"status": "healthy", "timestamp": "..."}
```

### 3. Metrics
```bash
GET /metrics
# Returns: Prometheus metrics including agent_executions_total
```

---

## 🐛 Troubleshooting

### Issue: "Failed to initialize TextCreator"

**Solution:**
```bash
# Check PostgreSQL is running
docker ps | grep postgres-pgvector

# If not running, start it
docker start postgres-pgvector

# Verify connection
psql postgresql://agno:password@localhost:5432/marketing_automation -c "SELECT 1;"
```

### Issue: "Module not found: agno"

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import agno; print(agno.__version__)"
```

### Issue: "Brief not found"

**Solution:**
You need to create and approve a brief first:
```bash
# Step 1: Scan trends
curl -X POST http://localhost:8080/api/v1/trends/scan -H "Content-Type: application/json" -d '{"product_categories": ["beauty"], "min_relevance_score": 0.6, "max_briefs": 1}'

# Step 2: Approve brief
curl -X POST http://localhost:8080/api/v1/approvals/submit -H "Content-Type: application/json" -d '{"brief_id": "#BeautyHacks", "approved": true}'

# Step 3: Generate copy
curl -X POST "http://localhost:8080/api/v1/content/generate-copy?brief_id=%23BeautyHacks&platforms=facebook"
```

---

## 📊 Monitoring

### View Metrics
```bash
curl http://localhost:8080/metrics | grep agent_executions
```

**Expected Output:**
```
agent_executions_total{agent_name="TextCreator",status="started"} 5.0
agent_executions_total{agent_name="TextCreator",status="completed"} 5.0
agent_executions_total{agent_name="TextCreator",status="failed"} 0.0
```

### Check Logs
```bash
# View server logs
tail -f logs/agentos.log

# Or if running in terminal
# Logs will appear in real-time
```

---

## 💡 Tips & Best Practices

### 1. Character Limits
- **Facebook:** Optimal 40-80 chars for newsfeed, but can go up to 63,206
- **TikTok:** Limit 2,200 chars, optimal 200-300 chars
- **Shopee:** Title 120 chars, description 3,000 chars
- **Instagram:** Limit 2,200 chars, optimal 125-150 chars

### 2. Hashtag Strategy
- **Facebook:** 4-8 hashtags (more looks spammy)
- **TikTok:** 8-10 hashtags (trending + niche)
- **Shopee:** 3-5 keywords (for SEO)
- **Instagram:** 8-12 hashtags (engagement sweet spot)

### 3. Emoji Usage
- Use 2-4 emojis per post for optimal engagement
- Place emojis at end of sentences, not mid-word
- Vietnamese audience loves: 💄 ✨ 🔥 💖 😍 💯

### 4. A/B Testing
Generate 2-3 variants and test:
- **Variant 1 (Default):** Conversational, relatable
- **Variant 2 (Promotional):** Price-focused, urgency
- **Variant 3 (Storytelling):** Personal experience, authentic

---

## 🎉 Success!

You've successfully run the TextCreator agent!

**What you can do now:**
1. ✅ Generate Vietnamese copy for Facebook, TikTok, Shopee
2. ✅ Create A/B testing variants
3. ✅ Validate character limits automatically
4. ✅ Optimize emoji and hashtag usage

**Next steps:**
- Integrate real Claude API for production
- Build VideoGenerator agent for video creation
- Add PublisherAgent for automatic posting
- Deploy to Kubernetes for production

---

**Questions?** Check `agentos/README.md` for more details or open an issue!
