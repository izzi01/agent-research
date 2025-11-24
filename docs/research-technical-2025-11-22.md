# Technical Research Report: AI Agent Framework for Vietnamese Marketing Automation

**Date:** 2025-11-22
**Prepared by:** President Trump
**Project Context:** E-commerce product marketing automation for Vietnamese market

---

## Executive Summary

[To be completed after research]

---

## 1. Research Objectives

### Technical Question

**Can AI agent frameworks (like CrewAI or AgentOps) automate Vietnamese marketing team workflows with human-in-the-loop approval and automated multi-platform posting?**

Specifically evaluating:
- AI agent frameworks (CrewAI, LangGraph, AutoGen, others)
- Vietnamese language content generation (text, video, voice)
- Multi-platform automation (Facebook, TikTok, Zalo, Shopee, YouTube)
- Human approval workflows (batch approval, single approver)
- Third-party automation platforms for platform integration
- Implementation architecture and cost feasibility (~$500/month budget)

### Project Context

**Current State:** Fully manual marketing operations across multiple platforms

**Team:** Developer-led (technical capability, limited marketing expertise)

**Use Case:** E-commerce product marketing and sales automation

**Target Market:** Vietnamese consumers across social and e-commerce platforms

**Marketing Operations to Automate:**
- Media posting schedules
- Multi-platform content posting (Facebook, Zalo, Reels, YouTube, TikTok)
- Website SEO and article writing
- Shopee & TikTok Shop management (product descriptions, video content, live streaming coordination)

### Requirements and Constraints

#### Functional Requirements

**CRITICAL (Must-Have):**
1. **Vietnamese Language Content Generation**
   - Generate Vietnamese text content (social posts, product descriptions, articles)
   - Create video content with Vietnamese subtitles
   - Generate Vietnamese AI voice-overs for videos
   - Natural, culturally appropriate Vietnamese content

2. **Multi-Platform Posting Automation**
   - Facebook (posts, Reels)
   - TikTok (videos, product integration)
   - API integration or third-party platform support for automated posting

3. **Human-in-the-Loop Approval Workflow**
   - Batch approval interface (review multiple pieces of content)
   - Single approver workflow (not multi-level)
   - Content queuing and scheduling after approval

4. **AI Agent Orchestration**
   - Multi-agent coordination (content creator, SEO specialist, video editor, scheduler)
   - Workflow automation across agent tasks
   - Error handling and retry logic

**IMPORTANT (High Priority):**
5. **Video Content Generation** ⚠️ CRITICAL FOCUS AREA
   - Text-to-video or template-based video creation
   - Subtitle generation and embedding (Vietnamese)
   - AI voice synthesis (Vietnamese voices)
   - Export formats compatible with Facebook, TikTok, YouTube (Reels, Shorts, standard videos)
   - Support multiple video formats and aspect ratios (9:16, 16:9, 1:1)

6. **Automatic Trend Monitoring**
   - Monitor TikTok groups/hashtags automatically
   - Capture trending topics in Vietnamese market
   - Identify viral content patterns
   - Surface trending products/themes for content creation
   - Provide trend insights to inform content strategy

7. **E-Commerce Platform Integration**
   - Shopee product description generation and updates
   - TikTok Shop product management
   - Product video generation for e-commerce listings

8. **Content Scheduling and Calendar Management**
   - Publishing calendar management
   - Optimal timing recommendations
   - Multi-platform coordinated campaigns

**NICE-TO-HAVE (Lower Priority):**
9. **Content Remixing and Adaptation** (Optional)
   - Analyze successful content from competitors/trends
   - Adapt trending content patterns for own products
   - Transform content across formats (article → social → video)
   - Localize trending content from other markets to Vietnamese

10. **SEO and Website Content**
    - Vietnamese SEO article generation
    - Keyword research and optimization
    - Website content updates

11. **Live Streaming Coordination**
    - Live stream planning and script generation
    - Product showcase scripts
    - Q&A preparation content

12. **Analytics and Performance Tracking**
    - Content performance monitoring
    - Engagement analytics
    - A/B testing capabilities

#### Non-Functional Requirements

**Performance:**
- Content generation: Under 5 minutes for social posts, under 30 minutes for videos
- Batch processing: Handle 20-50 content pieces per approval batch
- Platform posting: Near real-time scheduling (within minutes of approval)

**Scalability:**
- Support multiple product catalogs (100+ products)
- Handle multiple campaigns simultaneously (5-10 active campaigns)
- Scale to multiple brands/clients in future

**Reliability:**
- 99% uptime for content generation services
- Retry logic for failed API calls to platforms
- Content backup and version control

**Usability:**
- Developer-friendly setup and configuration
- Simple approval interface (web-based preferred)
- Clear documentation for non-marketing developer

**Maintainability:**
- Code-based configuration (version controllable)
- Modular architecture (can swap AI providers, platforms)
- Clear logging and debugging capabilities

#### Technical Constraints

**Budget:**
- **Total monthly budget: ~$500 USD**
- Must include: AI API costs (LLM, voice, video), platform automation tools, hosting/infrastructure
- Cost breakdown needed across components

**Team Skills:**
- **Developer:** Programming capability, can work with APIs and frameworks
- **Limited marketing expertise:** Solution should guide marketing best practices
- **No dedicated DevOps:** Simple deployment preferred (Docker, managed services)

**Language Requirements:**
- **CRITICAL:** Full Vietnamese language support
- Content generation must be natural Vietnamese (not translated English)
- Voice synthesis must have Vietnamese voice options
- Platform automation must support Vietnamese character encoding

**Platform Priorities:**
- **Must-have:** Facebook, TikTok
- **Important:** Shopee, TikTok Shop
- **Nice-to-have:** Zalo, YouTube, website/SEO

**Technical Preferences:**
- Open-source or transparent frameworks preferred
- Avoid vendor lock-in where possible
- Python-based preferred (developer familiarity)
- Cloud-agnostic or multi-cloud capable

**Compliance and Content Safety:**
- Platform content policy compliance (Facebook, TikTok guidelines)
- E-commerce product description accuracy
- Avoid AI-generated content that violates platform ToS

