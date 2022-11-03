import string
import numpy as np


def read_txt(file_name):
    with open(file_name) as f:
        lines = f.read().rstrip()
    return lines


def write_txt(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)


class ShacalCipher():
    """
    Class for Shacal-1 cypher representation.
    """
    RAUNDS_NUM = 80

    def __init__(self, massage, keyword=None):
        self.massage = massage
        if not keyword:
            self.key, self.keyword = self.generate_random_key()
        else:
            self.keyword = keyword
            self.key = ShacalCipher.word_to_binary(keyword)

        self.fill_key()
        self.FUNCTIONS_DICT = {}
        self.CONSTANTS_DICT = {}
        for i in range(0, 20):
            self.FUNCTIONS_DICT[i] = lambda x, y, z: (x & y) | ((x ^ (2**32-1)) & z)
            self.CONSTANTS_DICT[i] = '5A827999'
        for i in range(20, 40):
            self.FUNCTIONS_DICT[i] = lambda x, y, z: (x ^ y ^ z)
            self.CONSTANTS_DICT[i] = '6ED9EBA1'
        for i in range(40, 60):
            self.FUNCTIONS_DICT[i] = lambda x, y, z: (x & y) | (x & z) | (y & z)
            self.CONSTANTS_DICT[i] = '8F1BBCDC'
        for i in range(60, 80):
            self.FUNCTIONS_DICT[i] = lambda x, y, z: (x ^ y ^ z)
            self.CONSTANTS_DICT[i] = 'CA62C1D6'

    def fill_key(self):
        self.key = np.array(self.key)
        self.key = np.reshape(self.key, (-1, 4))
        self.key = [self.block_to_uint32(k) for k in self.key]
        for i in range(64):
            self.key.append(ISHFTC(self.key[i + 16 - 3] ^
                                   self.key[i + 16 - 8] ^
                                   self.key[i + 16 - 14] ^
                                   self.key[i + 16 - 16], 1, 32))

    def getKey(self):
        return self.key

    @staticmethod
    def shift(seq, n):
        n = n % len(seq)
        return seq[n:] + seq[:n]

    @staticmethod
    def word_to_binary(word):
        b = [ord(x) for x in word]
        return b

    @staticmethod
    def blocks_to_words(blocks):
        return "".join(chr(b) for b in blocks)

    @staticmethod
    def bin_to_word(b):
        binary = bin(b)
        return binary

    @staticmethod
    def generate_random_key():
        res = []
        keyword = ""
        for i in range(16):
            key = np.random.randint(255, size=4)
            keyword += "".join(chr(k) for k in key)
            res.append(key)
        return res, keyword

    @staticmethod
    def hex_to_binary(heximal):
        return int(heximal, base=16)

    @staticmethod
    def block_to_uint32(block):
        return int('{0:08b}'.format(block[3]) +
                   '{0:08b}'.format(block[2]) +
                   '{0:08b}'.format(block[1]) +
                   '{0:08b}'.format(block[0]), 2)

    @staticmethod
    def uint34_to_block(uint):
        b = bin(uint)[2:]
        b = "0" * (32 - len(b)) + b
        return [int(b[24:], 2), int(b[16:24], 2), int(b[8:16], 2), int(b[:8], 2)]

    def getCipherText(self):

        A_temp = ShacalCipher.word_to_binary(self.massage[:4])
        B_temp = ShacalCipher.word_to_binary(self.massage[4:8])
        C_temp = ShacalCipher.word_to_binary(self.massage[8:12])
        D_temp = ShacalCipher.word_to_binary(self.massage[12:16])
        E_temp = ShacalCipher.word_to_binary(self.massage[16:20])

        A_temp = self.block_to_uint32(A_temp)
        B_temp = self.block_to_uint32(B_temp)
        C_temp = self.block_to_uint32(C_temp)
        D_temp = self.block_to_uint32(D_temp)
        E_temp = self.block_to_uint32(E_temp)

        for i in range(self.RAUNDS_NUM):

            K = self.key[i]
            f = self.FUNCTIONS_DICT[i]

            A = ((K + ISHFTC(A_temp, 5, 32)) +
                 f(B_temp, C_temp, D_temp) +
                 E_temp +
                 self.hex_to_binary(self.CONSTANTS_DICT[i])) % 2**32

            B = A_temp
            C = ISHFTC(B_temp, 30, 32)
            D = C_temp
            E = D_temp

            A_temp = A
            B_temp = B
            C_temp = C
            D_temp = D
            E_temp = E

        res = [*self.uint34_to_block(A_temp),
               *self.uint34_to_block(B_temp),
               *self.uint34_to_block(C_temp),
               *self.uint34_to_block(D_temp),
               *self.uint34_to_block(E_temp)]

        return self.blocks_to_words(res), res

    def getOriginalText(self):
        A_temp = ShacalCipher.word_to_binary(self.massage[:4])
        B_temp = ShacalCipher.word_to_binary(self.massage[4:8])
        C_temp = ShacalCipher.word_to_binary(self.massage[8:12])
        D_temp = ShacalCipher.word_to_binary(self.massage[12:16])
        E_temp = ShacalCipher.word_to_binary(self.massage[16:20])

        A_temp = self.block_to_uint32(A_temp)
        B_temp = self.block_to_uint32(B_temp)
        C_temp = self.block_to_uint32(C_temp)
        D_temp = self.block_to_uint32(D_temp)
        E_temp = self.block_to_uint32(E_temp)

        for i in range(self.RAUNDS_NUM):

            K = self.key[79 - i]
            f = self.FUNCTIONS_DICT[79 - i]

            A = B_temp
            B = ISHFTC(C_temp, 2, 32)
            C = D_temp
            D = E_temp
            E = ((K ^ (2**32-1)) + (ISHFTC(B_temp, 5, 32) ^ (2**32-1)) +
                 (f(ISHFTC(C_temp, 2, 32), D_temp, E_temp) ^ (2**32-1)) +
                 A_temp + (self.hex_to_binary(self.CONSTANTS_DICT[79 - i]) ^ (2**32 - 1)) + 4) % (2 ** 32)

            A_temp = A
            B_temp = B
            C_temp = C
            D_temp = D
            E_temp = E

        res = [*self.uint34_to_block(A_temp),
               *self.uint34_to_block(B_temp),
               *self.uint34_to_block(C_temp),
               *self.uint34_to_block(D_temp),
               *self.uint34_to_block(E_temp)]

        return self.blocks_to_words(res), res


def ISHFTC(n, d, N):
    return ((n << d) % (1 << N)) | (n >> (N - d))


def encryption(message, keyword):
    message = message + "0" * (len(message) % 20)
    messages = [message[i * 20:(i + 1) * 20] for i in range(len(message) // 20)]
    s = ""
    for m in messages:
        sc = ShacalCipher(m, keyword)
        text, res = sc.getCipherText()
        s += text
    return s


def decryption(s, keyword):
    textes = [s[i * 20:(i + 1) * 20] for i in range(len(s) // 20)]
    ds = ""
    for m in textes:
        sc = ShacalCipher(m, keyword)
        text, res = sc.getOriginalText()
        ds += text
    return ds


if __name__ == "__main__":
    text_file = "../text.txt"

    message = read_txt(text_file)
    key, keyword = ShacalCipher.generate_random_key()
    print("message: ")
    print(message)
    print("key: ")
    print(keyword)

    # Encryption
    s = encryption(message, keyword)
    print("------------------------------------------------------")
    print("Encrypted text: ")
    print(s)

    # Decryption
    print("------------------------------------------------------")
    ds = decryption(s, keyword)
    print("Decrypted text: ")
    print(ds)


