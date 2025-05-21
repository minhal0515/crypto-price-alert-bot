from pycoingecko import CoinGeckoAPI
from telegram import Bot
import asyncio
import time

def price_tracking():
	cg = CoinGeckoAPI()
	targets = {
		'bitcoin' : 65000,
		'ethereum' : 4000,
		'possum' : 0.00095
	}
	met_targets = {}
	for crypto, crypto_target in targets.items():
		response = cg.get_price(ids = crypto, vs_currencies = 'usd')
		current_price = response[crypto]['usd']
		target_price = targets[crypto]

		if current_price >= targets[crypto]:
			met_targets[crypto] = current_price

	print(met_targets)

	if met_targets:
		message_body = 'congrats, you made some money!\n\n'

		for crypto, crypto_price in met_targets.items():
			current_price = crypto_price
			target_price = targets[crypto]
			message_body += (f'{crypto}\n'
							 f'Current price: {current_price}\n'
							 f'Target price: {target_price}\n')

	
	asyncio.run(send_telegram_message(message_body))


async def send_telegram_message(message):
	bot_token = '8124868472:AAEeKP5wQeu8-2rQ97QLFn92QVmNTAwPv90'
	chatID = '1364147094'

	bot = Bot(token = bot_token)
	await bot.send_message(chat_id = chatID, text = message)

price_tracking()

while True:
	price_tracking()
	time.sleep(60)