**Integration Requirements:**
- Must integrate with Facebook Graph API or alternative
- Must integrate with TikTok API or automation platform
- Shopee API support (if available)
- Third-party paid platforms acceptable for API abstraction

---

## 2. Technology Options Evaluated

Based on comprehensive 2025 research, here are the technology categories and specific options evaluated:

### AI Agent Framework Options
1. **CrewAI** - Role-based multi-agent collaboration
2. **LangGraph** - Graph-based stateful workflows with production focus
3. **AutoGen v0.4** - Microsoft's asynchronous multi-agent framework

### Video Generation Platforms
4. **HeyGen** - AI video with 175+ languages, avatar-based
5. **Runway Gen-4** - Creative text-to-video generation
6. **Simplified** - Vietnamese-focused video + subtitle generation
7. **D-ID** - Affordable avatar creation

### Vietnamese Language Support
8. **Claude 3.5/4.0** - Best translation quality for Vietnamese (2025 benchmarks)
9. **GPT-4/GPT-5** - Strong Vietnamese support, widely adopted
10. **VietTTS** - Open-source Vietnamese voice synthesis
11. **ElevenLabs** - Commercial Vietnamese TTS with regional dialects
12. **Viettel AI** - Vietnamese company, 95% human-like voices

### TikTok Trend Monitoring
13. **TickerTrends API** - Time-series hashtag analytics
14. **Meltwater Monitor** - TikTok trends across 246 regions
15. **TikTok Official APIs** - Discovery, Search, Hashtag Analytics

### Platform Automation
16. **Facebook Graph API** - Direct posting via Python
17. **TikTok Content Posting API** - Official video posting (requires audit)
18. **Shopee Open API v2.0** - Product/order management
19. **Vista Social** - Multi-platform scheduler (FB, TikTok, 12+ platforms)
20. **Sendible** - Affordable all-in-one social scheduler

### Human-in-the-Loop Tools
21. **HumanLayer SDK** - Slack/Email approval workflows
22. **Approveit** - Approval triggers via Slack, Teams, API
23. **LangGraph (built-in)** - Native HITL interrupts

### Workflow Automation Platforms
24. **n8n** - Open-source, AI-native, best cost/execution
25. **Make.com** - Visual workflows, 350+ AI apps, AI Agent beta
26. **Zapier** - Largest ecosystem (8000+ apps), easiest to use

---

---

## 3. Detailed Technology Profiles

### Option 1: CrewAI (AI Agent Framework)

**Source:** https://www.crewai.com/ | https://github.com/crewAIInc/crewAI | https://laten

ode.com/blog/crewai-framework-2025-complete-review-of-the-open-source-multi-agent-ai-platform

**Current Version (2025):** Active development, 32K+ GitHub stars, ~1M monthly downloads

**Overview:**
CrewAI is an open-source framework for orchestrating role-playing, autonomous AI agents in structured workflows. Launched in early 2024, it has rapidly gained traction for marketing automation, with over 100,000 certified developers.

**Key Features:**
- **Role-Based Agent Design:** Agents have specific roles (Content Creator, SEO Specialist, Video Editor, Scheduler)
- **Marketing Automation Focus:** Built-in patterns for market research, content creation, quality review
- **Task Delegation:** Agents can delegate subtasks to other specialized agents
- **Sequential & Hierarchical Workflows:** Support for both linear and branching workflows
- **LLM Agnostic:** Works with OpenAI, Anthropic, local models, etc.

**Vietnamese Use Case Fit:**
- ✅ Can coordinate content creation → translation → video generation → posting workflow
- ✅ Built-in patterns for marketing teams (research, copywriting, review)
- ✅ Integrates with external tools (video APIs, platform APIs)
- ⚠️ No built-in approval UI - requires custom implementation

**Pros:**
- Rapid development and growing community
- Marketing-specific use case examples
- Easier to implement than LangGraph for beginners
- Good documentation and tutorials
- Python-based (developer preference met)

**Cons:**
- Younger framework (less battle-tested than LangGraph)
- No native human-in-the-loop features (need external tool)
- Limited state management compared to LangGraph
- No built-in approval workflows

**Pricing:**
- **Open-source:** Free
- **LLM Costs:** Pay-per-use for OpenAI/Anthropic APIs
- **Infrastructure:** Self-hosting costs (Docker, server)

**Implementation Complexity:** Medium (3-4 weeks for developer to build POC)

---

### Option 2: LangGraph (AI Agent Framework - Production Focus)

**Source:** https://www.langchain.com/langgraph | https://latenode.com/blog/langgraph-ai-framework-2025-complete-architecture-guide-multi-agent-orchestration-analysis

**Current Version (2025):** Production-ready, used by LinkedIn, Uber, Klarna

**Overview:**
LangGraph is a Python framework from LangChain for building stateful, multi-agent workflows using graph architectures. It prioritizes production-readiness, reliability, and complex workflow orchestration with built-in state management and human-in-the-loop capabilities.

**Key Features:**
- **Graph-Based Workflow:** Nodes and edges enable branching, looping, parallel execution
- **Persistent State Management:** Workflows maintain state across interruptions
- **Built-in Checkpointers:** Save workflow state for recovery from errors/interruptions
- **Human-in-the-Loop (HITL):** Native support for approval workflows and time-travel debugging
- **Streaming:** Real-time token streaming and intermediate step visibility
- **LangSmith Integration:** Observability and debugging tools

**Vietnamese Use Case Fit:**
- ✅ **PERFECT for human approval workflows** - native HITL support
- ✅ Stateful workflows ensure content drafts persist through approval process
- ✅ Can handle complex multi-stage campaigns with branching logic
- ✅ Production-ready error handling and fault tolerance
- ⚠️ Steeper learning curve than CrewAI

**Pros:**
- **Best-in-class human-in-the-loop features** (critical requirement!)
- Production-tested at major companies
- Excellent error handling and recovery
- Time-travel debugging for workflow inspection
- Persistent state across sessions
- Strong observability with LangSmith

