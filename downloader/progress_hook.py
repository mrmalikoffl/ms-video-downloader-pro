async def progress_hook(d, message):
    """Send progress updates."""
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "0%").strip()
        await message.reply_text(f"⏬ Downloading: {percent}")