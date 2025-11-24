# AgentOS - Vietnamese Marketing Automation

AI agent system for automating Vietnamese e-commerce marketing using Agno framework, Claude 4.0, and multi-platform publishing.

## 🎯 What This Does

This sample implementation demonstrates:

1. **TrendMonitor Agent** - Discovers trending TikTok topics relevant to Vietnamese e-commerce
2. **ContentStrategist Agent** - Matches trends to products and creates Vietnamese content briefs
3. **Multi-Agent Workflow** - Coordinates agents to automate content generation pipeline
4. **FastAPI Server** - REST API with human-in-the-loop approval workflows
5. **Production-Ready** - Prometheus metrics, health checks, Docker deployment

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TrendMonitor Agent                       │
│  - Fetch TikTok trends via TickerTrends API                │
│  - Analyze engagement (views, likes, growth rate)           │
│  - Filter for Vietnamese market relevance                   │
│  - Store trends in pgvector for RAG                        │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                 ContentStrategist Agent                      │
│  - Query product catalog (vector search)                    │
│  - Match trends to products (semantic similarity)           │
│  - Generate Vietnamese content briefs using Claude          │
│  - Create hooks, scripts, hashtags, voiceover text         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Human Approval (HITL Workflow)                  │
│  - Queue briefs for batch review                            │
│  - Approval UI shows preview + metrics                      │
│  - Approve/reject with feedback                             │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│         Platform Publishing (Future Implementation)          │
│  - TextCreator Agent → Generate final Vietnamese copy       │
│  - VideoGenerator Agent → Create videos with Vbee TTS      │
│  - PublisherAgent → Post to Facebook, TikTok, Shopee       │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
agentos/
├── agents/
│   ├── trend_monitor.py          # TikTok trend discovery agent
│   └── content_strategist.py     # Content brief creation agent
│
├── workflows/
│   └── trend_to_content.py       # Multi-agent workflow orchestration
│
├── main.py                        # FastAPI application
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container image definition
├── .env.example                   # Environment variable template
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 16 with pgvector extension
- API keys (see `.env.example`)

### Local Development

1. **Clone and setup:**

```bash
cd agentos/
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment:**

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

3. **Start PostgreSQL with pgvector:**

```bash
docker run -d \
  --name postgres-pgvector \
  -e POSTGRES_USER=agno \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=marketing_automation \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

4. **Run the application:**

```bash
python main.py
```

The API will be available at http://localhost:8080

### Docker Deployment

```bash
# Build image
docker build -t marketing-automation/agentos:latest .

# Run container
docker run -d \
  --name agentos \
  -p 8080:8080 \
  --env-file .env \
  marketing-automation/agentos:latest
```

## 🧪 Testing the Agents

### 1. Test TrendMonitor Agent

```python
from agents.trend_monitor import TrendMonitor
import os

# Initialize agent
agent = TrendMonitor(
    db_url=os.getenv("DATABASE_URL"),
    tickertrends_api_key=os.getenv("TICKERTRENDS_API_KEY")
)

# Run trend scan
trends = agent.run_trend_scan(
    product_categories=["beauty", "fashion", "food", "electronics"],
    min_relevance_score=0.5
)

# Print results
for trend in trends[:3]:
    print(f"\n#{trend['hashtag']}")
    print(f"  Views: {trend['views']:,}")
    print(f"  Growth: {trend['growth_rate']}%")
    print(f"  Relevance: {trend['analysis']['relevance_score']:.2f}")
```

**Output:**
```
🔥 Found 3 Relevant Trends:

#ĂnVặt
  📊 Views: 234,000,000
  📈 Growth: 410%
  ⭐ Relevance: 0.80
  💡 Reasons: Category match: food, E-commerce keywords detected, High engagement rate: 15.6%, Viral growth: 410% in 24h
  ✅ Action: create_content

#BeautyHacks
  📊 Views: 67,000,000
  📈 Growth: 320%
  ⭐ Relevance: 0.70
  💡 Reasons: Category match: beauty, High engagement rate: 9.2%, Viral growth: 320% in 24h
  ✅ Action: create_content
```

### 2. Test ContentStrategist Agent