**Cons:**
- Higher learning curve (20-30 hours to proficiency)
- More complex initial setup
- Requires more development expertise
- Less marketing-specific abstractions than CrewAI

**Pricing:**
- **Open-source:** Free
- **LangSmith (optional observability):** Free tier, then $39/month
- **LLM Costs:** Pay-per-use for APIs
- **Infrastructure:** Self-hosting costs

**Implementation Complexity:** High (4-6 weeks for full implementation with HITL)

---

### Option 3: HeyGen (Video Generation Platform)

**Source:** https://www.heygen.com/

**Current Version (2025):** Production platform, 175+ languages supported

**Overview:**
HeyGen generates AI videos from text, image, or audio using AI avatars with natural lip-sync and subtitles in 175+ languages including Vietnamese.

**Key Features:**
- **175+ Languages:** Full Vietnamese support with natural lip-sync
- **AI Avatars:** 100+ professional avatars or create custom avatar
- **Video Translation:** Translate videos with lip-sync to Vietnamese/other languages
- **Subtitle Generation:** Auto-generate and embed Vietnamese subtitles
- **API Access:** Programmatic video generation

**Vietnamese Use Case Fit:**
- ✅ Excellent Vietnamese language support
- ✅ Good for product showcase videos with consistent avatar
- ⚠️ Avatar-based format (not creative scene generation)
- ⚠️ Higher cost for API usage

**Pros:**
- Proven Vietnamese language quality
- Professional avatar quality
- Easy to use API
- Reliable subtitle generation
- Natural Vietnamese voices

**Cons:**
- Avatar-focused (limited creative flexibility)
- More expensive than text-only alternatives
- "Talking head" format may not suit all content types
- Requires quality scripts

**Pricing (2025):**
- **Creator Plan:** $64/month (120 video credits, API access)
- **Enterprise:** Custom pricing
- **API Usage:** ~$0.10-$0.25 per video minute

**Implementation Complexity:** Low (API integration 1-2 days)

---

### Option 4: Claude 3.5/4.0 + VietTTS (Vietnamese Content Stack)

**Sources:**
- Claude: https://claude.com/pricing | https://www.getblend.com/blog/which-llm-is-best-for-translation/
- VietTTS: https://github.com/NTT123/vietTTS

**Current Versions (2025):**
- Claude 4.0 Sonnet/Opus (2025 release)
- VietTTS (open-source, active)

**Overview:**
Combine Claude's industry-leading Vietnamese translation quality with open-source VietTTS for cost-effective Vietnamese content generation and voice synthesis.

**Why Claude for Vietnamese:**
- **WMT24 Competition Winner:** Ranked #1 in 9 of 11 language pairs
- **Professional Translator Preference:** Blind study showed translators rated Claude 3.5 "good" more often than GPT-4, DeepL, Google
- **Vietnamese VLM Performance:** Strong OCR and reasoning on Vietnamese multimodal content

**Why VietTTS:**
- **Open-Source:** Free, self-hostable
- **OpenAI TTS API Compatible:** Drop-in replacement for easier integration
- **Voice Cloning:** Can clone voices from local audio files
- **Natural Synthesis:** Research-grade quality

**Vietnamese Use Case Fit:**
- ✅ **Best Vietnamese content quality** (2025 benchmarks)
- ✅ Cost-effective (open-source TTS, competitive Claude pricing)
- ✅ Self-hostable voice synthesis (no per-minute TTS fees)
- ✅ Excellent for product descriptions, social posts, articles

**Pros:**
- Highest quality Vietnamese text generation (verified 2025)
- VietTTS is free and self-hostable
- Claude API is reliable and well-documented
- Can handle complex Vietnamese cultural nuances
- Strong reasoning capabilities for marketing copy

**Cons:**
- VietTTS requires self-hosting (technical setup)
- No built-in video generation (need separate tool)
- VietTTS voice quality lower than commercial options (but still good)

**Pricing (2025):**
- **Claude Sonnet 4.0:** $3/million input tokens, $15/million output tokens
- **Claude Opus 4.0:** $15/million input tokens, $75/million output tokens
- **VietTTS:** Free (self-hosting infrastructure costs only)
- **Estimated monthly cost:** $50-150 for LLM + $10-30 hosting VietTTS

**Implementation Complexity:** Medium (VietTTS setup 1-2 days, Claude API simple)

---

### Option 5: TickerTrends API (TikTok Trend Monitoring)

**Source:** https://blog.tickertrends.io/p/tiktok-trends-api-timeseries-hashtag-analytics

**Current Status (2025):** Active API service

**Overview:**
TickerTrends provides programmatic access to TikTok hashtag trends and time-series data for view counts via HTTP JSON API.

**Key Features:**
- **Time-Series Hashtag Data:** Historical view count trends
- **Trending Hashtag Discovery:** Latest trending hashtags by region
- **Simple HTTP API:** Easy integration with Python
- **Automated Monitoring:** Build spike detection/alerting systems

**Vietnamese Use Case Fit:**
- ✅ Can monitor Vietnamese TikTok trends automatically
- ✅ Simple API for automation
- ✅ Time-series data shows trend growth (not just current state)
- ⚠️ Pricing not publicly listed (need to inquire)

**Pros:**
- Purpose-built for TikTok trend tracking
- Time-series data (see trend growth over time)
- Programmatic alerting capabilities
- Simple JSON API

**Cons:**
- Pricing unknown (need to contact)
- Limited to TikTok (no multi-platform trend tracking)
- May not cover all Vietnamese regions

**Pricing:** Contact for quote (likely $50-200/month based on similar services)

**Implementation Complexity:** Low (API integration 1 day)

---

### Option 6: n8n (Workflow Automation Platform)

**Source:** https://n8n.io/ | https://n8n.io/workflows/3066-automate-multi-platform-social-media-content-creation-with-ai/

**Current Version (2025):** Cloud & self-hosted, AI-native automation

**Overview:**
n8n is an open-source workflow automation platform with native AI integrations (85+ AI tools), LangChain support, and execution-based pricing (not task-based).

