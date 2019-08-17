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

        r1 = Rotor(0, l1, 3)
        r2 = Rotor(4, l2, 3)
        self.rotor_list = [r1, r2]

    def encrypt(self, plaintext: str) -> str:
        ciptext = ""
        for s in plaintext:
            # Rotate Rotor
            self.rotor_list[0].shift()
            if self.rotor_list[0].is_latch:
                self.rotor_list[1].shift()

            # Foward
            z = self.rotor_list[0].convert(s)
            z = self.rotor_list[1].convert(z)
            # Reverse
            z = self.rotor_list[1].convert(z)
            z = self.rotor_list[0].convert(z)
            ciptext += z
        return ciptext


class Rotor:
    def __init__(
        self, initial_position: int, conversion_list: list, latch_position: int
    ):
        self.conversion_list = conversion_list
        self.latch_position = latch_position
        self.position = initial_position

    def convert(self, s: str) -> str:
        index = ord(s) - 97
        return self.conversion_list[index]

    def shift(self, n=1):
        self.position += n
        self.conversion_list = self.conversion_list[n:] + self.conversion_list[:n]

    @property
    def is_latch(self) -> bool:
        return self.position == self.latch_position


if __name__ == "__main__":
    enigma = Enigma()
    print(enigma.encrypt("aaaaaaaaaaa"))
