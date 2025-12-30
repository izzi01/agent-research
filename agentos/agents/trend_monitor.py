"""
TrendMonitor Agent - Discovers trending TikTok topics relevant to Vietnamese e-commerce

This agent:
1. Monitors TikTok hashtags and trending topics
2. Analyzes engagement metrics (views, likes, shares)
3. Filters for Vietnamese market relevance
4. Stores trends in vector database for later matching
"""

from agno import Agent
from agno.storage.postgres import PostgresStorage
from agno.knowledge.vector_db import PgVector
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta
import os
from .glm_model import create_vietnamese_glm

logger = logging.getLogger(__name__)


class TrendMonitor(Agent):
    """
    Agent that monitors TikTok trends and identifies viral opportunities
    for Vietnamese e-commerce marketing
    """

    def __init__(
        self,
        db_url: str,
        tickertrends_api_key: str,
        model_id: str = "glm-4.6"
    ):
        # Initialize storage for agent state and memory
        storage = PostgresStorage(
            table_name="trend_monitor_runs",
            db_url=db_url
        )

        # Vector database for storing trend embeddings
        vector_db = PgVector(
            table_name="tiktok_trends",
            db_url=db_url,
            embedder="openai"  # or use sentence-transformers for free option
        )

        # Initialize GLM model optimized for Vietnamese
        glm_model = create_vietnamese_glm(model_id=model_id)
        
        super().__init__(
            name="TrendMonitor",
            model=glm_model.model,
            description="Monitor TikTok trends and identify viral opportunities for Vietnamese e-commerce using Z.AI GLM",
            instructions=[
                "Monitor trending TikTok hashtags in Vietnamese market",
                "Analyze engagement metrics (views, likes, shares, comments)",
                "Filter trends relevant to e-commerce products",
                "Identify emerging trends before they peak",
                "Tag trends by category (fashion, beauty, tech, food, lifestyle)",
                "Prioritize trends with high engagement growth rate",
                "Store trend data with Vietnamese keywords and context"
            ],
            storage=storage,
            knowledge_base=vector_db,
            tools=[self.fetch_tiktok_trends, self.analyze_trend_relevance],
            add_datetime_to_instructions=True,
            markdown=True
        )

        self.tickertrends_api_key = tickertrends_api_key
        self.vector_db = vector_db

    def fetch_tiktok_trends(
        self,
        region: str = "VN",
        limit: int = 50,
        time_range: str = "24h"
    ) -> List[Dict]:
        """
        Fetch trending TikTok hashtags and topics

        Args:
            region: Country code (VN for Vietnam)
            limit: Number of trends to fetch
            time_range: Time range for trends (24h, 7d, 30d)

        Returns:
            List of trending topics with metadata
        """
        # In production, this would call TickerTrends API
        # For now, returning mock data structure

        logger.info(f"Fetching TikTok trends for region={region}, limit={limit}, time_range={time_range}")

        # Mock data - replace with actual API call
        # Example API call:
        # import requests
        # response = requests.get(
        #     "https://api.tickertrends.com/v1/trends",
        #     headers={"Authorization": f"Bearer {self.tickertrends_api_key}"},
        #     params={"region": region, "limit": limit, "time_range": time_range}
        # )
        # trends = response.json()["data"]

        mock_trends = [
            {
                "hashtag": "#ReviewSảnPhẩm",
                "views": 125000000,
                "posts": 45200,
                "engagement_rate": 8.5,
                "growth_rate": 245,  # percentage growth in 24h
                "category": "product_reviews",
                "keywords": ["đánh giá", "review", "mua sắm", "shopping"],
                "trending_since": "2025-11-23T10:00:00Z"
            },
            {
                "hashtag": "#TikTokShop",
                "views": 890000000,
                "posts": 125000,
                "engagement_rate": 12.3,
                "growth_rate": 180,
                "category": "ecommerce",
                "keywords": ["tiktok shop", "mua hàng", "giảm giá", "khuyến mãi"],
                "trending_since": "2025-11-22T08:00:00Z"
            },
            {
                "hashtag": "#BeautyHacks",
                "views": 67000000,
                "posts": 23400,
                "engagement_rate": 9.2,
                "growth_rate": 320,
                "category": "beauty",
                "keywords": ["làm đẹp", "beauty", "skincare", "makeup"],
                "trending_since": "2025-11-24T06:00:00Z"
            },
            {
                "hashtag": "#TechViệtNam",
                "views": 45000000,
                "posts": 12800,
                "engagement_rate": 7.8,
                "growth_rate": 156,
                "category": "technology",
                "keywords": ["công nghệ", "tech", "điện thoại", "gadget"],
                "trending_since": "2025-11-23T14:00:00Z"
            },
            {
                "hashtag": "#ĂnVặt",
                "views": 234000000,
                "posts": 67800,
                "engagement_rate": 15.6,
                "growth_rate": 410,
                "category": "food",
                "keywords": ["đồ ăn vặt", "snack", "food", "ẩm thực"],
                "trending_since": "2025-11-24T09:00:00Z"
            }
        ]

        return mock_trends

    def analyze_trend_relevance(
        self,
        trend: Dict,
        product_categories: List[str]
    ) -> Dict:
        """
        Analyze if a trend is relevant to our product catalog

        Args:
            trend: Trend data dictionary
            product_categories: List of product categories we sell

        Returns:
            Relevance score and reasoning
        """
        logger.info(f"Analyzing trend relevance: {trend['hashtag']}")

        # Simple relevance scoring - in production use LLM + embeddings
        relevance_score = 0.0
        reasons = []

        # Check category match
        for category in product_categories:
            if category.lower() in trend.get("category", "").lower():
                relevance_score += 0.3
                reasons.append(f"Category match: {category}")

        # Check keyword overlap
        trend_keywords = [k.lower() for k in trend.get("keywords", [])]
        if any(kw in trend_keywords for kw in ["mua sắm", "shopping", "giảm giá", "khuyến mãi"]):
            relevance_score += 0.2
            reasons.append("E-commerce keywords detected")

        # High engagement boost
        if trend.get("engagement_rate", 0) > 10:
            relevance_score += 0.2
            reasons.append(f"High engagement rate: {trend.get('engagement_rate')}%")

        # Viral growth boost
        if trend.get("growth_rate", 0) > 200:
            relevance_score += 0.3
            reasons.append(f"Viral growth: {trend.get('growth_rate')}% in 24h")

        return {
            "trend_id": trend.get("hashtag"),
            "relevance_score": min(relevance_score, 1.0),  # Cap at 1.0
            "reasons": reasons,
            "recommended_action": "create_content" if relevance_score > 0.5 else "monitor"
        }

    def run_trend_scan(
        self,
        product_categories: List[str],
        min_relevance_score: float = 0.5
    ) -> List[Dict]:
        """
        Main workflow: Scan trends and return relevant opportunities

        Args:
            product_categories: Product categories to match against
            min_relevance_score: Minimum score to consider trend relevant

        Returns:
            List of relevant trends with analysis
        """
        logger.info(f"Starting trend scan for categories: {product_categories}")

        # Step 1: Fetch latest trends
        trends = self.fetch_tiktok_trends(region="VN", limit=50, time_range="24h")

        logger.info(f"Fetched {len(trends)} trends")

        # Step 2: Analyze each trend for relevance
        relevant_trends = []
        for trend in trends:
            analysis = self.analyze_trend_relevance(trend, product_categories)

            if analysis["relevance_score"] >= min_relevance_score:
                # Combine trend data with analysis
                relevant_trend = {
                    **trend,
                    "analysis": analysis
                }
                relevant_trends.append(relevant_trend)

                # Step 3: Store in vector database for later retrieval
                self.vector_db.upsert({
                    "id": f"trend_{trend['hashtag']}_{datetime.now().isoformat()}",
                    "content": f"{trend['hashtag']}: {', '.join(trend.get('keywords', []))}",
                    "metadata": {
                        "hashtag": trend["hashtag"],
                        "views": trend["views"],
                        "engagement_rate": trend["engagement_rate"],
                        "growth_rate": trend["growth_rate"],
                        "category": trend["category"],
                        "relevance_score": analysis["relevance_score"],
                        "discovered_at": datetime.now().isoformat()
                    }
                })

        logger.info(f"Found {len(relevant_trends)} relevant trends (score >= {min_relevance_score})")

        # Sort by combined score: relevance * growth_rate
        relevant_trends.sort(
            key=lambda t: t["analysis"]["relevance_score"] * t["growth_rate"],
            reverse=True
        )

        return relevant_trends


# Example usage in agent execution
if __name__ == "__main__":
    import os

    # Initialize agent
    agent = TrendMonitor(
        db_url=os.getenv("DATABASE_URL", "postgresql://agno:password@localhost:5432/marketing_automation"),
        tickertrends_api_key=os.getenv("TICKERTRENDS_API_KEY", "demo_key")
    )

    # Run trend scan
    product_categories = ["beauty", "fashion", "electronics", "food"]
    relevant_trends = agent.run_trend_scan(
        product_categories=product_categories,
        min_relevance_score=0.5
    )

    # Print results
    print(f"\n🔥 Found {len(relevant_trends)} Relevant Trends:\n")
    for trend in relevant_trends[:5]:  # Top 5
        print(f"#{trend['hashtag']}")
        print(f"  📊 Views: {trend['views']:,}")
        print(f"  📈 Growth: {trend['growth_rate']}%")
        print(f"  ⭐ Relevance: {trend['analysis']['relevance_score']:.2f}")
        print(f"  💡 Reasons: {', '.join(trend['analysis']['reasons'])}")
        print(f"  ✅ Action: {trend['analysis']['recommended_action']}\n")