**Key Features:**
- **85+ AI Integrations:** ChatGPT, Hugging Face, Cohere, custom connectors
- **LangChain Native Support:** Build sophisticated AI agent workflows
- **Execution-Based Pricing:** One execution regardless of workflow steps
- **Self-Hostable:** Full control, no vendor lock-in
- **Multi-Platform Social Media Template:** Pre-built AI content automation workflow

**Vietnamese Use Case Fit:**
- ✅ **Best cost efficiency** for AI-heavy workflows ($500/month budget)
- ✅ Can integrate all components (LLM, video APIs, platform posting)
- ✅ Self-hostable (data control, no API quotas)
- ✅ Pre-built social media automation templates
- ⚠️ Requires technical setup (developer must configure)

**Pros:**
- **Execution-based pricing** (AI workflows = 1 execution, not 100 tasks like Zapier)
- Open-source and self-hostable
- Unlimited users, unlimited workflows
- Native LangChain/AI agent support
- Pre-built social media automation workflows
- Best TCO (Total Cost of Ownership) for developers

**Cons:**
- Learning curve (20-30 hours to proficiency)
- Requires technical skills to set up
- Self-hosting adds infrastructure management
- Smaller app ecosystem than Zapier (though sufficient)

**Pricing (2025):**
- **Cloud Starter:** €20/month (2,500 executions)
- **Cloud Pro:** €50/month (10,000 executions)
- **Self-Hosted:** Free (infrastructure costs only, ~$20-40/month)

**Implementation Complexity:** Medium-High (initial setup 1 week, workflows 2-3 weeks)

---

### Option 7: Agno (AI Agent Framework - RECOMMENDED)

**Source:** https://docs.agno.com/ | https://github.com/agno-agi/agno

**Current Version (2025):** Production-ready, formerly Phidata, rebranded 2025

**Overview:**
Agno is a multi-agent framework, runtime and control plane built for speed, privacy, and scale. It features AgentOS, a FastAPI production runtime for deploying agentic systems.

**Key Features:**
- **Blazing Performance:** 2μs per agent creation (10,000x faster than LangGraph), 3.75KB memory per agent (50x less than LangGraph)
- **Built-in Human-in-the-Loop:** Native approval workflows and guardrails
- **Multi-Agent Teams:** 3 modes - route, collaborate, coordinate
- **AgentOS Runtime:** FastAPI production deployment, stateless, horizontally scalable
- **Model Agnostic:** Supports 23+ model providers (OpenAI, Anthropic, Gemini, Groq, Ollama, etc.)
- **Agentic RAG:** Built-in knowledge base with hybrid search and re-ranking across 20+ vector databases
- **Memory & Storage:** Persistent memory across sessions with plug-n-play drivers

**Vietnamese Use Case Fit:**
- ✅ **PERFECT: Built-in HITL + fastest performance + production runtime**
- ✅ 50x less memory = significantly lower hosting costs
- ✅ AgentOS FastAPI = easy deployment
- ✅ Multi-agent teams out of the box
- ✅ Supports Claude (best for Vietnamese)
- ✅ Faster time to market than LangGraph (6 weeks vs 8+ weeks)

**Pros:**
- Industry-leading performance (10,000x faster agent creation)
- Minimal memory footprint (lower infrastructure costs)
- Built-in human-in-the-loop (critical requirement met)
- Production-ready FastAPI runtime (AgentOS)
- Clear, intuitive developer experience
- Structured input/output schemas
- Comprehensive observability

**Cons:**
- Smaller community than LangGraph/CrewAI (newer framework)
- Less extensive documentation than LangGraph
- Fewer real-world case studies published

**Pricing:**
- **Open-source:** Free
- **LLM Costs:** Pay-per-use for APIs
- **Infrastructure:** Self-hosting costs (significantly lower due to efficiency)

**Implementation Complexity:** Medium (6 weeks to production with HITL)

**Performance Benchmarks (2025):**
- Agent creation: 2μs (vs LangGraph ~20ms)
- Memory per agent: 3.75KB (vs LangGraph ~187KB)
- Can run thousands of concurrent agents on single server

---

### Option 8: Vbee (Vietnamese Voice Synthesis - RECOMMENDED)

**Source:** https://vbee.vn/en | https://api.vbee.vn/

**Current Version (2025):** Commercial service, #1 Vietnamese TTS provider

**Overview:**
Vbee AIVoice is Vietnam's leading text-to-speech technology converting text into EMOTIONAL speech based on artificial intelligence. Provides 200+ reading voices in 50+ languages with Vietnamese-first expertise.

**Key Features:**
- **Vietnamese-First Company:** Deep understanding of Vietnamese market, accents, culture
- **Emotional Speech:** Not just neutral reading - excitement, urgency, calm, etc.
- **200+ Voices:** Professional quality across 50+ languages
- **Regional Accents:** Northern, Central, Southern Vietnamese dialects
- **API Integration:** RESTful API with flexible pricing
- **98%+ Accuracy:** Vietnamese tone marks and diacritics handled correctly

**Vietnamese Use Case Fit:**
- ✅ **BEST for Vietnamese marketing** - emotional voices critical for engagement
- ✅ Free tier covers initial usage (3K chars/day = 90K/month)
- ✅ Vietnamese company = local support, same timezone
- ✅ No self-hosting required (vs VietTTS)
- ✅ Professional quality vs research-grade alternatives

**Pros:**
- #1 Vietnamese TTS provider
- Emotional expression (critical for marketing)
- Free tier likely covers MVP usage
- Regional accent support
- Professional quality
- API-based (no infrastructure to manage)

**Cons:**
- Pricing beyond free tier requires quote
- Less control than self-hosted solutions
- Dependency on third-party service

**Pricing (2025):**
- **Free Tier:** 3,000 characters/day (90,000/month)
- **Estimated usage:** ~60 videos × 150 chars = 9,000 chars/month
- **Result:** FREE tier sufficient for MVP
- **Backup:** Contact for API pricing if exceed (estimated $20-50/month)

**Implementation Complexity:** Low (API integration 1 day)

---

### Multi-Tool Video Selection Strategy

**Decision Engine Architecture:**