```python
from agents.content_strategist import ContentStrategist

# Initialize agent
agent = ContentStrategist(db_url=os.getenv("DATABASE_URL"))

# Sample trend
trend = {
    "hashtag": "#BeautyHacks",
    "views": 67000000,
    "engagement_rate": 9.2,
    "growth_rate": 320,
    "category": "beauty",
    "keywords": ["làm đẹp", "beauty", "skincare", "makeup"]
}

# Create content briefs
briefs = agent.run_strategy_session(
    trend=trend,
    max_products=2,
    content_formats=["tiktok_video"]
)

# Print brief
brief = briefs[0]
print(f"\n📝 Content Brief:")
print(f"  Trend: {brief['trend_id']}")
print(f"  Hook: {brief['vietnamese_hook']}")
print(f"  Format: {brief['content_angle']}")
print(f"  Hashtags: {' '.join(brief['hashtags'][:5])}")
print(f"\n  Voiceover Script (excerpt):")
print(brief['vietnamese_voiceover'][:200] + "...")
```

**Output:**
```
📝 Content Brief:
  Trend: #BeautyHacks
  Hook: Chị em ơi! Trend làm đẹp này đang gây bão TikTok, mình phải thử ngay! 💄✨
  Format: Product Review + Tutorial - Show before/after transformation
  Hashtags: #BeautyHacks #ReviewSảnPhẩm #LàmĐẹp #BeautyVietNam #TikTokShop

  Voiceover Script (excerpt):
Chào các bạn! Hôm nay mình sẽ review cho các bạn cây son lì này đang được nhiều bạn hỏi.

[Unboxing]
Bao bì rất xinh xắn, giá chỉ 259k thôi nha các bạn!...
```

### 3. Test Complete Workflow

```python
from workflows.trend_to_content import TrendToContentWorkflow

# Initialize workflow
workflow = TrendToContentWorkflow(
    db_url=os.getenv("DATABASE_URL"),
    tickertrends_api_key=os.getenv("TICKERTRENDS_API_KEY")
)

# Run daily content generation
results = workflow.run_daily_content_generation(
    product_categories=["beauty", "fashion", "food", "electronics"],
    min_relevance_score=0.6,
    max_briefs_per_day=5
)

print(f"\n✅ Workflow completed:")
print(f"  Trends Discovered: {results['trends_discovered']}")
print(f"  Content Briefs Created: {results['content_briefs_created']}")
print(f"  Duration: {results['duration_seconds']:.2f}s")
```

## 🌐 API Endpoints

### Health & Metrics

```bash
# Health check (liveness probe)
curl http://localhost:8080/health

# Readiness check
curl http://localhost:8080/ready

# Prometheus metrics
curl http://localhost:8080/metrics
```

### Trend Scanning

```bash
# Scan trends and create content briefs
curl -X POST http://localhost:8080/api/v1/trends/scan \
  -H "Content-Type: application/json" \
  -d '{
    "product_categories": ["beauty", "fashion", "food"],
    "min_relevance_score": 0.6,
    "max_briefs": 5
  }'
```

**Response:**
```json
{
  "workflow_id": "workflow_2025-11-24T10:30:00",
  "status": "completed",
  "trends_discovered": 5,
  "content_briefs_created": 3,
  "briefs": [
    {
      "trend_id": "#BeautyHacks",
      "vietnamese_hook": "Chị em ơi! Trend làm đẹp này đang gây bão...",
      "hashtags": ["#BeautyHacks", "#LàmĐẹp", "#TikTokShop"],
      "success_metrics": {
        "target_views": 50000,
        "expected_revenue_vnd": 25900000
      }
    }
  ]
}
```

### Approval Workflow

```bash
# Get pending approvals
curl http://localhost:8080/api/v1/approvals/pending

# Submit approval decision
curl -X POST http://localhost:8080/api/v1/approvals/submit \
  -H "Content-Type: application/json" \
  -d '{
    "brief_id": "#BeautyHacks",
    "approved": true,
    "feedback": "Great content! Approved for posting."
  }'
```

### Publishing

