"""
ContentStrategist Agent - Matches trends to products and creates Vietnamese content briefs

This agent:
1. Receives trending topics from TrendMonitor
2. Queries product catalog (stored in vector DB)
3. Matches trends to relevant products
4. Creates Vietnamese content briefs for TextCreator and VideoGenerator
5. Ensures cultural appropriateness for Vietnamese audience
"""

from agno import Agent
from agno.storage.postgres import PostgresStorage
from agno.knowledge.vector_db import PgVector
from typing import List, Dict, Optional
import logging
from datetime import datetime
import os
from .glm_model import create_vietnamese_glm

logger = logging.getLogger(__name__)


class ContentStrategist(Agent):
    """
    Agent that creates strategic content briefs by matching trends to products
    """

    def __init__(
        self,
        db_url: str,
        model_id: str = "glm-4.6"
    ):
        # Storage for agent runs
        storage = PostgresStorage(
            table_name="content_strategist_runs",
            db_url=db_url
        )

        # Product catalog knowledge base
        product_kb = PgVector(
            table_name="product_catalog",
            db_url=db_url,
            embedder="openai"
        )

        # Trend knowledge base (shared with TrendMonitor)
        trend_kb = PgVector(
            table_name="tiktok_trends",
            db_url=db_url,
            embedder="openai"
        )

        # Initialize GLM model optimized for Vietnamese
        glm_model = create_vietnamese_glm(model_id=model_id)
        
        super().__init__(
            name="ContentStrategist",
            model=glm_model.model,
            description="Create strategic Vietnamese content briefs by matching trends to products using Z.AI GLM",
            instructions=[
                "You are an expert Vietnamese marketing strategist specializing in TikTok and social media content",
                "Analyze trending topics and match them to relevant products from our catalog",
                "Create culturally appropriate content briefs for Vietnamese audience",
                "Consider Vietnamese cultural nuances, humor, and communication style",
                "Suggest content angles that will resonate with Vietnamese consumers",
                "Prioritize authentic, relatable content over hard selling",
                "Include specific Vietnamese keywords and hashtags",
                "Recommend optimal posting times for Vietnamese timezone (GMT+7)",
                "Suggest content format (Reel, TikTok, Story, Post)",
                "Balance trending appeal with product relevance"
            ],
            storage=storage,
            knowledge_base=product_kb,
            tools=[
                self.search_products,
                self.get_trend_details,
                self.generate_vietnamese_hashtags
            ],
            add_datetime_to_instructions=True,
            markdown=True
        )

        self.product_kb = product_kb
        self.trend_kb = trend_kb

    def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Search product catalog using semantic search

        Args:
            query: Search query (trend description, keywords)
            category: Optional category filter
            limit: Maximum number of products to return

        Returns:
            List of matching products
        """
        logger.info(f"Searching products: query='{query}', category={category}")

        # In production, this uses vector similarity search
        # Mock product data for demonstration
        mock_products = [
            {
                "id": "PROD001",
                "name": "Son Lì Bền Màu 24H",
                "name_en": "Long-lasting Matte Lipstick 24H",
                "category": "beauty",
                "price_vnd": 259000,
                "description": "Son lì bền màu, không chứa chì, an toàn cho môi, giữ màu 24 giờ",
                "tags": ["beauty", "makeup", "lipstick", "làm đẹp", "son môi"],
                "inventory": 450,
                "rating": 4.8,
                "image_url": "https://cdn.shop.com/products/lipstick-001.jpg"
            },
            {
                "id": "PROD002",
                "name": "Mặt Nạ Dưỡng Da Collagen",
                "name_en": "Collagen Face Mask",
                "category": "beauty",
                "price_vnd": 35000,
                "description": "Mặt nạ dưỡng da collagen, cấp ẩm sâu, làm trắng da tự nhiên",
                "tags": ["beauty", "skincare", "mask", "làm đẹp", "dưỡng da"],
                "inventory": 1200,
                "rating": 4.6,
                "image_url": "https://cdn.shop.com/products/mask-002.jpg"
            },
            {
                "id": "PROD003",
                "name": "Bộ Quần Áo Thể Thao Nam",
                "name_en": "Men's Sports Outfit Set",
                "category": "fashion",
                "price_vnd": 489000,
                "description": "Bộ quần áo thể thao nam cao cấp, vải thấm hút mồ hôi, thoáng mát",
                "tags": ["fashion", "sports", "men", "quần áo", "thể thao"],
                "inventory": 230,
                "rating": 4.7,
                "image_url": "https://cdn.shop.com/products/sportswear-003.jpg"
            },
            {
                "id": "PROD004",
                "name": "Snack Hạnh Nhân Mật Ong",
                "name_en": "Honey Roasted Almonds Snack",
                "category": "food",
                "price_vnd": 89000,
                "description": "Hạnh nhân rang mật ong, giòn ngon, bổ dưỡng, không chất bảo quản",
                "tags": ["food", "snack", "healthy", "đồ ăn vặt", "hạnh nhân"],
                "inventory": 680,
                "rating": 4.9,
                "image_url": "https://cdn.shop.com/products/almonds-004.jpg"
            },
            {
                "id": "PROD005",
                "name": "Tai Nghe Bluetooth True Wireless",
                "name_en": "True Wireless Bluetooth Earbuds",
                "category": "electronics",
                "price_vnd": 599000,
                "description": "Tai nghe Bluetooth True Wireless, chống ồn chủ động, pin 20 giờ",
                "tags": ["electronics", "audio", "earbuds", "tai nghe", "bluetooth"],
                "inventory": 156,
                "rating": 4.5,
                "image_url": "https://cdn.shop.com/products/earbuds-005.jpg"
            }
        ]

        # Filter by category if provided
        if category:
            mock_products = [p for p in mock_products if p["category"] == category]

        # In production: semantic search using embeddings
        # results = self.product_kb.search(query, limit=limit)

        return mock_products[:limit]

    def get_trend_details(self, trend_id: str) -> Optional[Dict]:
        """
        Get full details of a trend from vector database

        Args:
            trend_id: Trend identifier (hashtag)

        Returns:
            Trend details or None if not found
        """
        logger.info(f"Getting trend details: {trend_id}")

        # In production: query vector DB
        # results = self.trend_kb.search(trend_id, limit=1)

        # Mock data
        return {
            "hashtag": trend_id,
            "views": 67000000,
            "engagement_rate": 9.2,
            "growth_rate": 320,
            "category": "beauty",
            "keywords": ["làm đẹp", "beauty", "skincare", "makeup"]
        }

    def generate_vietnamese_hashtags(
        self,
        trend_hashtag: str,
        product_name: str,
        category: str
    ) -> List[str]:
        """
        Generate Vietnamese hashtags for content

        Args:
            trend_hashtag: Original trending hashtag
            product_name: Product name
            category: Product category

        Returns:
            List of Vietnamese hashtags
        """
        # Base hashtags
        hashtags = [trend_hashtag]

        # Category-specific hashtags
        category_hashtags = {
            "beauty": ["#LàmĐẹp", "#BeautyVietNam", "#MakeupTips", "#Skincare"],
            "fashion": ["#ThờiTrang", "#FashionVN", "#OOTD", "#StyleViệtNam"],
            "food": ["#ĂnVặt", "#FoodVietNam", "#SnackTime", "#ĂnNgon"],
            "electronics": ["#CôngNghệ", "#TechVN", "#Gadget", "#ĐiệnTử"]
        }

        hashtags.extend(category_hashtags.get(category, []))

        # E-commerce hashtags
        hashtags.extend([
            "#TikTokShop",
            "#MuaSắm",
            "#GiảmGiá",
            "#Review"
        ])

        return hashtags[:10]  # Max 10 hashtags

    def create_content_brief(
        self,
        trend: Dict,
        products: List[Dict],
        content_format: str = "tiktok_video"
    ) -> Dict:
        """
        Create a detailed content brief using Claude AI

        Args:
            trend: Trending topic data
            products: Matched products
            content_format: Type of content (tiktok_video, facebook_reel, instagram_story)

        Returns:
            Content brief with Vietnamese copy, angles, and instructions
        """
        logger.info(f"Creating content brief: trend={trend['hashtag']}, products={len(products)}")

        # Prepare context for Claude
        context = f"""