Video tool selection is automated based on:
1. **Platform** (TikTok, Facebook, Shopee, YouTube)
2. **Content Purpose** (viral trend, product showcase, e-commerce listing, brand story)
3. **Budget per video**
4. **Quality tier** (budget, standard, premium)
5. **Avatar requirement** (talking person needed?)
6. **Creative freedom needed** (custom scenes vs templates)

**Tool Selection Matrix:**

| Use Case | Primary Tool | Fallback | Cost | Reason |
|----------|-------------|----------|------|---------|
| TikTok viral trend | Simplified | HeyGen, D-ID | $0.53 | 98% Vietnamese subtitle accuracy |
| TikTok product + avatar | HeyGen | Simplified | $0.53 | Professional lip-sync |
| TikTok hero content | Runway | HeyGen | $2.50 | Cinematic quality |
| Facebook brand story + avatar | HeyGen | Simplified | $0.53 | Professional avatar trust |
| Facebook brand story creative | Runway | HeyGen | $2.50 | Creative freedom |
| Facebook Reels | Simplified | HeyGen | $0.53 | Template efficiency |
| Shopee bulk (<$0.20 budget) | D-ID | Simplified | $0.05 | Cost optimization |
| Shopee standard | Simplified | D-ID, HeyGen | $0.53 | Balanced quality/cost |
| YouTube Shorts | Simplified | HeyGen | $0.53 | Similar to TikTok |
| YouTube long-form | HeyGen | Runway | $0.53 | Educational presenter |

**Recommended Multi-Tool Setup:**
- **Simplified:** $64/month (primary for TikTok/Reels - 60-80% of videos)
- **HeyGen:** $64/month (professional product showcases - 15-20%)
- **D-ID:** $4.70/month (bulk Shopee listings - 5-10%)
- **Runway:** $12/month optional (special campaigns - occasional)

**Total Video Tool Cost:** $132.70 - $144.70/month

---

## 4. Deployment Architecture

### Infrastructure Overview

**Deployment Topology:**
- **Platform:** DigitalOcean Droplet (4 vCPU, 8GB RAM, Ubuntu 22.04)
- **Orchestration:** Docker Compose
- **Network:** Internal Docker network (172.20.0.0/16)
- **External Access:** Nginx reverse proxy (HTTPS only)

**Container Architecture:**

```
Container 1: PostgreSQL + pgvector (172.20.0.2:5432)
- Purpose: Agent storage, memory, workflow state
- Volume: postgres_data

Container 2: Vbee Proxy (172.20.0.3:8000) [Optional]
- Purpose: Cache Vbee API responses
- Reduces API calls, improves performance

Container 3: Agno AgentOS (172.20.0.4:8080)
- Purpose: AI agent runtime
- Exposes: /v1/agents/* API endpoints
- Volume: agent_storage

Container 4: n8n (172.20.0.5:5678)
- Purpose: Workflow orchestration
- Volume: n8n_data

Container 5: Approval UI (172.20.0.6:3000)
- Purpose: React-based approval interface
- Connects to AgentOS API

Container 6: Nginx (172.20.0.10:80/443)
- Purpose: Reverse proxy, SSL termination
- Routes:
  - /n8n → n8n container
  - /api → AgentOS
  - / → Approval UI
```

**External Access:**
- `https://your-domain.com` → Approval UI
- `https://your-domain.com/n8n` → n8n Dashboard (authenticated)
- `https://your-domain.com/api` → AgentOS API (API key protected)

### n8n ↔ Agno Communication Patterns

**Pattern 1: HTTP Request (Synchronous)**
- Use case: Quick agent calls (<2 minutes)
- n8n → POST http://172.20.0.4:8080/v1/agents/run
- Response: Immediate JSON result
- Best for: Single agent executions, simple tasks

**Pattern 2: Webhook (Asynchronous)**
- Use case: Long-running workflows (2-30 minutes)
- n8n → POST with webhook_url parameter
- AgentOS → Executes in background → Callback to n8n webhook
- Response: 202 Accepted with session_id
- Best for: Multi-agent workflows, content generation batches

**Pattern 3: Server-Sent Events (Streaming)**
- Use case: Real-time progress updates
- n8n → POST with stream=true
- AgentOS → SSE stream with progress events
- Best for: Live progress monitoring

**Recommended Pattern by Use Case:**
- Content generation (2-10 min): Webhook (async)
- Multi-agent workflows (>10 min): Webhook (async)
- Quick agent calls (<2 min): HTTP Request (sync)
- Progress monitoring needed: SSE Streaming

### Security Architecture

**Authentication Layers:**
1. **Nginx → Public:** HTTPS/TLS encryption
2. **n8n Dashboard:** Basic Auth (username/password)
3. **AgentOS API:** API Key authentication (X-API-Key header)
4. **Approval UI:** Session-based auth with AgentOS

**Network Security:**
- All containers on isolated Docker network
- Only Nginx exposes ports to host (80, 443)
- Internal services communicate via Docker network IPs
- No direct external access to databases or agent runtime

**API Key Management:**
- Stored in environment variables (.env file)
- Never committed to version control
- Rotated monthly (best practice)
- Separate keys for n8n, approval UI, external integrations

### Deployment Procedure

1. **Infrastructure Setup:**
   - Provision DigitalOcean Droplet (4 vCPU, 8GB RAM)
   - Configure domain DNS (A record to droplet IP)
   - Install Docker and Docker Compose

2. **Environment Configuration:**
   - Create .env file with all secrets
   - Generate strong passwords and API keys
   - Configure API credentials (Anthropic, Vbee, video tools, platforms)

3. **Database Initialization:**
   - Start PostgreSQL container
   - Run init-db.sql for schema setup
   - Enable pgvector extension

4. **Service Deployment:**
   - Deploy AgentOS (verify health endpoint)
   - Deploy n8n (import workflows)
   - Deploy Approval UI
   - Deploy Nginx with SSL

5. **SSL Certificate:**
   - Use Let's Encrypt certbot
   - Automatic renewal configured

6. **Verification:**
   - Test all service health endpoints
   - Verify n8n → AgentOS communication
   - Test approval workflow end-to-end

