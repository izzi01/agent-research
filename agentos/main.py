"""
AgentOS Main Application - FastAPI server for Vietnamese Marketing Automation

This application provides:
1. REST API endpoints for agent execution
2. Human-in-the-loop approval workflows
3. Webhook receivers for n8n integration
4. Prometheus metrics for monitoring
5. Health checks and readiness probes
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import logging
import os
from datetime import datetime

# Import our agents and workflows
from workflows.trend_to_content import TrendToContentWorkflow
from agents.text_creator import TextCreator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Vietnamese Marketing Automation - AgentOS",
    description="AI agent system for automating Vietnamese e-commerce marketing",
    version="1.0.0"
)

# CORS middleware for Approval UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify actual domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
agent_executions_total = Counter(
    'agent_executions_total',
    'Total number of agent executions',
    ['agent_name', 'status']
)

agent_execution_duration = Histogram(
    'agent_execution_duration_seconds',
    'Agent execution duration in seconds',
    ['agent_name']
)

content_approval_total = Counter(
    'content_approval_total',
    'Total content approvals',
    ['decision']
)

approval_cycle_time = Histogram(
    'approval_cycle_time_seconds',
    'Time from content generation to approval decision',
    buckets=[300, 600, 1800, 3600, 7200, 14400, 28800]
)

content_pending_approval = Gauge(
    'content_pending_approval_count',
    'Number of content items awaiting approval'
)

platform_posts_total = Counter(
    'platform_posts_total',
    'Total posts published to platforms',
    ['platform', 'status']
)

video_generation_cost = Counter(
    'video_generation_cost_usd',
    'Video generation cost in USD',
    ['tool']
)

llm_tokens_used = Counter(
    'llm_tokens_used_total',
    'Total LLM tokens consumed',
    ['provider', 'model', 'type']
)

trends_monitored_total = Counter(
    'trends_monitored_total',
    'Total trends monitored',
    ['source']
)

trends_used_in_content_total = Counter(
    'trends_used_in_content_total',
    'Trends used in content generation'
)

# Global workflow and agent instances
workflow = None
text_creator = None

# In-memory storage for demo (use PostgreSQL in production)
pending_approvals = []
approved_content = []
generated_copy = []


# Pydantic models for API
class TrendScanRequest(BaseModel):
    product_categories: List[str]
    min_relevance_score: float = 0.6
    max_briefs: int = 10


class TrendScanResponse(BaseModel):
    workflow_id: str
    status: str
    trends_discovered: int
    content_briefs_created: int
    briefs: List[Dict]


class ApprovalRequest(BaseModel):
    brief_id: str
    approved: bool
    feedback: Optional[str] = ""


class ApprovalResponse(BaseModel):
    brief_id: str
    approved: bool
    approved_at: str


class PublishRequest(BaseModel):
    brief_id: str
    platforms: List[str]  # ["facebook", "tiktok", "shopee"]
    scheduled_time: Optional[str] = None


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize agents and workflows on startup"""
    global workflow, text_creator

    logger.info("Starting AgentOS application...")

    # Get configuration from environment
    db_url = os.getenv("DATABASE_URL", "postgresql://agno:password@postgres-service:5432/marketing_automation")
    tickertrends_api_key = os.getenv("TICKERTRENDS_API_KEY", "demo_key")

    # Initialize workflow
    try:
        workflow = TrendToContentWorkflow(
            db_url=db_url,
            tickertrends_api_key=tickertrends_api_key
        )
        logger.info("✅ Workflow initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize workflow: {e}")
        raise

    # Initialize TextCreator agent
    try:
        text_creator = TextCreator(db_url=db_url)
        logger.info("✅ TextCreator agent initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize TextCreator: {e}")
        raise

    logger.info("🚀 AgentOS is ready!")