Trending Topic: {trend['hashtag']}
- Views: {trend.get('views', 0):,}
- Engagement Rate: {trend.get('engagement_rate', 0)}%
- Growth Rate: {trend.get('growth_rate', 0)}%
- Category: {trend.get('category', 'general')}
- Keywords: {', '.join(trend.get('keywords', []))}

Matched Products:
"""
        for i, product in enumerate(products, 1):
            context += f"\n{i}. {product['name']} ({product['name_en']})"
            context += f"\n   - Price: {product['price_vnd']:,} VNĐ"
            context += f"\n   - Description: {product['description']}"
            context += f"\n   - Rating: {product['rating']}/5.0"

        context += f"\n\nContent Format: {content_format}"

        # Prompt for Claude
        prompt = f"""
Based on the trending topic and products above, create a Vietnamese content brief for {content_format}.

Your brief should include:

1. **Vietnamese Hook** (Câu mở đầu thu hút): A compelling opening line in natural Vietnamese that connects the trend to the product

2. **Content Angle** (Góc nhìn nội dung): The creative approach to present the product (e.g., review, tutorial, before/after, storytelling)

3. **Script Outline** (Kịch bản):
   - Opening (3-5 seconds)
   - Main content (15-20 seconds)
   - Call-to-action (3-5 seconds)

