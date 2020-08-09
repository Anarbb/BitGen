import hashlib
import secrets
import binascii


class Bip39Gen(object):
    def __init__(self, bip39wordlist):
        self.bip39wordlist = bip39wordlist
        word_count = 12
        checksum_bit_count = word_count // 3
        total_bit_count = word_count * 11
        generated_bit_count = total_bit_count - checksum_bit_count
        entropy = self.generate_entropy(generated_bit_count)
        entropy_hash = self.get_hash(entropy)
        indices = self.pick_words(entropy, entropy_hash, checksum_bit_count)
        self.print_words(indices)



    def generate_entropy(self, generated_bit_count):
        entropy = secrets.randbits(generated_bit_count)
        return self.int_to_padded_binary(entropy, generated_bit_count)


    def get_hash(self, entropy):
        generated_bit_count = len(entropy)
        generated_char_count = generated_bit_count // 4
        entropy_hex = self.binary_to_padded_hex(entropy, generated_char_count)

        entropy_hex_no_padding = entropy_hex[2:]

        entropy_bytearray = bytearray.fromhex(entropy_hex_no_padding)

        return hashlib.sha256(entropy_bytearray).hexdigest()


    def pick_words(self, entropy, entropy_hash, checksum_bit_count):
        checksum_char_count = checksum_bit_count // 4
        bit = entropy_hash[0:checksum_char_count]

        check_bit = int(bit, 16)
        checksum = self.int_to_padded_binary(check_bit, checksum_bit_count)

        source = str(entropy) + str(checksum)
        return [int(str('0b') + source[i:i + 11], 2) for i in range(0, len(source), 11)]


    def print_words(self, indices):
        words = [self.bip39wordlist[indices[i]] for i in range(len(indices))]
        word_string = ' '.join(words)
        self.mnemonic = word_string


    def int_to_padded_binary(self, num, padding):
        return bin(num)[2:].zfill(padding)


    def binary_to_padded_hex(self, bin, padding):
        num = int(bin, 2)
        return '0x{0:0{1}x}'.format(num, padding)
