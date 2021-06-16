import re
from time import sleep

from urllib.request import urlopen


def check_balance(address):
    try:
        blockchain_tags_json = [
            "total_received",
            "final_balance",
        ]

        SATOSHIS_PER_BTC = 1e8

        check_address = address

        # Read info from Blockchain about the Address
        reading_state = 1
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
                return "0"
    except:
        pass