# Health check endpoints
@app.get("/health")
async def health_check():
    """Liveness probe - is the application running?"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/ready")
async def readiness_check():
    """Readiness probe - is the application ready to serve requests?"""
    if workflow is None:
        raise HTTPException(status_code=503, detail="Workflow not initialized")

    return {
        "status": "ready",
        "workflow_initialized": workflow is not None,
        "timestamp": datetime.now().isoformat()
    }


# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Main API endpoints
@app.post("/api/v1/trends/scan", response_model=TrendScanResponse)
async def scan_trends(request: TrendScanRequest, background_tasks: BackgroundTasks):
    """
    Scan TikTok trends and create content briefs

    This endpoint:
    1. Discovers trending TikTok topics
    2. Matches trends to products
    3. Creates Vietnamese content briefs
    4. Queues briefs for approval
    """
    logger.info(f"Received trend scan request: {request.dict()}")

    try:
        # Track metrics
        agent_executions_total.labels(agent_name="TrendMonitor", status="started").inc()

        # Run workflow
        with agent_execution_duration.labels(agent_name="TrendMonitor").time():
            results = workflow.run_daily_content_generation(
                product_categories=request.product_categories,
                min_relevance_score=request.min_relevance_score,
                max_briefs_per_day=request.max_briefs
            )

        # Update metrics
        agent_executions_total.labels(agent_name="TrendMonitor", status="completed").inc()
        trends_monitored_total.labels(source="tiktok").inc(results["trends_discovered"])
        trends_used_in_content_total.inc(results["content_briefs_created"])

        # Queue briefs for approval
        for brief in results["briefs"]:
            brief["created_at"] = datetime.now().isoformat()
            brief["status"] = "pending_approval"
            pending_approvals.append(brief)

        content_pending_approval.set(len(pending_approvals))

        logger.info(f"✅ Workflow completed: {results['content_briefs_created']} briefs created")

        return TrendScanResponse(
            workflow_id=results["workflow_id"],
            status=results["status"],
            trends_discovered=results["trends_discovered"],
            content_briefs_created=results["content_briefs_created"],
            briefs=results["briefs"]
        )

    except Exception as e:
        logger.error(f"❌ Trend scan failed: {str(e)}", exc_info=True)
        agent_executions_total.labels(agent_name="TrendMonitor", status="failed").inc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/approvals/pending")
async def get_pending_approvals():
    """Get all content briefs awaiting approval"""
    return {
        "count": len(pending_approvals),
        "briefs": pending_approvals
    }


@app.post("/api/v1/approvals/submit", response_model=ApprovalResponse)
async def submit_approval(request: ApprovalRequest):
    """
    Submit approval decision for a content brief

    This implements the human-in-the-loop workflow
    """
    logger.info(f"Approval received: {request.dict()}")

    # Find the brief
    brief = None
    for i, b in enumerate(pending_approvals):
        # In mock, use trend_id as brief_id
        if b.get("trend_id") == request.brief_id:
            brief = pending_approvals.pop(i)
            break

    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")

    # Calculate approval cycle time
    created_at = datetime.fromisoformat(brief["created_at"])
    approval_time = (datetime.now() - created_at).total_seconds()
    approval_cycle_time.observe(approval_time)

    # Update metrics
    content_approval_total.labels(decision="approved" if request.approved else "rejected").inc()
    content_pending_approval.set(len(pending_approvals))

    # Process approval
    brief["status"] = "approved" if request.approved else "rejected"
    brief["approved_at"] = datetime.now().isoformat()
    brief["feedback"] = request.feedback

    if request.approved:
        approved_content.append(brief)
        logger.info(f"✅ Brief approved: {request.brief_id}")
    else:
        logger.info(f"❌ Brief rejected: {request.brief_id} - Reason: {request.feedback}")

    return ApprovalResponse(
        brief_id=request.brief_id,
        approved=request.approved,
        approved_at=brief["approved_at"]
    )


@app.post("/api/v1/content/generate-copy")
async def generate_copy(brief_id: str, platforms: List[str], generate_variants: bool = False):
    """
    Generate Vietnamese social media copy from approved content brief

    This endpoint:
    1. Takes an approved content brief
    2. Generates platform-specific Vietnamese copy
    3. Validates character limits and formatting
    4. Returns copy ready for publishing
    """
    logger.info(f"Copy generation request: brief_id={brief_id}, platforms={platforms}, variants={generate_variants}")

    # Find approved brief
    brief = None
    for b in approved_content:
        if b.get("trend_id") == brief_id:
            brief = b
            break

    if not brief:
        raise HTTPException(status_code=404, detail="Approved brief not found")

    try:
        # Track metrics
        agent_executions_total.labels(agent_name="TextCreator", status="started").inc()

        # Generate copy
        with agent_execution_duration.labels(agent_name="TextCreator").time():
            results = text_creator.run_copy_generation(
                brief=brief,
                platforms=platforms,
                generate_variants=generate_variants
            )

        # Update metrics
        agent_executions_total.labels(agent_name="TextCreator", status="completed").inc()

        # Store generated copy
        results["brief_id"] = brief_id
        results["status"] = "ready_for_publish"
        generated_copy.append(results)

        logger.info(f"✅ Copy generated for {len(platforms)} platforms")

        return results

    except Exception as e:
        logger.error(f"❌ Copy generation failed: {str(e)}", exc_info=True)
        agent_executions_total.labels(agent_name="TextCreator", status="failed").inc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/content/publish")
async def publish_content(request: PublishRequest):
    """
    Publish approved content to platforms

    This would integrate with platform APIs (Facebook, TikTok, Shopee)
    """
    logger.info(f"Publish request: {request.dict()}")

    # Find approved content
    brief = None
    for b in approved_content:
        if b.get("trend_id") == request.brief_id:
            brief = b
            break

    if not brief:
        raise HTTPException(status_code=404, detail="Approved content not found")

    # Mock publishing (in production: call platform APIs)
    results = []
    for platform in request.platforms:
        try:
            # Simulate API call
            logger.info(f"Publishing to {platform}...")

            # Update metrics
            platform_posts_total.labels(platform=platform, status="success").inc()

            results.append({
                "platform": platform,
                "status": "published",
                "post_id": f"{platform}_{datetime.now().timestamp()}",
                "url": f"https://{platform}.com/post/mock_id"
            })

        except Exception as e:
            logger.error(f"Failed to publish to {platform}: {e}")
            platform_posts_total.labels(platform=platform, status="failed").inc()
            results.append({
                "platform": platform,
                "status": "failed",
                "error": str(e)
            })

    return {
        "brief_id": request.brief_id,
        "platforms": request.platforms,
        "results": results,
        "published_at": datetime.now().isoformat()
    }


# Webhook endpoint for n8n integration
@app.post("/webhooks/n8n/trigger")
async def n8n_webhook(payload: Dict):
    """
    Webhook receiver for n8n workflows

    Example payload from n8n scheduled trigger:
    {
        "trigger": "daily_trend_scan",
        "timestamp": "2025-11-24T08:00:00Z",
        "config": {
            "product_categories": ["beauty", "fashion"],
            "min_relevance_score": 0.6
        }
    }
    """
    logger.info(f"Received n8n webhook: {payload}")

    trigger_type = payload.get("trigger")

    if trigger_type == "daily_trend_scan":
        # Run trend scan
        config = payload.get("config", {})
        request = TrendScanRequest(
            product_categories=config.get("product_categories", ["beauty", "fashion", "food"]),
            min_relevance_score=config.get("min_relevance_score", 0.6),
            max_briefs=config.get("max_briefs", 10)
        )

        # Execute in background
        results = workflow.run_daily_content_generation(
            product_categories=request.product_categories,
            min_relevance_score=request.min_relevance_score,
            max_briefs_per_day=request.max_briefs
        )

        return {
            "status": "success",
            "workflow_id": results["workflow_id"],
            "briefs_created": results["content_briefs_created"]
        }

    else:
        return {"status": "unknown_trigger", "trigger": trigger_type}


# Admin endpoints
@app.post("/admin/migrate")
async def run_migrations():
    """Run database migrations"""
    logger.info("Running database migrations...")
    # In production: run Alembic migrations
    return {"status": "migrations_complete"}


@app.post("/admin/import-products")
async def import_products(products: List[Dict]):
    """Import product catalog into vector database"""
    logger.info(f"Importing {len(products)} products...")
    # In production: insert into pgvector
    return {"status": "success", "products_imported": len(products)}


if __name__ == "__main__":
    import uvicorn

    # Run server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,  # Disable in production
        log_level="info"
    )
