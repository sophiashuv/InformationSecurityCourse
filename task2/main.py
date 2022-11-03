import string


def read_txt(file_name):
    with open(file_name) as f:
        lines = f.read().rstrip()
    return lines


def write_txt(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)


class CipherImplementation:
    """
    Base class for Cipher representation.
    """

    all_alphabets = list(string.ascii_uppercase)

    def __init__(self, message, keyword):
        self.message = message
        self.keyword = keyword

    @staticmethod
    def removeDuplicates(lst):
        without_duplicates = []
        for ch in lst:
            if ch in CipherImplementation.all_alphabets and ch not in without_duplicates:
                without_duplicates.append(ch)
        return without_duplicates

    @staticmethod
    def shift(seq, n):
        n = n % len(seq)
        return seq[n:] + seq[:n]


class KeywordCipher(CipherImplementation):
    """
    Class for Cesar Cipher representation.
    """

    def __init__(self, message, keyword, key):
        super().__init__(message, CipherImplementation.removeDuplicates(keyword.upper()))
        self.key = key
        encrypting = self.removeDuplicates(self.keyword + self.all_alphabets)
        self.encrypting = self.shift(encrypting, self.key)

    def getCipherText(self):
        ciphertext = ""
        for i in range(len(self.message)):
            if self.message[i].upper() in self.all_alphabets:
                ch = self.encrypting[self.all_alphabets.index(self.message[i].upper())]
                if self.message[i].islower():
                    ch = ch.lower()
                ciphertext = ciphertext + ch
            else:
                ciphertext = ciphertext + self.message[i]
        return ciphertext

    def getOriginalText(self):
        text = ""
        for i in range(len(self.message)):
            if self.message[i].upper() in self.all_alphabets:
                ch = self.all_alphabets[self.encrypting.index(self.message[i].upper())]
                if self.message[i].islower():
                    ch = ch.lower()
                text += ch
            else:
                text += self.message[i]
        return text


class VigenereCipher(CipherImplementation):
    """
    Class for Vigenere Cipher representation.
    """

    def __init__(self, message, keyword):
        super().__init__(message, keyword.upper())
        self.key = self.generateKey(message, self.keyword)

    @staticmethod
    def generateKey(message, keyword):
        res = ""
        k = 0
        for i, ch in enumerate(message):
            if ch.upper() not in CipherImplementation.all_alphabets:
                res += ch
                k += 1
            else:
                res += keyword[(i - k) % len(keyword)]
        return res

    def getCipherText(self):
        cipher_text = ""
        for i, letter in enumerate(self.message):
            if letter.upper() in self.all_alphabets:
                x = (ord(letter.upper()) + ord(self.key[i])) % 26
                x += ord('A')
                ch = chr(x)
                if letter.islower():
                    ch = ch.lower()
                cipher_text += ch
            else:
                cipher_text += letter
        return cipher_text

    def getOriginalText(self):
        orig_text = ""
        for i, letter in enumerate(self.message):
            if letter.upper() in self.all_alphabets:
                x = (ord(letter.upper()) - ord(self.key[i]) + 26) % 26
                x += ord('A')
                ch = chr(x)
                if letter.islower():
                    ch = ch.lower()
                orig_text += ch
            else:
                orig_text += letter
        return orig_text


if __name__ == "__main__":
    text_file = "../text.txt"
    cipher_file = "../cipher.txt"

    task = input("Enter 1 to use Keyword Caesar Cipher, and 2 for Vigenere Cipher: ")
    task1 = input("Enter 1 encrypt, and 2 decrypt: ")
    keyword = input("Enter keyword: ")

    if task == "1":
        key = int(input("Enter key: "))
        if task1 == "1":
            message = read_txt(text_file)
            kc = KeywordCipher(message, keyword, key)
            write_txt(cipher_file, kc.getCipherText())
        elif task1 == "2":
            message = read_txt(cipher_file)
            kc = KeywordCipher(message, keyword, key)
            print("Decrypted text: ")
            print(kc.getOriginalText())
        else:
            print("You entered wrong command.")

    elif task == "2":
        if task1 == "1":
            message = read_txt(text_file)
            vc = VigenereCipher(message, keyword)
            write_txt(cipher_file, vc.getCipherText())
        elif task == "2":
            message = read_txt(cipher_file)
            vc = VigenereCipher(message, keyword)
            print("Decrypted text: ")
            print(vc.getOriginalText())
        else:
            print("You entered wrong command.")
    else:
        print("You entered wrong command.")
