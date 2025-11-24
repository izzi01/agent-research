#!/usr/bin/env python3
"""
Quick test script for TextCreator agent

Run this to test the TextCreator agent without the full server.
"""

from agents.text_creator import TextCreator
import os
import sys

def main():
    print("\n" + "=" * 60)
    print("🤖 TEXTCREATOR AGENT - QUICK TEST")
    print("=" * 60)

    # Initialize agent
    print("\n📝 Initializing TextCreator agent...")
    db_url = os.getenv("DATABASE_URL", "postgresql://agno:password@localhost:5432/marketing_automation")

    try:
        agent = TextCreator(db_url=db_url)
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\n💡 Tip: Make sure PostgreSQL is running:")
        print("   docker run -d -p 5432:5432 --name postgres-pgvector pgvector/pgvector:pg16")
        sys.exit(1)

    # Sample content brief (from ContentStrategist)
    sample_brief = {
        "trend_id": "#BeautyHacks",
        "vietnamese_hook": "Chị em ơi! Trend làm đẹp này đang gây bão TikTok, mình phải thử ngay! 💄✨",
        "content_angle": "Product Review + Tutorial - Show before/after transformation using the product while riding the trending beauty hack wave",
        "products": ["PROD001 - Son Lì Bền Màu 24H"],
        "hashtags": ["#BeautyHacks", "#ReviewSảnPhẩm", "#LàmĐẹp", "#BeautyVietNam", "#TikTokShop"],
        "vietnamese_voiceover": "Chào các bạn! Hôm nay mình sẽ review cho các bạn cây son lì này đang được nhiều bạn hỏi..."
    }

    print("\n📋 Content Brief:")
    print(f"   Trend: {sample_brief['trend_id']}")
    print(f"   Hook: {sample_brief['vietnamese_hook'][:50]}...")
    print(f"   Products: {', '.join(sample_brief['products'])}")

    # Test 1: Generate copy for multiple platforms
    print("\n" + "-" * 60)
    print("TEST 1: Generate Copy for Facebook, TikTok, Shopee")
    print("-" * 60)

    results = agent.run_copy_generation(
        brief=sample_brief,
        platforms=["facebook", "tiktok", "shopee"],
        generate_variants=False
    )

    print(f"\n✅ Generated copy for {len(results['platforms'])} platforms\n")

    for platform, copies in results["copy"].items():
        copy = copies[0]  # First variant

        print(f"{'=' * 60}")
        print(f"📱 {platform.upper()} COPY")
        print(f"{'=' * 60}")
        print(f"\nVariant: {copy.get('variant', 'default')} | Tone: {copy.get('tone', 'casual')}")
        print(f"\n{copy['copy']['body']}")
        print(f"\n📌 Hashtags: {' '.join(copy['copy']['hashtags'])}")
        print(f"✨ CTA: {copy['copy']['call_to_action']}")

        # Metadata
        meta = copy['metadata']
        print(f"\n📊 Stats:")
        print(f"   • Characters: {meta['character_count']} / {meta['character_limit']}")
        print(f"   • Within limit: {'✅' if meta['within_limit'] else '⚠️  (exceeds optimal length)'}")
        print(f"   • Hashtags: {meta['hashtag_validation']['count']} {'✅' if meta['hashtag_validation']['valid'] else '❌'}")
        print(f"   • Emojis: {meta['emoji_analysis']['emoji_count']} - {meta['emoji_analysis']['recommendation']}")
        print()

    # Test 2: Generate A/B variants
    print("\n" + "-" * 60)
    print("TEST 2: Generate A/B Testing Variants (Facebook)")
    print("-" * 60)

    ab_results = agent.generate_ab_variants(
        brief=sample_brief,
        platform="facebook",
        num_variants=3
    )

    print(f"\n✅ Generated {len(ab_results)} A/B testing variants\n")

    for i, variant in enumerate(ab_results, 1):
        print(f"\nVariant #{i}: {variant['variant']} ({variant['tone']})")
        print(f"ID: {variant['variant_id']}")
        print(f"Copy: {variant['copy']['body'][:100]}...")
        print(f"Characters: {variant['metadata']['character_count']}")

    # Summary
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   • Platforms tested: {len(results['platforms'])}")
    print(f"   • Total copy generated: {sum(len(copies) for copies in results['copy'].values())}")
    print(f"   • A/B variants: {len(ab_results)}")
    print(f"\n💡 Next steps:")
    print(f"   1. Review the Vietnamese copy above")
    print(f"   2. Adjust tone/variant for your brand")
    print(f"   3. Integrate with real Claude API for production")
    print(f"   4. Connect to publishing workflow\n")


if __name__ == "__main__":
    main()
