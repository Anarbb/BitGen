#  Bitcoin Address  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/bitcoinaddress
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.

from .key.key import Key
from . import Address, Seed


class Wallet:
    def __init__(self, hash_or_seed=None, testnet=False):
        if hash_or_seed is None:
            hash_or_seed = Seed()
        self.key = Key.of(hash_or_seed)
        self.address = Address.of(self.key)
        self.testnet = testnet

    def __str__(self):
        return """%s\n%s""" % (
            self.key.__str__(self.testnet),
            self.address.__str__(self.testnet),
        )


if __name__ == "__main__":
    wallet = Wallet()
    print(wallet)
