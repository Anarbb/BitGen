import requests
from time import sleep
from datetime import datetime


# No proxy
def check_balance_bc(address):
    try:
        blockchain_tags_json = [
            "total_received",
            "final_balance",
        ]

        SATOSHI_PER_BTC = 1e8

        reading_state = 1

        # keeps reading till OK
        while reading_state:
            try:
                _response = requests.get(
                    "https://blockchain.info/address/%s?format=json" % address,
                    timeout=10,
                ).json()
                reading_state = 0
            except Exception as e:
                print(e)  # todo Add logger
                reading_state += 1
                sleep(60 * reading_state)

        blockchain_info_array = [_response.get(key) for key in blockchain_tags_json]

        for btc_tokens in blockchain_info_array:
            if btc_tokens > 0.0:
                return btc_tokens / SATOSHI_PER_BTC
            return False
    except Exception as e:
        print(e)  # todo Add logger
        return None


def check_balance_btc(address):
    # get json data from https://chain.api.btc.com/v3/address/1assTGVhuCnrix5LvhL2GXEkSS3fS2XBT and parse it
    # to get the balance
    try:
        reading_state = 1
        while reading_state:
            try:
                _response = requests.get(
                    "https://chain.api.btc.com/v3/address/%s?format=json" % address,
                    timeout=10,
                ).json()['data']
                reading_state = 0
            except Exception as e:
                print(e)  # todo Add logger
                reading_state += 1
                sleep(60 * reading_state)
        return _response['balance']
    except Exception as e:
        print(e)  # todo Add logger
        return None


def last_seen_bc(address):
    try:
        reading_state = 1
        while reading_state:
            try:
                _response = requests.get(
                    "https://blockchain.info/q/addressfirstseen/%s?format=json" % address,
                    timeout=10,
                ).json()
                reading_state = 0
            except Exception as e:
                print(e)  # todo Add logger
                reading_state += 1
                sleep(60 * reading_state)
        if _response == 0:
            return 0
        return str(datetime.utcfromtimestamp(_response).strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print(e)  # todo Add logger
        return None
