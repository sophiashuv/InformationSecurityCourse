import random
import math


def read_txt(file_name):
    with open(file_name) as f:
        lines = f.read().rstrip()
    return lines


def write_txt(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)


class StreamCipherBBS():

    def __init__(self, massage, integers=None):
        self.massage = massage
        if not integers:
            self.p, self.q, self.r, self.n = self.generate_random_integers()
        else:
            self.p, self.q, self.r = integers
            self.n = self.p * self.q

    @staticmethod
    def generate_random_integers():
        p = random.randrange(3, 1000, 4)
        q = random.randrange(3, 1000, 4)
        n = p * q
        r = random.randint(1, 1000)
        while math.gcd(r, n) != 1:
            r = random.randint(1, 1000)
        return p, q, r, n

    def getCipherText(self):
        res = ""
        x = (self.r ** 2) % self.n
        for letter in self.massage:
            letter_bin = bin(ord(letter))[2:]

            res_b = ''
            letter_bin = "0" * (8 - len(letter_bin)) + letter_bin
            for b in letter_bin:
                s = x % 2
                x = (x ** 2) % self.n
                new_b = s ^ int(b)
                res_b += str(new_b)
            res_b = "0" * (8 - len(res_b)) + res_b
            res += chr(int(res_b, base=2))
        return res

    def getOriginalText(self):
        return self.getCipherText()


if __name__ == "__main__":
    text_file = "../text.txt"

    message = read_txt(text_file)

    p, q, r, n = StreamCipherBBS.generate_random_integers()
    print("message: ")
    print(message)
    print("p, q, r, n: ")
    print(p, q, r, n)
    # Encryption
    s = StreamCipherBBS(message, (p, q, r))
    res = s.getCipherText()
    print("------------------------------------------------------")
    print("Encrypted text: ")
    print(res)

    # Decryption
    print("------------------------------------------------------")
    s = StreamCipherBBS(res, (p, q, r))
    res = s.getOriginalText()
    print("Decrypted text: ")
    print(res)
