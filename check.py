from time import sleep
import requests
import urllib
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

def check_balance_btc(data=generate_addresses(100), proxy=""):
	try:
		addresses = "|".join(data.keys())
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Firefox/116.0"
		}
		url = f"https://blockchain.info/multiaddr?active={addresses}"
		if(proxy != ""):
			prox = {
				"http": f"http://{proxy}/",
				"https": f"http://{proxy}/"
			}
			response = requests.get(url, headers=headers, proxies=prox).json()
		else:
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

def check_proxy_list(proxy_list_path):
	print("Checking proxy list...")
	proxy_list = open(proxy_list_path, 'r')
	proxies = proxy_list.readlines()
	for proxy in proxies:
		proxy = proxy.replace('\n','')
		prox = {
			"http": f"http://{proxy}/",
			"https": f"http://{proxy}/"
		}
		try:
			response = requests.get("http://ifconfig.me/ip", proxies=prox, timeout=5)
			assert response.text in proxy
		except:
			pass
		else:
			valid = open('validProxy.txt', 'a')
			valid.write(proxy + "\n")
			valid.close()
			print(f"\033[92mProxy {proxy} valid")
	exit()

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