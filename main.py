from btcaddr import Wallet
from check import check_balance_bc, last_seen_bc
import threading
from discord_webhook import DiscordWebhook
import argparse
import os
from colorama import init

init()

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--threads",
    help="amount of threads (default: 100)",
    type=int,
    default=100,
)
parser.add_argument(
    "-s",
    "--savedry",
    help="save empty wallets",
    action="store_true",
    default=False,
)
parser.add_argument(
    "-p",
    "--proxy",
    help="use a proxy (host:port) (coming soon)",
)
parser.add_argument(
    "--proxy_auth",
    help="proxy credantials (user:pass) (coming soon)",
)
parser.add_argument(
    "-v",
    "--verbose",
    help="increases output verbosity",
    action="store_true",
)
parser.add_argument(
    "-d",
    "--discord",
    help="send a discord notification."
)

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
            wallet = Wallet()
            prv = wallet.key.__dict__["mainnet"].__dict__["wif"]
            addr = wallet.address.__dict__["mainnet"].__dict__["pubaddr1"]
            balance = int(check_balance_bc(addr))
            if balance == 0:
                if last_seen_bc(addr) == 0:
                    if args.savedry:
                        with open("results/dry.txt", "a") as w:
                            w.write(
                                f"Address: {addr} | Balance: {balance} | Private key: {prv}\n"
                            )
                    print(f"{bcolors.RED}{addr} : {prv} : {balance} BTC")
                else:
                    with open("results/moist.txt", "a") as w:
                        w.write(
                            f"Address: {addr} | Balance: {balance} | Private key: {prv} | Last seen: {last_seen_bc(addr)}\n"
                        )
                    print(
                        f"{bcolors.YELLOW}{last_seen_bc(addr)} : {balance} : {prv} : {addr}"
                    )
            else:
                with open("results/wet.txt", "a") as w:
                    w.write(
                        f"Address: {addr} | Balance: {balance} | Private key: {prv} | Last seen: {last_seen_bc(addr)}\n"
                    )
                    if args.discord:
                        webhook = DiscordWebhook(url=args.discord,
                                                 rate_limit_retry=True,
                                                 content=f'@everyone Address: {addr} | '
                                                         f'Balance: {balance} | '
                                                         f'Private key: {prv}')
                        response = webhook.execute()
                print(f"{last_seen_bc(addr)} {bcolors.GREEN} : {balance} : {prv} : {addr}")


if __name__ == "__main__":
    makeDir()
    threads = args.threads
    for _ in range(threads):
        th = threading.Thread(target=main, args=())
        th.start()