4. **Visual Suggestions** (Gợi ý hình ảnh):
   - Key scenes to show
   - Product demonstration ideas
   - Background/setting recommendations

5. **Vietnamese Voiceover Script** (Lời thoại tiếng Việt): Full Vietnamese script for AI voice

6. **Hashtags**: Top 8-10 Vietnamese hashtags including the trending hashtag

7. **Optimal Posting Time** (Giờ đăng tối ưu): Best time to post for Vietnamese audience

8. **Success Metrics** (Chỉ số thành công): Expected engagement KPIs

Write in a natural, conversational Vietnamese style that resonates with Gen Z and Millennial Vietnamese audiences on TikTok.

{context}
"""

        # Call Claude (in production)
        # response = self.model.generate(prompt)

        # Mock response for demonstration
        mock_brief = {
            "trend_id": trend["hashtag"],
            "products": [p["id"] for p in products],
            "content_format": content_format,
            "created_at": datetime.now().isoformat(),

            "vietnamese_hook": "Chị em ơi! Trend làm đẹp này đang gây bão TikTok, mình phải thử ngay! 💄✨",

            "content_angle": "Product Review + Tutorial - Show before/after transformation using the product while riding the trending beauty hack wave",

            "script_outline": {
                "opening": "Hook with trending sound + text overlay: 'Thử ngay beauty hack đang viral!' (3s)",
                "main_content": "Show product unboxing → Quick application tutorial → Before/After comparison → Share honest review in Vietnamese (20s)",
                "cta": "Text overlay with shop link + voiceover: 'Link mua ở Shop ngay nào!' (3s)"
            },

            "visual_suggestions": [
                "Open with trending TikTok transition effect",
                "Close-up shots of product texture and application",
                "Split-screen before/after comparison",
                "Natural lighting, clean white/pink background",
                "Show product packaging with price clearly visible"
            ],

            "vietnamese_voiceover": """
Chào các bạn! Hôm nay mình sẽ review cho các bạn cây son lì này đang được nhiều bạn hỏi.

