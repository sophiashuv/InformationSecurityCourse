import numpy as np


def read_txt(file_name):
    with open(file_name) as f:
        lines = f.read().rstrip()
    return lines


def write_txt(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)


class LinearShiftCipher():

    def __init__(self, massage, s=None):
        self.massage = massage
        self.l = 8
        self.f = lambda s: str(int(s[self.l - 8]) ^ int(s[self.l - 4]) ^ int(s[self.l - 3]) ^ int(s[self.l - 2]) ^ 1)
        if not s:
            self.s = self.generate_state(self.l)
        else:
            self.s = s

    @staticmethod
    def generate_state(l):
        return "".join([str(i) for i in np.random.randint(2, size=l)])

    def getCipherText(self):
        res = ""
        for letter in self.massage:
            letter_bin = bin(ord(letter))[2:]

            res_b = ''
            letter_bin = "0" * (8 - len(letter_bin)) + letter_bin
            for b in letter_bin:
                s = int(self.s[-1])
                new_b = s ^ int(b)
                res_b += str(new_b)
                self.s = str(self.f(self.s)) + self.s[:-1]
            res_b = "0" * (8 - len(res_b)) + res_b
            res += chr(int(res_b, base=2))
        return res

    def getOriginalText(self):
        return self.getCipherText()


if __name__ == "__main__":
    text_file = "../text.txt"

    message = read_txt(text_file)

    s = LinearShiftCipher.generate_state(8)
    print("message: ")
    print(message)
    print("Initial register stage: ")
    print(s)
    # Encryption
    ss = LinearShiftCipher(message, s)
    res = ss.getCipherText()
    print("------------------------------------------------------")
    print("Encrypted text: ")
    print(res)

    # Decryption
    print("------------------------------------------------------")
    ss = LinearShiftCipher(res, s)
    res = ss.getOriginalText()
    print("Decrypted text: ")
    print(res)
