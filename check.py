import re
from time import sleep
from datetime import datetime
from urllib.request import urlopen
from loguru import logger

# No proxy

SATOSHI_PER_BTC: float = 1e8


def check_balance_bc(address):
    try:
        blockchain_tags_json = [
            "total_received",
            "final_balance",
        ]

        check_address: object = address
        reading_state: int = 1
        # keeps reading till OK
        while reading_state:
            try:
                htmlfile = urlopen(
                    "https://blockchain.info/address/%s?format=json" % check_address,
                    timeout=10,
                )
                htmltext = htmlfile.read().decode("utf-8")
                reading_state = 0
            except Exception as err:
                logger.exception(err)
                reading_state += 1
                sleep(60 * reading_state)

        blockchain_info_array = []
        tag = ""
        try:
            for tag in blockchain_tags_json:
                blockchain_info_array.append(
                    float(re.search(r'%s":(\d+),' % tag, htmltext).group(1))
                )
        except Exception as err:
            logger.exception(err)
            pass
        for i, btc_tokens in enumerate(blockchain_info_array):

            if btc_tokens > 0.0:
                return btc_tokens / SATOSHI_PER_BTC
            else:
                return 0
    except Exception as err:
        logger.exception(err)
        pass


def check_balance_btc(address):
    # get json data from https://chain.api.btc.com/v3/address/1assTGVhuCnrix5LvhL2GXEkSS3fS2XBT and parse it
    # to get the balance
    try:
        reading_state = 1
        while reading_state:
            try:
                htmlfile = urlopen(
                    "https://chain.api.btc.com/v3/address/%s?format=json" % address,
                    timeout=10,
                )
                htmltext = htmlfile.read().decode("utf-8")
                reading_state = 0
            except Exception as err:
                logger.exception(err)
                reading_state += 1
                sleep(60 * reading_state)
        balance = float(re.search(r'"balance":(\d+\.\d+),', htmltext).group(1))
        return balance
    except Exception as err:
        logger.exception(err)
        return None


def last_seen_bc(address):
    try:
        address = address
        reading_state = 1
        while reading_state:
            try:
                htmlfile = urlopen(
                    "https://blockchain.info/q/addressfirstseen/%s?format=json" % address,
                    timeout=10,
                )
                htmltext = htmlfile.read().decode("utf-8")
                reading_state = 0
            except Exception as err:
                logger.exception(err)
                reading_state += 1
                sleep(60 * reading_state)
        ts = int(htmltext)
        if ts == 0:
            return 0
        return str(datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as err:
        logger.exception(err)
        return None
