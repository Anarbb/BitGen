from btcaddr import Wallet
from check import check_balance_bc, last_seen_bc
import threading
from multiprocessing.pool import ThreadPool as Pool
import argparse
import requests
import os

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


def getInternet():
    try:
        try:
            requests.get("http://1.1.1.1")
        except requests.ConnectTimeout:
            requests.get("http://216.58.213.14")
        return True
    except requests.ConnectionError:
        return False


def main():
    with lock:
        while 1:
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
                print(f"{last_seen_bc(addr)} {bcolors.OK} : {balance} : {prv} : {addr}")


if __name__ == "__main__":
    if not getInternet():
        print(bcolors.RED + "No internet connection")
    makeDir()
    threads = args.threads
    pool = Pool(threads)
    for _ in range(threads):
        pool.apply_async(main, ())
    pool.close()
    pool.join()
