from check import check_balance_btc, check_proxy_list
import threading
from discord_webhook import DiscordWebhook
import argparse
import requests
import os
from colorama import init
from time import sleep
init()

parser = argparse.ArgumentParser()
parser.add_argument(
	"-t",
	"--threads",
	help="Amount of threads (default: 50)",
	type=int,
	default=50,
)
parser.add_argument(
	"-s",
	"--savedry",
	help="Save empty wallets",
	action="store_true",
	default=False,
)
parser.add_argument(
	"-dp",
	"--disableprint",
	help="Disable printing of wallets (Printing in python greatly slows down the script. If you do not need wallets without balance to be printed to the console, then it is better to disable printing to increase performance)",
	action="store_true",
	default=False,
)
parser.add_argument(
	"-v",
	"--verbose",
	help="Increases output verbosity",
	action="store_true",
)
parser.add_argument("-d", "--discord", help="send a discord notification.")
parser.add_argument(
	"-tg", 
    "--telegram", 
    nargs=2,
    metavar=('botToken', 'chatId'),
    help="Send a telegram nostification. -tg <botToken> <chatId>",
)
parser.add_argument(
	"-p", 
    "--proxy",
    help="Use proxy. -p <ip:port> or <user:pass@ip:port>",
)
parser.add_argument("-cp", "--checkProxy", help="Check proxy list")

args = parser.parse_args()
lock = threading.Lock()
proxy = args.proxy

class bcolors:
	GREEN = "\033[92m"  # GREEN
	YELLOW = "\033[93m"  # YELLOW
	RED = "\033[91m"  # RED
	RESET = "\033[0m"  # RESET COLOR


def makeDir():
	path = "results"
	if not os.path.exists(path):
		os.makedirs(path)


def main():
	with lock:
		while True:
			try:
				wallets = check_balance_btc(proxy=proxy)
				for wallet in wallets:
					if wallet["balance"] > 0:
						print(
							f"{bcolors.GREEN}[+] {wallet['address']} : {float(wallet['balance'])/1e8} BTC : {wallet['private']}",
							flush=True,
						)
						# save wallet to file
						with open("results/wallets.txt", "a") as f:
							f.write(
								f"{wallet['address']} : {float(wallet['balance'])/1e8} BTC : {wallet['private']}\n"
							)
						if args.telegram:
							text_to_send = f"Found wallet with balance:\nBalance: `{wallet['balance']}`\nAddress: `{wallet['address']}`\nPrivate Key: `{wallet['private']}`"
							requests.get(f"https://api.telegram.org/bot{args.telegram[0]}/sendMessage?chat_id={args.telegram[1]}&text={text_to_send}&parse_mode=MarkDown")
						if args.discord:
							webhook = DiscordWebhook(
								url=args.discord,
								content=f"{wallet['address']} : {float(wallet['balance'])/1e8} BTC : {wallet['private']}",
							)
							response = webhook.execute()
					else:
						if args.savedry:
							with open("results/empty.txt", "a") as f:
								f.write(
									f"{wallet['address']} : {float(wallet['balance'])/1e8} BTC : {wallet['private']}\n"
								)
						if args.verbose:
							print(
								f"{bcolors.RED}[-] {wallet['address']} : {float(wallet['balance'])/1e8} BTC : {wallet['private']}{bcolors.RESET}",
								flush=True,
							)
						elif(args.disableprint == False):
							print(
								f"{bcolors.RED}[-] {wallet['address']} : {float(wallet['balance'])/1e8} BTC : {wallet['private']}{bcolors.RESET}",
								end="\r",
								flush=True,
							)
						sleep(0.01)
			except (TypeError, AttributeError):
				print("You are rate-limited please switch to a vpn/proxy or you dont have connection")
				exit()


if __name__ == "__main__":
	makeDir()
	if args.checkProxy:
		check_proxy_list(args.checkProxy)
	threads = args.threads
	for _ in range(threads):
		th = threading.Thread(target=main, args=())
		th.start()
