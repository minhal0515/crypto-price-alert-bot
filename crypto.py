from pycoingecko import CoinGeckoAPI
from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio
import time

# Load .env values
load_dotenv()
bot_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

cg = CoinGeckoAPI()

targets = {
    'bitcoin': 65000,
    'ethereum': 4000,
    'possum': 0.00095
}

async def send_telegram_message(message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

def check_targets():
    met_targets = {}
    for crypto, target_price in targets.items():
        response = cg.get_price(ids=crypto, vs_currencies='usd')
        current_price = response[crypto]['usd']

        if current_price >= target_price:
            met_targets[crypto] = current_price
    return met_targets

async def main_loop():
    while True:
        met_targets = check_targets()
        if met_targets:
            message_body = '🎉 Congrats! Price targets met:\n\n'
            for crypto, price in met_targets.items():
                message_body += f"{crypto.capitalize()} - ${price:.2f} (Target: ${targets[crypto]})\n"
            await send_telegram_message(message_body)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main_loop())
