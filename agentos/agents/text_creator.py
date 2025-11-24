"""
TextCreator Agent - Generates final Vietnamese social media copy from content briefs

This agent:
1. Takes content briefs from ContentStrategist
2. Generates platform-specific Vietnamese copy (Facebook, TikTok, Shopee)
3. Ensures character limits and formatting per platform
4. Creates A/B testing variants
5. Optimizes emoji usage and hashtag placement
"""

from agno import Agent
from agno.models.anthropic import Claude
from agno.storage.postgres import PostgresStorage
from typing import List, Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TextCreator(Agent):
    """
    Agent that generates final Vietnamese social media copy from content briefs
    """

    # Platform character limits
    PLATFORM_LIMITS = {
        "facebook_post": 63206,  # Facebook has high limit, but optimal is 40-80 chars
        "facebook_optimal": 80,  # For engagement
        "tiktok_caption": 2200,  # TikTok caption limit
        "tiktok_optimal": 300,   # Optimal for readability
        "shopee_title": 120,     # Shopee product title
        "shopee_description": 3000,  # Shopee description
        "instagram_caption": 2200,
        "youtube_description": 5000
    }

    def __init__(
        self,
        db_url: str,
        model_id: str = "claude-sonnet-4-20250514"
    ):
        # Storage for generated copy
        storage = PostgresStorage(
            table_name="text_creator_runs",
            db_url=db_url
        )

        super().__init__(
            name="TextCreator",
            model=Claude(id=model_id),
            description="Generate final Vietnamese social media copy optimized for each platform",
            instructions=[
                "You are an expert Vietnamese copywriter specializing in social media marketing",
                "Write in natural, conversational Vietnamese that resonates with Gen Z and Millennials",
                "Use authentic Vietnamese expressions, not literal translations",
                "Include emojis strategically (2-4 per post) for visual appeal",
                "Place hashtags at the end of copy, not mixed in text",
                "Keep copy concise and punchy - Vietnamese audiences scan quickly",
                "Use 'mình' (casual first person) for relatability",
                "Address audience as 'các bạn' (friendly) or 'chị em' (for female audience)",
                "Avoid overly formal language unless for luxury products",
                "Include call-to-action that feels natural, not pushy",
                "Respect Vietnamese cultural values (family, community, authenticity)",
                "Optimize for mobile reading (short paragraphs, line breaks)"
            ],
            storage=storage,
            tools=[
                self.count_characters,
                self.validate_hashtags,
                self.optimize_emojis
            ],
            add_datetime_to_instructions=True,
            markdown=True
        )

    def count_characters(self, text: str) -> int:
        """Count characters in text (excluding spaces for some platforms)"""
        return len(text)

    def validate_hashtags(self, hashtags: List[str]) -> Dict:
        """
        Validate hashtag format and count

        Args:
            hashtags: List of hashtags to validate

        Returns:
            Validation results
        """
        issues = []

        if len(hashtags) > 30:
            issues.append("Too many hashtags (max 30 recommended)")

        if len(hashtags) < 3:
            issues.append("Too few hashtags (min 3 recommended)")

        for tag in hashtags:
            if not tag.startswith("#"):
                issues.append(f"Hashtag missing #: {tag}")
            if " " in tag:
                issues.append(f"Hashtag contains space: {tag}")

        return {
            "valid": len(issues) == 0,
            "count": len(hashtags),
            "issues": issues
        }

    def optimize_emojis(self, text: str, max_emojis: int = 5) -> Dict:
        """
        Check emoji usage in text

        Args:
            text: Text to analyze
            max_emojis: Maximum recommended emojis

        Returns:
            Emoji analysis
        """
        # Simple emoji detection (in production use emoji library)
        emoji_chars = ['😍', '💄', '✨', '🔥', '💖', '👗', '🎉', '💯', '😊', '🌟',
                       '💕', '❤️', '🥰', '😘', '🤩', '💋', '👄', '🎀', '💅', '🌸']

        emoji_count = sum(text.count(emoji) for emoji in emoji_chars)

        return {
            "emoji_count": emoji_count,
            "optimal": 2 <= emoji_count <= max_emojis,
            "recommendation": "Add more emojis" if emoji_count < 2 else "Good emoji usage" if emoji_count <= max_emojis else "Too many emojis"
        }

    def generate_platform_copy(
        self,
        brief: Dict,
        platform: str,
        variant: str = "default",
        tone: str = "casual"
    ) -> Dict:
        """
        Generate platform-specific Vietnamese copy

        Args:
            brief: Content brief from ContentStrategist
            platform: Target platform (facebook, tiktok, shopee, instagram)
            variant: Copy variant (default, promotional, storytelling)
            tone: Tone of voice (casual, professional, enthusiastic)

        Returns:
            Generated copy with metadata
        """
        logger.info(f"Generating {platform} copy: variant={variant}, tone={tone}")

        # Get platform constraints
        char_limit = self.PLATFORM_LIMITS.get(f"{platform}_optimal", 500)

        # Build prompt for Claude
        prompt = self._build_copy_prompt(brief, platform, variant, tone, char_limit)

        # In production: Call Claude API
        # response = self.model.generate(prompt)
        # generated_copy = response.content

        # Mock response for demonstration
        generated_copy = self._generate_mock_copy(brief, platform, variant, tone)

        # Validate copy
        char_count = self.count_characters(generated_copy["body"])
        hashtag_validation = self.validate_hashtags(generated_copy["hashtags"])
        emoji_analysis = self.optimize_emojis(generated_copy["body"])

        return {
            "platform": platform,
            "variant": variant,
            "tone": tone,
            "copy": generated_copy,
            "metadata": {
                "character_count": char_count,
                "character_limit": char_limit,
                "within_limit": char_count <= char_limit,
                "hashtag_validation": hashtag_validation,
                "emoji_analysis": emoji_analysis,
                "generated_at": datetime.now().isoformat()
            }
        }

    def _build_copy_prompt(
        self,
        brief: Dict,
        platform: str,
        variant: str,
        tone: str,
        char_limit: int
    ) -> str:
        """Build prompt for Claude to generate copy"""

        prompt = f"""
Generate Vietnamese social media copy based on this content brief:

CONTENT BRIEF:
- Trend: {brief.get('trend_id', 'N/A')}
- Hook: {brief.get('vietnamese_hook', 'N/A')}
- Content Angle: {brief.get('content_angle', 'N/A')}
- Products: {', '.join(brief.get('products', []))}
- Target Hashtags: {' '.join(brief.get('hashtags', [])[:5])}

PLATFORM: {platform.upper()}
VARIANT: {variant}
TONE: {tone}
CHARACTER LIMIT: {char_limit} characters (optimal length)

REQUIREMENTS:
1. Write natural, conversational Vietnamese (not formal translation)
2. Keep within {char_limit} characters for optimal engagement
3. Include 2-4 emojis strategically placed
4. End with call-to-action (subtle, not pushy)
5. Use hashtags at the end only
6. Format for mobile reading (line breaks for clarity)

OUTPUT FORMAT (JSON):
{{
    "body": "The main Vietnamese copy here...",
    "hashtags": ["#hashtag1", "#hashtag2", ...],
    "call_to_action": "Visit shop/Like/Comment/Share"
}}

Generate the copy now:
"""
        return prompt

    def _generate_mock_copy(
        self,
        brief: Dict,
        platform: str,
        variant: str,
        tone: str
    ) -> Dict:
        """Generate mock copy for demonstration"""

        if platform == "facebook":
            if variant == "promotional":
                return {
                    "body": "Chị em ơi! Deal hot đây! 🔥\n\nSon lì bền màu 24h đang sale sốc chỉ còn 199K (giá gốc 259K) 💄✨\n\nLên màu chuẩn, không khô môi, giữ màu cả ngày luôn nha! Mình dùng thấy ổn lắm, các bạn thử nghen 😍\n\nShop ship toàn quốc, đặt ngay kẻo hết! 💖",
                    "hashtags": ["#SaleSốc", "#SonLì", "#LàmĐẹp", "#BeautyVietNam", "#TikTokShop"],
                    "call_to_action": "Inbox shop để đặt hàng ngay nha các bạn!"
                }
            else:  # default
                return {
                    "body": "Hôm nay mình review cho các bạn cây son lì này nha! 💄\n\nThật ra lúc đầu mình cũng hơi nghi ngờ vì giá chỉ 259K thôi. Nhưng dùng rồi mình phải công nhận: màu đẹp, lên môi mịn, không khô môi như mấy em son lì khác 😍\n\nQuan trọng là giữ màu được 4-5 tiếng luôn nè! Ăn uống nhẹ vẫn còn màu 80% 💖\n\nCác bạn thích thì vào shop mình xem nhé!",
                    "hashtags": ["#ReviewSảnPhẩm", "#SonLì", "#LàmĐẹp", "#BeautyTips"],
                    "call_to_action": "Comment 'Đẹp' để mình gửi link shop nha!"
                }

        elif platform == "tiktok":
            return {
                "body": "Trend làm đẹp hot nhất tuần này! 🔥\n\nThử ngay beauty hack với son lì bền màu 24h 💄✨\n\nKết quả: Môi căng mọng, màu chuẩn, không khô! Giá chỉ 259K thôi nha 😍\n\nLink shop ở dưới, các bạn múa tay lên nào! 💖",
                "hashtags": ["#BeautyHacks", "#LàmĐẹp", "#TikTokShop", "#ReviewSảnPhẩm", "#SonLì"],
                "call_to_action": "Lướt qua shop ngay! 👇"
            }

        elif platform == "shopee":
            return {
                "body": """SON LÌ BỀN MÀU 24H - CHÍNH HÃNG 💄

🌟 ĐẶC ĐIỂM NỔI BẬT:
• Màu sắc chuẩn, bền màu 24 giờ
• Công thức lì mượt, không khô môi
• An toàn, không chứa chì
• Phù hợp mọi loại môi

💖 THÀNH PHẦN:
• Vitamin E dưỡng môi
• Chiết xuất thiên nhiên
• Không gây kích ứng

✨ CAM KẾT:
✓ Hàng chính hãng 100%
✓ Hoàn tiền nếu hàng giả
✓ Đổi trả trong 7 ngày
✓ Freeship đơn từ 50K

📦 Giao hàng toàn quốc
🎁 Tặng kèm son dưỡng mini

ĐẶT NGAY HÔM NAY! 🛒""",
                "hashtags": ["#SonLì", "#MỹPhẩmChínhHãng", "#FreeshíP", "#ShopeeVietNam"],
                "call_to_action": "Thêm vào giỏ hàng ngay!"
            }

        else:  # instagram or default
            return {
                "body": "Beauty moment of the day 💄✨\n\nHôm nay mình thử son lì màu này, các bạn thấy thế nào? Màu hồng cam rất tươi tắn luôn nha! 😍\n\nGiá chỉ 259K, bền màu cả ngày, không khô môi. Mình rate 9/10 điểm! 💖\n\nSwipe để xem before/after nè! 👉",
                "hashtags": ["#BeautyVietNam", "#LàmĐẹp", "#MOTD", "#VietnameseBeauty", "#SonLì"],
                "call_to_action": "Save post này để khỏi quên nha!"
            }

    def generate_ab_variants(
        self,
        brief: Dict,
        platform: str,
        num_variants: int = 3
    ) -> List[Dict]:
        """
        Generate multiple A/B testing variants

        Args:
            brief: Content brief
            platform: Target platform
            num_variants: Number of variants to generate

        Returns:
            List of copy variants
        """
        logger.info(f"Generating {num_variants} A/B variants for {platform}")

        variants = []
        variant_types = ["default", "promotional", "storytelling", "educational", "humorous"]
        tones = ["casual", "enthusiastic", "professional"]

        for i in range(num_variants):
            variant_type = variant_types[i % len(variant_types)]
            tone = tones[i % len(tones)]

            copy = self.generate_platform_copy(
                brief=brief,
                platform=platform,
                variant=variant_type,
                tone=tone
            )

            copy["variant_id"] = f"{platform}_v{i+1}_{variant_type}"
            variants.append(copy)

        logger.info(f"Generated {len(variants)} variants")
        return variants

    def run_copy_generation(
        self,
        brief: Dict,
        platforms: List[str] = ["facebook", "tiktok"],
        generate_variants: bool = False
    ) -> Dict:
        """
        Main workflow: Generate copy for multiple platforms

        Args:
            brief: Content brief from ContentStrategist
            platforms: List of platforms to generate copy for
            generate_variants: Whether to generate A/B testing variants

        Returns:
            Generated copy for all platforms
        """
        logger.info(f"Starting copy generation for platforms: {platforms}")
        logger.info(f"Brief: {brief.get('trend_id', 'N/A')}")

        results = {
            "brief_id": brief.get("trend_id"),
            "platforms": platforms,
            "generated_at": datetime.now().isoformat(),
            "copy": {}
        }

        for platform in platforms:
            if generate_variants:
                # Generate 3 A/B variants
                variants = self.generate_ab_variants(brief, platform, num_variants=3)
                results["copy"][platform] = variants
                logger.info(f"✅ {platform}: Generated {len(variants)} variants")
            else:
                # Generate single default copy
                copy = self.generate_platform_copy(brief, platform)
                results["copy"][platform] = [copy]
                logger.info(f"✅ {platform}: Generated default copy")

        logger.info(f"Copy generation completed for {len(platforms)} platforms")
        return results