[Unboxing]
Bao bì rất xinh xắn, giá chỉ 259k thôi nha các bạn!

[Application]
Mình thử màu hồng cam này nhé. Lên môi rất mịn, không khô môi, màu cũng rất chuẩn.

[Result]
Sau 4 tiếng đi làm, ăn uống bình thường, màu vẫn giữ được 80% luôn nè!

Các bạn thích thì vào shop của mình mua nhé! Link ở dưới nha! ❤️
""",

            "hashtags": [
                trend["hashtag"],  # Trending hashtag
                "#ReviewSảnPhẩm",
                "#LàmĐẹp",
                "#BeautyVietNam",
                "#TikTokShop",
                "#SonLì",
                "#MakeupTutorial",
                "#GiảmGiá",
                "#MuaSắm"
            ],

            "optimal_posting_time": "19:00-21:00 GMT+7 (Vietnamese evening prime time)",

            "success_metrics": {
                "target_views": 50000,
                "target_engagement_rate": 8.0,
                "target_conversions": 100,
                "expected_revenue_vnd": 25900000  # 100 units * 259k
            },

            "cultural_notes": [
                "Use friendly 'chị em' address for female audience",
                "Include price transparency (Vietnamese consumers value clear pricing)",
                "Show honest review (build trust over hard selling)",
                "Use trending sounds but keep Vietnamese voiceover"
            ]
        }

        return mock_brief

    def run_strategy_session(
        self,
        trend: Dict,
        max_products: int = 3,
        content_formats: List[str] = ["tiktok_video"]
    ) -> List[Dict]:
        """
        Main workflow: Create content briefs for a trending topic

        Args:
            trend: Trending topic data
            max_products: Maximum products to match
            content_formats: List of content formats to create

        Returns:
            List of content briefs ready for creators
        """
        logger.info(f"Starting strategy session for trend: {trend['hashtag']}")

        # Step 1: Search for relevant products
        query = f"{trend['hashtag']} {' '.join(trend.get('keywords', []))}"
        products = self.search_products(
            query=query,
            category=trend.get('category'),
            limit=max_products
        )

        if not products:
            logger.warning(f"No products found for trend: {trend['hashtag']}")
            return []

        logger.info(f"Matched {len(products)} products")

        # Step 2: Create content briefs for each format
        briefs = []
        for content_format in content_formats:
            brief = self.create_content_brief(
                trend=trend,
                products=products,
                content_format=content_format
            )
            briefs.append(brief)

        logger.info(f"Created {len(briefs)} content briefs")

        return briefs


# Example usage
if __name__ == "__main__":
    import os

    # Initialize agent
    agent = ContentStrategist(
        db_url=os.getenv("DATABASE_URL", "postgresql://agno:password@localhost:5432/marketing_automation")
    )

    # Sample trend from TrendMonitor
    sample_trend = {
        "hashtag": "#BeautyHacks",
        "views": 67000000,
        "engagement_rate": 9.2,
        "growth_rate": 320,
        "category": "beauty",
        "keywords": ["làm đẹp", "beauty", "skincare", "makeup"]
    }

    # Create content briefs
    briefs = agent.run_strategy_session(
        trend=sample_trend,
        max_products=2,
        content_formats=["tiktok_video", "facebook_reel"]
    )

    # Print results
    print(f"\n📝 Created {len(briefs)} Content Briefs:\n")
    for i, brief in enumerate(briefs, 1):
        print(f"Brief #{i}: {brief['content_format']}")
        print(f"  Trend: {brief['trend_id']}")
        print(f"  Products: {', '.join(brief['products'])}")
        print(f"  Hook: {brief['vietnamese_hook']}")
        print(f"  Hashtags: {' '.join(brief['hashtags'][:5])}")
        print(f"  Expected Views: {brief['success_metrics']['target_views']:,}")
        print()