```bash
# Publish to platforms
curl -X POST http://localhost:8080/api/v1/content/publish \
  -H "Content-Type: application/json" \
  -d '{
    "brief_id": "#BeautyHacks",
    "platforms": ["facebook", "tiktok"],
    "scheduled_time": "2025-11-24T19:00:00+07:00"
  }'
```

## 🔧 Configuration

### Environment Variables

See `.env.example` for all configuration options.

**Required:**
- `DATABASE_URL` - PostgreSQL connection string with pgvector
- `ANTHROPIC_API_KEY` - Claude API key for content generation
- `TICKERTRENDS_API_KEY` - TikTok trend monitoring API

**Optional:**
- `SIMPLIFIED_API_KEY`, `HEYGEN_API_KEY`, `DID_API_KEY`, `RUNWAY_API_KEY` - Video generation
- `VBEE_API_KEY` - Vietnamese text-to-speech
- `FACEBOOK_ACCESS_TOKEN`, `TIKTOK_ACCESS_TOKEN` - Platform publishing

## 📊 Monitoring

### Prometheus Metrics

The application exposes metrics at `/metrics`:

**Agent Execution:**
- `agent_executions_total{agent_name, status}` - Total agent executions
- `agent_execution_duration_seconds{agent_name}` - Execution duration histogram

**Content Workflow:**
- `content_approval_total{decision}` - Approvals/rejections
- `approval_cycle_time_seconds` - Time from generation to approval
- `content_pending_approval_count` - Current approval queue size

**Business Metrics:**
- `trends_monitored_total{source}` - Total trends monitored
- `platform_posts_total{platform, status}` - Platform posts published
- `llm_tokens_used_total{provider, model, type}` - Token usage

### Grafana Dashboards

See `/k8s/monitoring/grafana-dashboards.yaml` for pre-built dashboards.

## 🔌 n8n Integration

The application provides a webhook endpoint for n8n workflows:

```javascript
// n8n HTTP Request Node
POST http://agentos-service:8080/webhooks/n8n/trigger
{
  "trigger": "daily_trend_scan",
  "config": {
    "product_categories": ["beauty", "fashion"],
    "min_relevance_score": 0.6,
    "max_briefs": 10
  }
}
```

**n8n Workflow Example:**

1. **Schedule Trigger** - Daily at 8:00 AM GMT+7
2. **HTTP Request** - Call AgentOS webhook
3. **Set Node** - Extract briefs
4. **Loop** - For each brief
5. **Send Email** - Notify team for approval
6. **Wait for Webhook** - Approval decision
7. **HTTP Request** - Submit approval to AgentOS

## 🏗️ Next Steps

This sample implementation covers the foundation. To complete the system:

### 1. Implement TextCreator Agent
- Generate final Vietnamese copy from briefs
- Support multiple formats (short/long, formal/casual)
- Add A/B testing variants

### 2. Implement VideoGenerator Agent
- Multi-tool selector (Simplified, HeyGen, D-ID, Runway)
- Vietnamese subtitle generation
- Vbee TTS integration for voiceover
- Video template selection

### 3. Implement PublisherAgent
- Facebook Graph API integration
- TikTok Content Posting API
- Shopee Open API
- YouTube Data API
- Scheduled posting with retry logic

### 4. Build Approval UI
- React dashboard for batch content review
- Video preview player
- Side-by-side product comparison
- Quick approve/reject buttons
- Feedback form for revisions

### 5. Production Enhancements
- Add database migrations (Alembic)
- Implement product catalog import
- Add proper authentication (JWT)
- Enable HTTPS/TLS
- Add rate limiting
- Implement caching (Redis)

## 📚 References

- **Agno Documentation:** https://docs.agno.com
- **Claude API:** https://docs.anthropic.com
- **FastAPI:** https://fastapi.tiangolo.com
- **pgvector:** https://github.com/pgvector/pgvector

## 🤝 Contributing

This is a sample implementation for demonstration purposes. For production use:

1. Replace mock data with real API integrations
2. Add comprehensive error handling
3. Implement database migrations
4. Add unit and integration tests
5. Set up CI/CD pipeline
6. Configure production secrets management

## 📝 License

MIT License - See LICENSE file for details

---

**Built with ❤️ for Vietnamese e-commerce marketing automation**
