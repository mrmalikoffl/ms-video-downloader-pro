async def send_upi_instructions(bot, user_id: int, plan: str, days: int, usd: float, inr: float):
    """Send UPI payment instructions."""
    await bot.send_message(
        chat_id=user_id,
        text=(
            f"💳 UPI Payment for {plan.capitalize()} Premium ({days} days):\n"
            f"Amount: ${usd} / ₹{inr}\n"
            f"UPI ID: msmalikoffl-1@okicici\n\n"
            "1. Pay the amount via any UPI app.\n"
            "2. Take a screenshot of the payment.\n"
            "3. Send the screenshot to @YourTelegramAccount.\n"
            "4. Admin will grant your premium status.\n\n"
            "⚠️ Ensure the payment is correct to avoid delays."
        )
    )