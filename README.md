# 🌟 Premium Telegram Video Downloader Bot

A professional Telegram bot for downloading videos from YouTube, Instagram Reels, and Twitter/X with premium subscriptions, admin features, and dual payment options (Telegram Stars and UPI).

## Features
- 📹 Download videos from YouTube, Instagram Reels, and Twitter/X.
- 🎨 Quality selection: 360p, 720p, 1080p (/quality).
- ⏳ Real-time download progress.
- 🚦 Rate limiting: 5 downloads/hour (free); unlimited (premium/admins).
- 🌟 Premium subscriptions:
  - Telegram Stars: Daily (100 Stars), Weekly (250), Monthly (500), Yearly (1000).
  - UPI: Daily ($1/₹85), Weekly ($2.50/₹210), Monthly ($5/₹420), Yearly ($10/₹840).
- 🛠️ Admin commands: /grant_premium, /revoke_premium, /users_list, /premium_users_list, /admin_stats.
- 📊 User stats: /stats.
- ℹ️ Bot info: /bot_info.
- 🎉 Attractive messages with emojis.
- ⚠️ Legal disclaimers.
- ☁️ Heroku deployment.

## Prerequisites
- Python 3.8+
- Telegram account and BotFather token
- Git and Heroku CLI
- FFmpeg (for future compression)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/telegram-video-downloader.git
cd telegram-video-downloader

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate