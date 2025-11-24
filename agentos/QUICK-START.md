# TextCreator Agent - Quick Start ⚡

**Generate Vietnamese social media copy in 30 seconds!**

---

## 🚀 Fastest Way to Run

```bash
cd /home/cid/projects/agent-research/agentos/
pip install -r requirements.txt
python test_textcreator.py
```

**Done!** Vietnamese copy for Facebook, TikTok, and Shopee will print to your terminal.

---

## 📋 What You Get

### Facebook Copy (300+ chars)
```
Hôm nay mình review cho các bạn cây son lì này nha! 💄

Thật ra lúc đầu mình cũng hơi nghi ngờ...
#ReviewSảnPhẩm #SonLì #LàmĐẹp
```

### TikTok Copy (200 chars)
```
Trend làm đẹp hot nhất tuần này! 🔥
Thử ngay beauty hack với son lì bền màu 24h 💄✨
#BeautyHacks #LàmĐẹp #TikTokShop
```

### Shopee Description (500+ chars)
```
SON LÌ BỀN MÀU 24H - CHÍNH HÃNG 💄
🌟 ĐẶC ĐIỂM NỔI BẬT:
• Màu sắc chuẩn, bền màu 24 giờ
• Công thức lì mượt, không khô môi
...
```

---

## 🎯 Use the API

**Start server:**
```bash
python main.py
# Server runs at http://localhost:8080
```

**Generate copy:**
```bash
curl -X POST "http://localhost:8080/api/v1/content/generate-copy?brief_id=%23BeautyHacks&platforms=facebook&platforms=tiktok"
```

**Get response in JSON with:**
- Vietnamese copy for each platform
- Character count validation
- Hashtag optimization
- Emoji analysis
- Ready-to-publish status

---

## 💡 Common Commands

**Test standalone:**
```bash
python test_textcreator.py
```

**Run server:**
```bash
python main.py
```

**Check health:**
```bash
curl http://localhost:8080/health
```

**View metrics:**
```bash
curl http://localhost:8080/metrics | grep agent_executions
```

---

## 📝 Platform Guidelines

| Platform | Optimal Length | Hashtags | Emojis |
|----------|---------------|----------|--------|
| **Facebook** | 40-80 chars | 4-8 | 3-5 |
| **TikTok** | 200-300 chars | 8-10 | 4-6 |
| **Shopee** | 500-800 chars | 3-5 | 2-4 |
| **Instagram** | 125-150 chars | 8-12 | 3-5 |

---

## 🐛 Troubleshooting

**Issue:** Module not found
```bash
pip install -r requirements.txt
```

**Issue:** Database connection failed
```bash
docker run -d -p 5432:5432 --name postgres-pgvector \
  -e POSTGRES_PASSWORD=password pgvector/pgvector:pg16
```

**Issue:** No output
```bash
# Check logs
python test_textcreator.py 2>&1 | tee output.log
```

---

## 💰 Cost

- **Per content piece:** $0.02
- **100 posts/month:** $2
- **500x cheaper** than human copywriter

---

## 📚 More Info

- **Full Guide:** `HOW-TO-RUN.md`
- **Summary:** `TEXTCREATOR-SUMMARY.md`
- **Code:** `agents/text_creator.py`

---

**Questions? Check the docs or run `python test_textcreator.py` to see it in action!**