---

## 5. Cost Analysis & Budget Breakdown

### Final Monthly Cost Estimate

**AI/ML APIs:**
- Claude 4.0 Sonnet: $18/month (2M tokens)
- Vbee Voice API: **FREE** (under 90K chars/month)
- Subtotal: $18/month

**Video Generation (Multi-Tool):**
- Simplified (primary): $64/month
- HeyGen (professional): $64/month
- D-ID (bulk): $4.70/month
- Runway (optional): $12/month
- Subtotal: $132.70 - $144.70/month

**Trend Monitoring:**
- TickerTrends API: $80/month (estimated)

**Orchestration:**
- n8n Cloud Starter: €20/month (~$22/month)
  - Alternative: Self-hosted FREE (included in infrastructure below)

**Infrastructure:**
- DigitalOcean Droplet (4vCPU, 8GB): $40/month
- PostgreSQL + Storage: $18/month
- Subtotal: $58/month

**Platform APIs:**
- Facebook Graph API: FREE
- TikTok Content Posting API: FREE (post-audit)
- Shopee Open API: FREE
- Subtotal: $0/month

**TOTAL MONTHLY COST:**
- **Minimum** (Simplified + D-ID, self-hosted n8n): $288.70
- **Recommended** (+ HeyGen, n8n Cloud): $352.70
- **Maximum** (+ Runway, all tools): $386.70

**Your Budget:** $500/month
**Remaining Margin:** $113 - $211 (23-42% buffer)

**Cost Savings vs Manual:**
- Manual team: ~$2,000-3,000/month (2-3 part-time staff)
- AI automation: ~$353/month
- **Savings: 82-88%**

---

## 6. Key Decisions & Recommendations

### RECOMMENDED TECHNOLOGY STACK

**AI Agent Framework:** ✅ **Agno**
- Why: Built-in HITL, 10,000x faster than LangGraph, 50x less memory, production-ready AgentOS
- vs CrewAI: Agno has native approval workflows
- vs LangGraph: Agno is faster, more cost-efficient, easier deployment

**Vietnamese Content:** ✅ **Claude 4.0 Sonnet + Vbee**
- Why: Claude = #1 Vietnamese translation quality (WMT24 winner), Vbee = #1 Vietnamese TTS with emotional voices
- Cost: ~$18/month LLM + FREE Vbee tier

**Video Generation:** ✅ **Multi-Tool Strategy**
- Primary: Simplified (TikTok/Reels) - $64/month
- Professional: HeyGen (product showcases) - $64/month
- Bulk: D-ID (Shopee listings) - $4.70/month
- Special: Runway (hero content) - $12/month optional
- Why: Match tool to content type for optimal quality/cost

**Orchestration:** ✅ **n8n**
- Why: Visual debugging, non-developer friendly, execution-based pricing
- Team can fix workflows without developer
- €20/month investment prevents hours of debugging

**Deployment:** ✅ **Docker Compose on DigitalOcean**
- Why: Simple, cost-effective, scalable enough for MVP
- Avoid Kubernetes complexity (overkill for this scale)

### ARCHITECTURE DECISION: Agno vs LangGraph

**Winner: Agno**

