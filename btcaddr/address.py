#  Bitcoin Address  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/bitcoinaddress
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.
import hashlib
from abc import ABC
import base58
import binascii
from .key.key import Key
from . import segwit_addr
from .util import hash160, ecdsa_secp256k1, checksum


class Address:
    PREFIX_EVEN = b"\x02"
    PREFIX_ODD = b"\x03"
    WITNESS_VERSION = 0x00

    class Net(ABC):
        def __init__(self):
            self.pubaddr1 = None
            self.pubaddr1c = None
            self.pubaddr3 = None
            self.pubaddrbc1_P2WPKH = None
            self.pubaddrbc1_P2WSH = None

    class MainNet(Net):
        PREFIX_A = b"\x00"
        PREFIX_B = b"\x04"
        SEGWIT_PREFIX = b"\x05"
        BECH32_PREFIX = "bc"

        def __init__(self, instance):
            self.instance = instance

        def generate_publicaddress1(self):
            self.pubaddr1 = self.instance._generate_publicaddress1(
                Address.MainNet.PREFIX_A, Address.MainNet.PREFIX_B
            )

        def generate_publicaddress1_compressed(self):
            self.pubaddr1c = self.instance._generate_publicaddress1_compressed(
                Address.MainNet.PREFIX_A
            )

        def generate_publicaddress3(self):
            self.pubaddr3 = self.instance._generate_publicaddress3(
                Address.MainNet.SEGWIT_PREFIX
            )

        def generate_publicaddress_bc1_P2WPKH(self):
            self.pubaddrbc1_P2WPKH = (
                self.instance._generate_publicaddress_bech32_P2WPKH(
                    Address.MainNet.BECH32_PREFIX
                )
            )

        def generate_publicaddress_bc1_P2WSH(self):
            self.pubaddrbc1_P2WSH = self.instance._generate_publicaddress_bech32_P2WSH(
                Address.MainNet.BECH32_PREFIX
            )

    class TestNet(Net):
        PREFIX_A = b"\x6F"
        PREFIX_B = b"\x04"
        SEGWIT_PREFIX = b"\xC4"
        BECH32_PREFIX = "tb"

        def __init__(self, instance):
            self.instance = instance

        def generate_publicaddress1(self):
            self.pubaddr1 = self.instance._generate_publicaddress1(
                Address.TestNet.PREFIX_A, Address.TestNet.PREFIX_B
            )

        def generate_publicaddress1_compressed(self):
            self.pubaddr1c = self.instance._generate_publicaddress1_compressed(
                Address.TestNet.PREFIX_A
            )

        def generate_publicaddress3(self):
            self.pubaddr3 = self.instance._generate_publicaddress3(
                Address.TestNet.SEGWIT_PREFIX
            )

        def generate_publicaddress_tb1_P2WPKH(self):
            self.pubaddrtb1_P2WPKH = (
                self.instance._generate_publicaddress_bech32_P2WPKH(
                    Address.TestNet.BECH32_PREFIX
                )
            )

        def generate_publicaddress_tb1_P2WSH(self):
            self.pubaddrtb1_P2WSH = self.instance._generate_publicaddress_bech32_P2WSH(
                Address.TestNet.BECH32_PREFIX
            )

    def __init__(self, key: Key):
        self.key = key
        self.pubkey = None
        self.pubkeyc = None
        self.mainnet = Address.MainNet(self)
        self.testnet = Address.TestNet(self)

    @staticmethod
    def of(key: Key):
        address = Address(key)
        address.generate()
        return address

    def generate(self) -> {}:
        if self.key.digest is None:
            self.key.generate()
        self.mainnet.generate_publicaddress1()
        self.mainnet.generate_publicaddress1_compressed()
        self.mainnet.generate_publicaddress3()
        self.mainnet.generate_publicaddress_bc1_P2WPKH()
        self.mainnet.generate_publicaddress_bc1_P2WSH()
        self.testnet.generate_publicaddress1()
        self.testnet.generate_publicaddress1_compressed()
        self.testnet.generate_publicaddress3()
        self.testnet.generate_publicaddress_tb1_P2WPKH()
        self.testnet.generate_publicaddress_tb1_P2WSH()

    def _generate_publicaddress1(self, prefix_a, prefix_b):
        p = self._generate_uncompressed_pubkey(prefix_b)
        m = prefix_a + hash160(p).digest()
        c = checksum(m)
        return base58.b58encode(m + c).decode("utf-8")

    def _generate_publicaddress1_compressed(self, prefix):
        p = self._generate_compressed_pubkey()
        m = prefix + hash160(p).digest()
        c = checksum(m)
        return base58.b58encode(m + c).decode("utf-8")

    def _generate_publicaddress3(self, prefix):
        prefix_redeem = b"\x00\x14"
        p = self._generate_compressed_pubkey()
        redeem_script = hash160(
            prefix_redeem + hash160(p).digest()
        ).digest()  # 20 bytes
        m = prefix + redeem_script
        c = checksum(m)
        return base58.b58encode(m + c).decode("utf-8")

    def _generate_publicaddress_bech32_P2WPKH(self, bech32_prefix):
        p = self._generate_compressed_pubkey()
        redeem_script_P2WPKH = hash160(p).digest()  # 20 bytes
        return str(
            segwit_addr.encode(
                bech32_prefix, Address.WITNESS_VERSION, redeem_script_P2WPKH
            )
        )

    def _generate_publicaddress_bech32_P2WSH(self, bech32_prefix):
        p = self._generate_compressed_pubkey()
        redeem_script_P2WSH = hashlib.sha256(p).digest()
        return str(
            segwit_addr.encode(
                bech32_prefix, Address.WITNESS_VERSION, redeem_script_P2WSH
            )
        )

    def _generate_uncompressed_pubkey(self, prefix):
        digest = self.key.digest
        ret = prefix + ecdsa_secp256k1(digest).to_string()  # 1 + 32 bytes + 32 bytes
        self.pubkey = str(binascii.hexlify(ret).decode("utf-8"))
        return ret

    def _generate_compressed_pubkey(self):
        ecdsa_digest = ecdsa_secp256k1(self.key.digest).to_string()
        x_coord = ecdsa_digest[: int(len(ecdsa_digest) / 2)]
        y_coord = ecdsa_digest[int(len(ecdsa_digest) / 2) :]
        if int(binascii.hexlify(y_coord), 16) % 2 == 0:
            p = Address.PREFIX_EVEN + x_coord
        else:
            p = Address.PREFIX_ODD + x_coord
        self.pubkeyc = str(binascii.hexlify(p).decode("utf-8"))
        return p

    def __str__(self, testnet=False):
        if testnet:
            params = (
                self.pubkey,
                self.pubkeyc,
                self.testnet.pubaddr1,
                self.testnet.pubaddr1c,
                self.testnet.pubaddr3,
                self.testnet.pubaddrtb1_P2WPKH,
                self.testnet.pubaddrtb1_P2WSH,
            )
        else:
            params = (
                self.pubkey,
                self.pubkeyc,
                self.mainnet.pubaddr1,
                self.mainnet.pubaddr1c,
                self.mainnet.pubaddr3,
                self.mainnet.pubaddrbc1_P2WPKH,
                self.mainnet.pubaddrbc1_P2WSH,
            )

        return """Public Key: %s 
                      \rPublic Key compressed: %s\n
                      \rPublic Address 1: %s   
                      \rPublic Address 1 compressed: %s   
                      \rPublic Address 3: %s  
                      \rPublic Address bc1 P2WPKH: %s    
                      \rPublic Address bc1 P2WSH: %s  
                    """ % (
            params
        )
