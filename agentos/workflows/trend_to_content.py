"""
Trend-to-Content Workflow - Complete pipeline from trend discovery to content brief

This workflow orchestrates multiple agents:
1. TrendMonitor → Discover trending topics
2. ContentStrategist → Match trends to products and create briefs
3. (Future) TextCreator → Generate Vietnamese copy
4. (Future) VideoGenerator → Create videos with Vietnamese voiceover
5. (Future) ApprovalCoordinator → Queue for human approval
"""

from agno import Team
from agno.models.anthropic import Claude
from agents.trend_monitor import TrendMonitor
from agents.content_strategist import ContentStrategist
from typing import List, Dict
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrendToContentWorkflow:
    """
    Complete workflow from trend monitoring to content brief creation
    """

    def __init__(self, db_url: str, tickertrends_api_key: str):
        """
        Initialize workflow with required agents

        Args:
            db_url: PostgreSQL database URL
            tickertrends_api_key: TickerTrends API key for trend monitoring
        """
        self.db_url = db_url
        self.tickertrends_api_key = tickertrends_api_key

        # Initialize agents
        logger.info("Initializing agents...")

        self.trend_monitor = TrendMonitor(
            db_url=db_url,
            tickertrends_api_key=tickertrends_api_key
        )

        self.content_strategist = ContentStrategist(
            db_url=db_url
        )

        # Create agent team for coordination
        self.team = Team(
            name="VietnameseMarketingAutomation",
            agents=[self.trend_monitor, self.content_strategist],
            mode="coordinate",  # Agents work together on tasks
            description="Vietnamese e-commerce marketing automation team"
        )

        logger.info("Agents initialized successfully")

    def run_daily_content_generation(
        self,
        product_categories: List[str],
        min_relevance_score: float = 0.6,
        max_briefs_per_day: int = 10
    ) -> Dict:
        """
        Daily workflow: Discover trends → Create content briefs

        Args:
            product_categories: Product categories to match
            min_relevance_score: Minimum relevance for trends
            max_briefs_per_day: Maximum content briefs to create

        Returns:
            Workflow results with statistics
        """
        workflow_start = datetime.now()
        logger.info("=" * 60)
        logger.info("🚀 STARTING DAILY CONTENT GENERATION WORKFLOW")
        logger.info("=" * 60)

        results = {
            "workflow_id": f"workflow_{workflow_start.isoformat()}",
            "started_at": workflow_start.isoformat(),
            "product_categories": product_categories,
            "trends_discovered": 0,
            "trends_relevant": 0,
            "content_briefs_created": 0,
            "briefs": [],
            "status": "running"
        }

        try:
            # STEP 1: Trend Discovery
            logger.info("\n📊 STEP 1: DISCOVERING TIKTOK TRENDS")
            logger.info("-" * 60)

            trends = self.trend_monitor.run_trend_scan(
                product_categories=product_categories,
                min_relevance_score=min_relevance_score
            )

            results["trends_discovered"] = len(trends)
            results["trends_relevant"] = len([t for t in trends if t["analysis"]["relevance_score"] >= min_relevance_score])

            logger.info(f"✅ Found {results['trends_discovered']} total trends")
            logger.info(f"✅ {results['trends_relevant']} trends meet relevance threshold (>= {min_relevance_score})")

            if not trends:
                logger.warning("⚠️  No relevant trends found. Ending workflow.")
                results["status"] = "no_trends_found"
                return results

            # STEP 2: Content Strategy
            logger.info("\n📝 STEP 2: CREATING CONTENT BRIEFS")
            logger.info("-" * 60)

            briefs_created = 0
            for trend in trends[:max_briefs_per_day]:
                logger.info(f"\nProcessing trend: {trend['hashtag']}")
                logger.info(f"  Relevance: {trend['analysis']['relevance_score']:.2f}")
                logger.info(f"  Growth: {trend['growth_rate']}%")
                logger.info(f"  Views: {trend['views']:,}")

                # Create content briefs
                briefs = self.content_strategist.run_strategy_session(
                    trend=trend,
                    max_products=2,
                    content_formats=["tiktok_video"]  # Start with TikTok only
                )

                if briefs:
                    results["briefs"].extend(briefs)
                    briefs_created += len(briefs)
                    logger.info(f"  ✅ Created {len(briefs)} content brief(s)")
                else:
                    logger.info(f"  ⚠️  No products matched for this trend")

            results["content_briefs_created"] = briefs_created

            # STEP 3: Workflow Summary
            logger.info("\n📈 STEP 3: WORKFLOW SUMMARY")
            logger.info("=" * 60)

            workflow_end = datetime.now()
            duration = (workflow_end - workflow_start).total_seconds()

            results["completed_at"] = workflow_end.isoformat()
            results["duration_seconds"] = duration
            results["status"] = "completed"

            logger.info(f"⏱️  Duration: {duration:.2f} seconds")
            logger.info(f"🔥 Trends Discovered: {results['trends_discovered']}")
            logger.info(f"✅ Relevant Trends: {results['trends_relevant']}")
            logger.info(f"📝 Content Briefs Created: {results['content_briefs_created']}")

            if results["briefs"]:
                logger.info("\n📋 CONTENT BRIEFS READY FOR PRODUCTION:")
                for i, brief in enumerate(results["briefs"], 1):
                    logger.info(f"\n  Brief #{i}:")
                    logger.info(f"    Trend: {brief['trend_id']}")
                    logger.info(f"    Format: {brief['content_format']}")
                    logger.info(f"    Products: {len(brief['products'])}")
                    logger.info(f"    Hook: {brief['vietnamese_hook'][:60]}...")
                    logger.info(f"    Expected Views: {brief['success_metrics']['target_views']:,}")
                    logger.info(f"    Expected Revenue: {brief['success_metrics']['expected_revenue_vnd']:,} VNĐ")

            # Calculate total expected impact
            total_expected_views = sum(b["success_metrics"]["target_views"] for b in results["briefs"])
            total_expected_revenue = sum(b["success_metrics"]["expected_revenue_vnd"] for b in results["briefs"])

            logger.info(f"\n💰 TOTAL EXPECTED IMPACT:")
            logger.info(f"    Views: {total_expected_views:,}")
            logger.info(f"    Revenue: {total_expected_revenue:,} VNĐ (${total_expected_revenue/24000:.2f} USD)")

            logger.info("\n" + "=" * 60)
            logger.info("✅ WORKFLOW COMPLETED SUCCESSFULLY")
            logger.info("=" * 60 + "\n")

            return results

        except Exception as e:
            logger.error(f"❌ Workflow failed: {str(e)}", exc_info=True)
            results["status"] = "failed"
            results["error"] = str(e)
            results["completed_at"] = datetime.now().isoformat()
            return results

    def get_brief_by_id(self, brief_id: str) -> Dict:
        """
        Retrieve a specific content brief

        Args:
            brief_id: Brief identifier

        Returns:
            Content brief or None
        """
        # In production: query from database
        pass

    def approve_brief(self, brief_id: str, approved: bool, feedback: str = "") -> Dict:
        """
        Human approval of content brief

        Args:
            brief_id: Brief identifier
            approved: Approval decision
            feedback: Optional feedback for revision

        Returns:
            Updated brief status
        """
        # In production: update database + trigger next workflow step
        logger.info(f"Brief {brief_id}: {'APPROVED' if approved else 'REJECTED'}")
        if feedback:
            logger.info(f"Feedback: {feedback}")

        return {
            "brief_id": brief_id,
            "approved": approved,
            "feedback": feedback,
            "approved_at": datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Initialize workflow
    workflow = TrendToContentWorkflow(
        db_url=os.getenv("DATABASE_URL", "postgresql://agno:password@localhost:5432/marketing_automation"),
        tickertrends_api_key=os.getenv("TICKERTRENDS_API_KEY", "demo_key")
    )

    # Run daily content generation
    results = workflow.run_daily_content_generation(
        product_categories=["beauty", "fashion", "food", "electronics"],
        min_relevance_score=0.6,
        max_briefs_per_day=5
    )

    # Print summary
    print("\n" + "=" * 60)
    print("WORKFLOW RESULTS SUMMARY")
    print("=" * 60)
    print(f"Status: {results['status']}")
    print(f"Trends Discovered: {results['trends_discovered']}")
    print(f"Content Briefs Created: {results['content_briefs_created']}")
    print(f"Duration: {results.get('duration_seconds', 0):.2f}s")

    if results['briefs']:
        print(f"\nFirst brief preview:")
        first_brief = results['briefs'][0]
        print(f"  Trend: {first_brief['trend_id']}")
        print(f"  Hook: {first_brief['vietnamese_hook']}")
        print(f"  Hashtags: {' '.join(first_brief['hashtags'][:5])}")
