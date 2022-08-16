import re
from time import sleep
from datetime import datetime
from urllib.request import urlopen

# No proxy
def check_balance_bc(address):
    try:
        blockchain_tags_json = [
            "total_received",
            "final_balance",
        ]

        SATOSHIS_PER_BTC = 1e8

        check_address = address
        reading_state = 1
        # keeps reading till OK
        while reading_state:
            try:
                htmlfile = urlopen(
                    "https://blockchain.info/address/%s?format=json" % check_address,
                    timeout=10,
                )
                htmltext = htmlfile.read().decode("utf-8")
                reading_state = 0
            except:
                reading_state += 1
                sleep(60 * reading_state)

        blockchain_info_array = []
        tag = ""
        try:
            for tag in blockchain_tags_json:
                blockchain_info_array.append(
                    float(re.search(r'%s":(\d+),' % tag, htmltext).group(1))
                )
        except:
            pass
        for i, btc_tokens in enumerate(blockchain_info_array):

            if btc_tokens > 0.0:
                return btc_tokens / SATOSHIS_PER_BTC
            else:
                return 0
    except:
        pass


def check_balance_btc(address):
    # get json data from https://chain.api.btc.com/v3/address/1assTGVhuCnrix5LvhL2GXEkSS3fS2XBT and parse it
    # to get the balance
    try:
        address = address
        reading_state = 1
        while reading_state:
            try:
                htmlfile = urlopen(
                    "https://chain.api.btc.com/v3/address/%s?format=json" % address,
                    timeout=10,
                )
                htmltext = htmlfile.read().decode("utf-8")
                reading_state = 0
            except:
                reading_state += 1
                sleep(60 * reading_state)
        balance = float(re.search(r'"balance":(\d+\.\d+),', htmltext).group(1))
        return balance
    except:
        return None


def last_seen_bc(address):

    try:
        address = address
        reading_state = 1
        while reading_state:
            try:
                htmlfile = urlopen(
                    "https://blockchain.info/q/addressfirstseen/%s?format=json"
                    % address,
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
