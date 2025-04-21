from telegram import LabeledPrice

async def send_stars_invoice(bot, user_id: int, title: str, description: str, payload: str, stars: int):
    """Send a Telegram Stars invoice."""
    prices = [LabeledPrice(title, stars)]
    await bot.send_invoice(
        chat_id=user_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="",  # Empty for Stars
        currency="XTR",
        prices=prices,
        is_flexible=False,
    )