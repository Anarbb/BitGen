#  Bitcoin Address  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/bitcoinaddress
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.

import hashlib
import ecdsa


def sha256(v):
    return hashlib.sha256(v)


def doublehash256(v):
    return sha256(sha256(v).digest())


def hash160(v):
    return ripemd(hashlib.sha256(v).digest())


def ripemd(v):
    r = hashlib.new('ripemd160')
    r.update(v)
    return r


def ecdsa_secp256k1(digest):
    sk = ecdsa.SigningKey.from_string(digest, curve=ecdsa.SECP256k1)
    return sk.get_verifying_key()


def checksum(v):
    checksum_size = 4
    return doublehash256(v).digest()[:checksum_size]
