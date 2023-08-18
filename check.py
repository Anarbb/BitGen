from time import sleep
import requests
import json
from btcaddr import Wallet
from time import sleep
from fake_user_agent import user_agent

def generate_addresses(count):
	addresses = {}
	for i in range(count):
		wallet = Wallet()
		pub = wallet.address.__dict__["mainnet"].__dict__["pubaddr1"]
		prv = wallet.key.__dict__["mainnet"].__dict__["wif"]
		addresses[pub] = prv
	return addresses

def check_balance_btc(data=generate_addresses(100)):
	try:
		addresses = "|".join(data.keys())
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Firefox/116.0"
		}
		url = f"https://blockchain.info/multiaddr?active={addresses}"
		response = requests.get(url, headers=headers).json()
		sleep(0.5)
		extract = []
		for address in response["addresses"]:
			# add all data into a list
			extract.append({
				"address": address["address"],
				"balance": address["final_balance"],
				"private": data[address["address"]]
			})
		return extract
	except:
		pass

"""def last_seen_bc(address):

	try:
		address = address
		reading_state = 1
		while reading_state:
			try:
				htmlfile = urlopen(
					f"https://blockchain.info/q/addressfirstseen/{address}?format=json",
					timeout=10,
				)
				htmltext = htmlfile.read().decode("utf-8")
				reading_state = 0
			except:
				reading_state += 1
				sleep(60 * reading_state)
		ts = int(htmltext)
		if ts == 0:
			return 0
		return str(datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))
	except:
		return None
"""