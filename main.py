from check import check_balance_btc
import threading
from discord_webhook import DiscordWebhook
import argparse
import os
from colorama import init
from time import sleep
init()

parser = argparse.ArgumentParser()
parser.add_argument(
	"-t",
	"--threads",
	help="amount of threads (default: 50)",
	type=int,
	default=50,
)
parser.add_argument(
	"-s",
	"--savedry",
	help="save empty wallets",
	action="store_true",
	default=False,
)
parser.add_argument(
	"-v",
	"--verbose",
	help="increases output verbosity",
	action="store_true",
)
parser.add_argument("-d", "--discord", help="send a discord notification.")

args = parser.parse_args()
lock = threading.Lock()


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
				wallets = check_balance_btc()
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
						else:
							print(
								f"{bcolors.RED}[-] {wallet['address']} : {float(wallet['balance'])/1e8} BTC : {wallet['private']}{bcolors.RESET}",
								end="\r",
								flush=True,
							)
						sleep(0.01)
			except (TypeError, AttributeError):
				print("You are rate-limited please switch to a vpn/proxy or you dont have connection")
				pass


if __name__ == "__main__":
	makeDir()
	threads = args.threads
	for _ in range(threads):
		th = threading.Thread(target=main, args=())
		th.start()
