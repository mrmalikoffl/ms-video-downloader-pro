# MS Video Downloader Pro 🎥

**MS Video Downloader Pro** is a Telegram bot that lets you download videos from platforms like YouTube, Instagram, and TikTok directly in Telegram! 🚀 Built with Python and powered by `yt-dlp`, it’s easy to use and deployable on Heroku for 24/7 access. 📱💻

## Features ✨

- 📹 Download videos from YouTube, Instagram, TikTok, and more.
- 🎞️ Supports multiple formats (MP4, MP3) and resolutions (720p, 1080p).
- 🛠️ Simple Telegram interface with intuitive commands.
- 🚫 Robust error handling for invalid URLs or unsupported sites.
- ☁️ Easy Heroku deployment for constant availability.
- 🔒 Secure: Uses environment variables for sensitive data.

## Prerequisites 📋

Before setting up, you’ll need:

- 🤖 A Telegram account and a bot token from [BotFather](https://t.me/BotFather).
- 🐍 Python 3.10+ installed locally for testing.
- ☁️ A Heroku account with a paid plan (Eco, Basic, or Standard).
- 🌳 Git for version control.
- 🎬 (Optional) `ffmpeg` for video processing (handled automatically on Heroku).

## Installation (Local Setup) 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mrmalikoffl/ms-video-downloader-pro.git
   cd ms-video-downloader-pro

## Create a virtual environment (recommended):
bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install dependencies:
bash

pip install -r requirements.txt

## Set environment variables:
Create a .env file in the project root and add your Telegram bot token:

TELEGRAM_BOT_TOKEN=your_bot_token_here

Or export it manually:
bash

export TELEGRAM_BOT_TOKEN=your_bot_token_here

## Run the bot locally:
bash

python bot.py

## Test the bot:
Open Telegram, find your bot (e.g., @MSVideoDownloaderPro), and send /start to check it’s working! 

## Usage 
Interact with the bot on Telegram using these commands:
/start: Shows a welcome message and instructions .

/download <video_url>: Downloads a video from the given URL (e.g., /download https://www.youtube.com/watch?v=example) .

/help: Lists all commands and tips .

Example:

@MSVideoDownloaderPro /download https://www.youtube.com/watch?v=dQw4w9WgXcQ

The bot will process the URL and send the video file (or a link for large files) in the chat! 
Notes:
 Supported platforms: YouTube, Instagram, TikTok, and more (check yt-dlp supported sites).

 File size limits: Telegram caps files at 50 MB (2 GB for premium users). Large files may be uploaded to a cloud service with a shared link.

## Deployment on Heroku 
To deploy the bot on Heroku for 24/7 availability:
Install Heroku CLI:
Download and install from Heroku CLI .

## Log in to Heroku:
bash

heroku login

## Create a Heroku app:
bash

heroku create ms-video-downloader-pro

## Set environment variables:
bash

heroku config:set TELEGRAM_BOT_TOKEN=your_bot_token_here

## Add buildpacks (for Python and ffmpeg):
bash

heroku buildpacks:set heroku/python
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

## Deploy the code:
bash

git add .
git commit -m "Deploy to Heroku"
git push heroku main

## Scale the worker:
bash

heroku ps:scale worker=1

## Check logs for debugging:
bash

heroku logs --tail

## Set up Telegram webhook (optional, if using webhooks instead of polling):
bash

heroku domains  # Get your Heroku app URL (e.g., https://ms-video-downloader-pro.herokuapp.com)

## Configure the webhook with Telegram:
bash

curl -F "url=https://ms-video-downloader-pro.herokuapp.com/your_bot_token" https://api.telegram.org/bot<your_bot_token>/setWebhook

Your bot is now live on Heroku and ready to use on Telegram! 
Troubleshooting 
 Bot not responding: Check Heroku logs (heroku logs --tail) for errors. Ensure TELEGRAM_BOT_TOKEN is set correctly.

 Dependency issues: Verify requirements.txt includes all packages and versions.

 Large file issues: For videos over 50 MB, consider adding cloud storage (e.g., Google Drive) to share links.

 Rate limits: Telegram may limit messages. The bot includes retry logic, but avoid spamming commands.

## Contributing 
We love contributions! To contribute:
 Fork the repository.

 Create a new branch: git checkout -b feature/your-feature-name.

 Make changes and commit: git commit -m "Add your feature".

 Push to your fork: git push origin feature/your-feature-name.

 Open a pull request with a clear description of your changes.

Please follow the Code of Conduct (CODE_OF_CONDUCT.md) and check the Contributing Guidelines (CONTRIBUTING.md) for details.
## License 
This project is licensed under the MIT License. See the LICENSE file for details.
Contact 
For questions, suggestions, or issues:
 Open an issue on this repository.

 Contact the developer: mrmalikoffl.

(Add Telegram support group link here if available).

Happy downloading! 

### How to Use
1. **Copy the Content**: Select and copy the entire Markdown text above.
2. **Go to GitHub**:
   - Navigate to your repository: `https://github.com/mrmalikoffl/ms-video-downloader-pro`.
   - If `README.md` exists, click the pencil icon to edit.
   - If it doesn’t, click “Create new file”, name it `README.md`, and paste the content.
3. **Paste and Commit**:
   - Paste the copied text into the editor.
   - Commit with a message like “Add README.md” or “Update README.md”.
4. **Preview**: GitHub will render the README with emojis and formatting on your repo’s main page.

### Customization Notes
- **Bot Handle**: Replace `@MSVideoDownloaderPro` with your bot’s actual Telegram handle (e.g., `@MyVideoBot`).
- **Supported Platforms**: Update the list (e.g., add Vimeo, remove TikTok) to match your bot’s capabilities.
- **Commands**: Adjust `/start`, `/download`, `/help` to reflect your bot’s actual commands.
- **Cloud Storage**: If you’ve implemented a solution for large files (e.g., Google Drive, `transfer.sh`), add details under “Features” or “Usage”.
- **Contact**: Include your email, Telegram group, or other contact methods in the “Contact” section.
- **License**: Assumes MIT License. Change to GPL or another license if preferred, and create a matching `LICENSE` file.
- **Webhook/Polling**: If you’re using polling only, remove the webhook setup step or clarify your choice.

### Additional Files to Create
To align with the README, you may need:
- **LICENSE**: Create a `LICENSE` file with MIT License text ([available here](https://opensource.org/licenses/MIT)).
- **requirements.txt**: List dependencies, e.g.:
  ```plaintext
  python-telegram-bot==13.7
  yt-dlp==2023.7.6
  requests==2.28.1

Procfile: Add worker: python bot.py for Heroku.

.gitignore: Include:
plaintext

__pycache__/
*.pyc
.env
*.log

CONTRIBUTING.md (optional): Add contribution guidelines.

CODE_OF_CONDUCT.md (optional): Use a template like Contributor Covenant.

## Verification Checklist
Ensure the bot token is not hard-coded (use .env locally and Heroku Config Vars).

Test the bot locally to confirm commands (e.g., /start, /download) work.

Verify Heroku setup matches the README (e.g., Python version in runtime.txt, buildpacks).

Check that requirements.txt and Procfile exist and are correct.