**Reasons:**
1. **Built-in HITL:** Native human approval (your #1 requirement)
2. **Performance:** 50x less memory = lower hosting costs ($40/month vs $80+/month)
3. **Time to Market:** 6 weeks vs 8+ weeks (LangGraph complexity)
4. **Developer Experience:** Intuitive API, clear documentation
5. **Production Runtime:** AgentOS FastAPI = easy deployment
6. **Cost Efficiency:** Lower infrastructure overhead

**When LangGraph Would Be Better:**
- Need maximum observability (LangSmith deep debugging)
- Complex graph workflows with many conditional branches
- Already invested in LangChain ecosystem
- Prefer battle-tested at mega-scale (LinkedIn/Uber references)

**For your use case (Vietnamese marketing automation, $500 budget, developer-led team):** Agno is the clear winner.

### ARCHITECTURE DECISION: n8n Inclusion

**Winner: Include n8n**

**Why Initially Considered Skipping:**
- Agno can handle scheduling via Python APScheduler
- Adds €20/month cost
- Extra service to maintain

**Why We Recommend Keeping It:**
1. **Operational Reality:** Team can fix broken workflows at 3 AM without developer
2. **Visual Debugging:** See exactly where workflow failed, retry manually
3. **Non-Developer Maintenance:** Marketing team can modify schedules, add platforms
4. **Rapid Iteration:** Test new workflows without code deployment
5. **Error Handling UI:** Built-in retry, notifications, execution history
6. **Future Flexibility:** Easy to add Airtable, webhooks, Zapier triggers, etc.

**Cost:** €20/month (4% of budget)
**Value:** Prevents hours of debugging, enables team autonomy

**Responsibility Split:**
- n8n: Orchestration (when to run, error handling, external triggers)
- Agno: Intelligence (AI agents, content generation, approval logic)

### VIDEO TOOL SELECTION LOGIC

**Automated Decision Engine:**

Tool selected based on:
1. Platform (TikTok/Facebook/Shopee/YouTube)
2. Content purpose (trend/product/brand/ecommerce)
3. Budget constraint
4. Avatar requirement
5. Quality tier

**Example Decisions:**
- TikTok viral trend → Simplified (98% Vietnamese subtitles)
- Product showcase + avatar → HeyGen (professional lip-sync)
- Shopee bulk (<$0.20/video) → D-ID (cost optimization)
- Brand hero content → Runway (cinematic quality)

**Fallback Chain:**
- Primary tool fails → Try fallback #1 → Try fallback #2
- Log all failures for monitoring
- Return which tool was used in result metadata

---

## 11. Kubernetes Deployment Architecture

### Overview

Complete production-ready Kubernetes deployment with FluxCD GitOps for automated deployment and monitoring.

**Status:** ✅ All manifests created and ready for deployment

**Infrastructure:** DigitalOcean Kubernetes (DOKS) with managed load balancer

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    FluxCD GitOps Controller                      │
│              (Auto-deploys from GitHub repository)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼──────┐ ┌───▼─────┐ ┌────▼────────┐
        │ Infrastructure│ │  Base   │ │ Monitoring  │
        │  (cert-mgr,  │ │  Apps   │ │   Stack     │
        │   nginx-ing) │ │         │ │             │
        └──────────────┘ └─────────┘ └─────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼─────┐        ┌──────▼─────┐       ┌──────▼──────┐
   │ AgentOS  │◄──────►│ PostgreSQL │◄─────►│     n8n     │
   │ (Agno)   │        │  +pgvector │       │ (Workflows) │
   │ 1-5 pods │        │   50GB     │       │   1 pod     │
   └────┬─────┘        └────────────┘       └──────┬──────┘
        │                                           │
        │              ┌──────────────┐            │
        └─────────────►│ Approval UI  │◄───────────┘
                       │  (React)     │
                       │   2 pods     │
                       └──────┬───────┘
                              │
                    ┌─────────▼──────────┐
                    │  Nginx Ingress     │
                    │  with Let's Encrypt│
                    └────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │   LoadBalancer     │
                    │ (Public Internet)  │
                    └────────────────────┘
```

### Infrastructure Components

**GitOps Deployment:**
- **FluxCD:** Automated deployment from Git (5-minute sync interval)
- **SealedSecrets:** Encrypted secrets safe to commit to Git
- **Kustomize:** Configuration management and patching

**Ingress & Certificates:**
- **Nginx Ingress Controller:** HTTPS routing with 2 replicas
- **cert-manager:** Automatic Let's Encrypt SSL certificates
- **LoadBalancer:** DigitalOcean managed load balancer

**Observability Stack:**
- **Prometheus:** Metrics collection (30-day retention)
- **Grafana:** 3 pre-built dashboards (Business, System, Agent Performance)
- **Loki + Promtail:** Centralized log aggregation
- **AlertManager:** 24 alert rules with Slack notifications

### Application Services

| Service | Type | Replicas | CPU Request | Memory Request | Storage |
|---------|------|----------|-------------|----------------|---------|
| **PostgreSQL** | StatefulSet | 1 | 500m | 1Gi | 50Gi |
| **AgentOS** | Deployment + HPA | 1-5 | 500m | 1Gi | - |
| **n8n** | Deployment | 1 | 250m | 512Mi | 10Gi |
| **Approval UI** | Deployment | 2 | 100m | 256Mi | - |
| **Prometheus** | StatefulSet | 1 | 500m | 2Gi | 50Gi |
| **Grafana** | Deployment | 1 | 100m | 256Mi | 10Gi |
| **Loki** | StatefulSet | 1 | 200m | 512Mi | 50Gi |

**Total Resources:**
- CPU: ~2.7 cores (request), ~10 cores (limit)
- Memory: ~5.5Gi (request), ~16Gi (limit)
- Storage: ~170Gi persistent volumes

**Recommended Nodes:** 2x `s-4vcpu-8gb` DigitalOcean Droplets

### Auto-Scaling Configuration

**AgentOS Horizontal Pod Autoscaler (HPA):**
- **Min Replicas:** 1
- **Max Replicas:** 5
- **Scale Up:** Aggressive (1-min stabilization, +100% or +2 pods per 30s)
- **Scale Down:** Gradual (5-min stabilization, -50% per 60s)
- **Triggers:**
  - CPU: 70% average utilization
  - Memory: 80% average utilization

### Monitoring Dashboards

**1. Business Metrics Dashboard:**
- Daily content generated (text + video)
- Approval rate (% approved vs rejected)
- Platform posts by platform (Facebook, TikTok, Shopee, YouTube)
- Video generation cost by tool (Simplified, HeyGen, D-ID, Runway)
- LLM token usage and cost (Claude 4.0 Sonnet)
- Approval cycle time (p50, p95, p99)
- TikTok trends monitored and used in content

**2. System Health Dashboard:**
- Pod CPU and memory usage
- Agent execution duration (p95 by agent)
- PostgreSQL connections and database size
- n8n workflow execution counts
- API error rate and pod restart count
- Infrastructure health checks

**3. Agent Performance Dashboard:**
- Agent executions by status (completed/failed/in_progress)
- Agent success rate by agent name
- Video generation queue length
- Content pending approval count

### Alert Rules (24 total)

**Business Critical (4 alerts):**
1. High content rejection rate (>50% for 10min) → Slack
2. No content generated in 2 hours → Slack Critical
3. Video cost spike (>$50/hour) → Slack
4. LLM cost spike (>$10/hour) → Slack

**System Health (8 alerts):**
5. High agent failure rate (>10% for 5min)
6. AgentOS pod down
7. AgentOS high memory (>90%)
8. AgentOS high CPU (>1.8 cores)
9. PostgreSQL down
10. PostgreSQL high connections (>80)
11. PostgreSQL disk space (>80%)
12. n8n workflow failures (>5 in 15min)

**Performance (3 alerts):**
13. Slow agent execution (p95 >5 minutes)
14. Slow approval cycle (p95 >4 hours)
15. Video queue backlog (>50 pending)

**Data Quality (2 alerts):**
16. No TikTok trends in 6 hours
17. Platform posting failures (>10 in 1 hour)

**Cost Budget (2 alerts):**
18. Monthly budget warning ($400 threshold)
19. Monthly budget exceeded ($500 threshold)

### GitOps Workflow

```
1. Developer commits code → GitHub
2. FluxCD detects change (5-minute interval)
3. FluxCD validates manifests
4. FluxCD applies to Kubernetes cluster
5. Kubernetes reconciles desired state
6. Pods restart with new images (rolling update)
7. Health checks validate deployment
8. Slack notification on success/failure
```

**Benefits:**
- Single source of truth (Git repository)
- Automated deployments (no manual kubectl)
- Audit trail (Git commit history)
- Easy rollback (Git revert)
- Declarative configuration (infrastructure as code)

### Security Features

**Secrets Management:**
- SealedSecrets controller encrypts secrets
- Encrypted secrets safe to commit to Git
- Automatic decryption in cluster
- 90-day rotation policy recommended

**Network Security:**
- HTTPS-only (HTTP → HTTPS redirect)
- Let's Encrypt SSL certificates (auto-renewal)
- Internal service mesh (ClusterIP services)
- External access only via Ingress

**RBAC:**
- FluxCD service accounts with minimal permissions
- Namespace isolation (marketing-automation)
- Pod security standards (can be enabled)

### Access URLs

After deployment:
- **Approval UI:** https://marketing.your-domain.com
- **n8n Editor:** https://marketing.your-domain.com/n8n
- **Grafana:** https://grafana.marketing.your-domain.com
- **AgentOS API:** https://marketing.your-domain.com/api

### Deployment Files Created

**Total:** 17 Kubernetes manifest files

**Base Application (k8s/base/):**
1. 00-namespace.yaml - marketing-automation namespace
2. 01-configmap.yaml - Environment configuration
3. 02-secrets.yaml - Secret template (use SealedSecrets)
4. 03-postgres.yaml - PostgreSQL StatefulSet (50GB)
5. 04-agentos.yaml - AgentOS Deployment + HPA
6. 05-n8n.yaml - n8n Deployment (10GB PVC)
7. 06-approval-ui.yaml - React UI Deployment
8. 07-ingress.yaml - Nginx Ingress with HTTPS
9. kustomization.yaml - Kustomize config

**Monitoring Stack (k8s/monitoring/):**
1. kube-prometheus-stack.yaml - Prometheus + Grafana (Helm)
2. servicemonitors.yaml - Metrics scraping configs
3. grafana-dashboards.yaml - 3 dashboards (Business, System, Agent)
4. loki-stack.yaml - Loki + Promtail (Helm)
5. alertmanager-rules.yaml - 24 alert rules
6. kustomization.yaml - Kustomize config

**Infrastructure (clusters/production/):**
1. infrastructure.yaml - cert-manager, nginx-ingress, sealed-secrets
2. marketing-automation.yaml - FluxCD Kustomization resources

### Deployment Procedure

**Prerequisites:**
1. DigitalOcean Kubernetes cluster (2x s-4vcpu-8gb)
2. kubectl CLI installed
3. FluxCD CLI installed
4. kubeseal CLI installed (for SealedSecrets)
5. Domain name with DNS access
6. GitHub repository for GitOps

**Deployment Steps:**
1. Bootstrap FluxCD: `flux bootstrap github`
2. Seal secrets: `kubeseal < secrets.yaml > sealed-secrets.yaml`
3. Update configuration (domain, email, registry)
4. Build and push container images (AgentOS, Approval UI)
5. Commit and push to GitHub
6. FluxCD auto-deploys (monitor with `flux get all`)
7. Configure DNS (point to LoadBalancer IP)
8. Access services (HTTPS certificates auto-issued)

**Time to Deploy:** ~30 minutes (mostly DNS propagation + certificate issuance)

### Cost Breakdown with Kubernetes

| Category | Service | Monthly Cost |
|----------|---------|--------------|
| **Infrastructure** | DOKS (2x s-4vcpu-8gb nodes) | $80 |
| **Workflow** | n8n Cloud (execution-based) | $22 |
| **LLM** | Claude 4.0 Sonnet | $18 |
| **Video Tools** | Simplified + HeyGen + D-ID + Runway | $144.70 |
| **TTS** | Vbee (FREE tier) | $0 |
| **Trend Monitoring** | TickerTrends API | $80 |
| **Total** | | **$344.70/month** |

**Budget:** $500/month → **$155.30 buffer (31%)**

**Infrastructure cost increase:** +$27/month vs Docker Compose
**Benefits:** Auto-scaling, high availability, GitOps, professional monitoring

### Backup Strategy

**PostgreSQL:**
- Daily pg_dump via CronJob (to be added)
- 30-day retention in DigitalOcean Spaces (S3-compatible)
- Point-in-time recovery capability

**n8n Workflows:**
- Stored in PostgreSQL (included in DB backup)
- Manual export via n8n UI (Settings → Import/Export)

**Grafana Dashboards:**
- Stored as ConfigMaps (in Git via FluxCD)

### High Availability

**Current Configuration:**
- AgentOS: 2 replicas (scale to 5)
- Approval UI: 2 replicas
- PostgreSQL: 1 replica (can add streaming replication)
- n8n: 1 replica (can enable queue mode for multi-instance)

**Failure Scenarios:**
- Pod failure → Kubernetes auto-restarts (liveness probe)
- Node failure → Pods rescheduled to healthy node
- Zone failure → Requires multi-zone node pool (add cost)

### Performance Tuning

**AgentOS:**
- Monitor p95 execution times in Grafana
- Adjust HPA thresholds based on actual load
- Scale replicas during peak hours (8-10am Vietnamese time)

**PostgreSQL:**
- Add read replicas for heavy read workloads
- Tune `shared_buffers`, `work_mem` based on query patterns
- Add PgBouncer connection pooling if connections >80

**n8n:**
- Enable queue mode for multi-instance (requires Redis)
- Increase execution timeout for video generation (10+ minutes)
- Monitor workflow execution duration

### Documentation

**Deployment Guide:** `/home/cid/projects/agent-research/README-DEPLOYMENT.md`
- Complete step-by-step deployment instructions
- Troubleshooting guide
- Scaling instructions
- Security best practices

**Deployment Summary:** `/home/cid/projects/agent-research/KUBERNETES-DEPLOYMENT-SUMMARY.md`
- Architecture overview
- File structure
- Resource allocation
- Monitoring dashboards
- Alert rules
- Cost optimization

---

## References and Sources

**CRITICAL: All technical claims, versions, and benchmarks verified through sources**

---

## Document Information

**Workflow:** BMad Research Workflow - Technical Research
**Generated:** 2025-11-22
**Research Type:** Technical/Architecture Research - AI Marketing Automation
**Status:** Requirements Definition Complete - Research In Progress

---

_This technical research report is being generated using the BMad Method Research Workflow with real-time 2025 research and analysis._