# Example usage
if __name__ == "__main__":
    import os

    # Initialize agent
    agent = TextCreator(
        db_url=os.getenv("DATABASE_URL", "postgresql://agno:password@localhost:5432/marketing_automation")
    )

    # Sample brief from ContentStrategist
    sample_brief = {
        "trend_id": "#BeautyHacks",
        "vietnamese_hook": "Chị em ơi! Trend làm đẹp này đang gây bão TikTok, mình phải thử ngay! 💄✨",
        "content_angle": "Product Review + Tutorial - Show before/after transformation",
        "products": ["PROD001"],
        "hashtags": ["#BeautyHacks", "#LàmĐẹp", "#TikTokShop", "#ReviewSảnPhẩm"],
        "vietnamese_voiceover": "Chào các bạn! Hôm nay mình review son lì..."
    }

    # Generate copy for multiple platforms
    results = agent.run_copy_generation(
        brief=sample_brief,
        platforms=["facebook", "tiktok", "shopee"],
        generate_variants=False  # Set to True for A/B testing
    )

    # Print results
    print("\n" + "=" * 60)
    print("VIETNAMESE COPY GENERATION RESULTS")
    print("=" * 60)

    for platform, copies in results["copy"].items():
        print(f"\n📱 {platform.upper()}")
        print("-" * 60)

        for copy in copies:
            print(f"\nVariant: {copy.get('variant', 'default')} ({copy.get('tone', 'casual')})")
            print(f"\n{copy['copy']['body']}")
            print(f"\nHashtags: {' '.join(copy['copy']['hashtags'])}")
            print(f"CTA: {copy['copy']['call_to_action']}")

            # Metadata
            meta = copy['metadata']
            print(f"\n📊 Metadata:")
            print(f"  Characters: {meta['character_count']} / {meta['character_limit']}")
            print(f"  Within limit: {'✅' if meta['within_limit'] else '❌'}")
            print(f"  Hashtags: {meta['hashtag_validation']['count']} (valid: {meta['hashtag_validation']['valid']})")
            print(f"  Emojis: {meta['emoji_analysis']['emoji_count']} - {meta['emoji_analysis']['recommendation']}")
