#  Bitcoin Address  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/bitcoinaddress
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.

import hashlib
from abc import ABC
import base58
from binascii import hexlify, unhexlify
from ..key.seed import Seed
from ..util import checksum


class Key:
    class Net(ABC):
        def __init__(self):
            self.wif = None
            self.wifc = None

    class MainNet(Net):
        PREFIX = b"\x80"
        SUFFIX = b"\x01"

        def __init__(self, instance):
            self.instance = instance

        def generate_wif(self):
            self.wif = self.instance._generate_wif(Key.MainNet.PREFIX)

        def generate_wif_compressed(self):
            self.wifc = self.instance._generate_wif_compressed(
                Key.MainNet.PREFIX, Key.MainNet.SUFFIX
            )

    class TestNet(Net):
        PREFIX = b"\xEF"
        SUFFIX = b"\x01"

        def __init__(self, instance):
            self.instance = instance

        def generate_wif(self):
            self.wif = self.instance._generate_wif(Key.TestNet.PREFIX)

        def generate_wif_compressed(self):
            self.wifc = self.instance._generate_wif_compressed(
                Key.TestNet.PREFIX, Key.TestNet.SUFFIX
            )

    def __init__(self):
        self.seed = None
        self.digest = None
        self.hex = None
        self.mainnet = Key.MainNet(self)
        self.testnet = Key.TestNet(self)

    @staticmethod
    def of(obj):
        key = Key()
        if isinstance(obj, Seed):
            key._from_seed(obj)
        else:
            try:
                if len(obj) == 64:
                    key._from_hex(obj)
                    return key
                if len(obj) == 51:
                    key._from_wif(obj)
                    return key
                if len(obj) == 52:
                    pass  # TODO
            except:
                raise Exception("Unsupported format.")

        return key

    def _from_seed(self, seed: Seed):
        self.seed = seed
        self._generate_digest()
        self._generate_hex()
        self.mainnet.generate_wif()
        self.mainnet.generate_wif_compressed()
        self.testnet.generate_wif()
        self.testnet.generate_wif_compressed()

    def _from_hex(self, hex: str):
        self.hex = hex
        self.digest = unhexlify(hex)
        self.mainnet.generate_wif()
        self.mainnet.generate_wif_compressed()
        self.testnet.generate_wif()
        self.testnet.generate_wif_compressed()

    def _from_wif(self, wif: str):
        checksum_size = 4
        self.digest = base58.b58decode(wif)[1:-checksum_size]
        self._generate_hex()
        self.mainnet.generate_wif()
        self.mainnet.generate_wif_compressed()
        self.testnet.generate_wif()
        self.testnet.generate_wif_compressed()

    def _generate_digest(self):
        entropy = str(self.seed.entropy)
        hash = hashlib.sha256(entropy.encode())
        self.digest = hash.digest()

    def _generate_hex(self):
        self.hex = hexlify(self.digest).decode()

    def _generate_wif(self, prefix):
        digest = prefix + self.digest
        c = checksum(digest)
        return base58.b58encode(digest + c).decode("utf-8")

    def _generate_wif_compressed(self, prefix, suffix):
        digest = prefix + self.digest
        c = checksum(digest + suffix)
        return base58.b58encode(digest + suffix + c).decode("utf-8")

    def __str__(self, testnet=False):
        if testnet:
            params = (self.hex, self.testnet.wif, self.testnet.wifc)
        else:
            params = (self.hex, self.mainnet.wif, self.mainnet.wifc)

        return """
              \rPrivate Key HEX: %s
              \rPrivate Key WIF: %s
              \rPrivate Key WIF compressed: %s 
            """ % (
            params
        )
