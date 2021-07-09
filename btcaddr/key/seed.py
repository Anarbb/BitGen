#  Bitcoin Address  v0.1
#  Copyright (c) 2020 - https://github.com/fortesp/bitcoinaddress
#  This software is distributed under the terms of the MIT License.
#  See the file 'LICENSE' in the root directory of the present distribution,
#  or http://opensource.org/licenses/MIT.

import time
import os
from random import randrange


class Seed:

    def __init__(self, entropy=None):
        self.entropy = entropy
        if self.entropy is None:
            self.generate()

    def generate(self):
        self.entropy = Seed.random()

    @staticmethod
    def of(entropy=None):
        return Seed(entropy)

    @staticmethod
    def random():
        # from bitcoin project
        return str(os.urandom(32).hex()) \
               + str(randrange(2 ** 256)) \
               + str(int(time.time() * 1000000))

    def __str__(self):
        return self.entropy
