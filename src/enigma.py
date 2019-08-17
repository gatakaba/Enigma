# coding:utf-8
import random
import string

random.seed(0)


class Enigma:
    def __init__(self):
        l1 = list(string.ascii_lowercase)
        random.shuffle(l1)

        l2 = list(string.ascii_lowercase)
        random.shuffle(l2)

        r1 = Rotor(1, l1, 3)
        r2 = Rotor(3, l2, 3)
        self.rotor_list = [r1, r2]

        l = list(string.ascii_lowercase)
        random.shuffle(l)
        self.conversion_dic = dict()

        for i, x in enumerate(l):
            self.conversion_dic[string.ascii_lowercase[i]] = x
        self.reverse_conversion_dic = {v: k for k, v in self.conversion_dic.items()}

    def encrypt(self, plaintext):
        return self.reflect(plaintext, False)

    def decrypt(self, ciptext):
        return self.reflect(ciptext, True)

    def reflect(self, plaintext: str, is_decrypt=False) -> str:
        ciptext = ""
        for s in plaintext:
            # Rotate Rotor
            self.rotor_list[0].shift()
            if self.rotor_list[0].is_latch:
                self.rotor_list[1].shift()

            # Foward
            z = self.rotor_list[0].convert(s, reverse=False)
            z = self.rotor_list[1].convert(z, reverse=False)
            # Reflect
            if is_decrypt:
                z = self.conversion_dic[z]
            else:
                z = self.reverse_conversion_dic[z]

            # Reverse
            z = self.rotor_list[1].convert(z, reverse=True)
            z = self.rotor_list[0].convert(z, reverse=True)

            ciptext += z
        return ciptext


class Rotor:
    def __init__(
        self, initial_position: int, conversion_list: list, latch_position: int
    ):
        self.position = initial_position
        self.latch_position = latch_position
        self.conversion_list = conversion_list

    def convert(self, s: str, reverse=False) -> str:
        def shift(seq, n):
            return seq[n:] + seq[:n]

        l = shift(self.conversion_list, self.position)

        conversion_dic = dict()
        for i, x in enumerate(l):
            conversion_dic[string.ascii_lowercase[i]] = x
        reverse_conversion_dic = {v: k for k, v in conversion_dic.items()}

        if not reverse:
            return conversion_dic[s]

        else:
            return reverse_conversion_dic[s]

    def shift(self, n=1):
        self.position += n

    @property
    def is_latch(self) -> bool:
        return self.position == self.latch_position


if __name__ == "__main__":
    enigma = Enigma()
    import copy

    enigma_copy = copy.deepcopy(enigma)
    plain_text = "abc"

    ciphertext = enigma.encrypt(plain_text)
    print(plain_text)
    print(ciphertext)
    print(enigma_copy.decrypt(ciphertext))

