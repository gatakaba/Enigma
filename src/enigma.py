# coding:utf-8
import random
import string

random.seed(0)


class Enigma:
    def __init__(self, rotor_list):
        self.rotor_list = rotor_list
        # set reflector parameter
        l = list(string.ascii_lowercase)
        l[8], l[7] = l[7], l[8]
        l[4], l[24] = l[24], l[4]
        l[12], l[2] = l[2], l[12]
        l[21], l[11] = l[11], l[21]
        l[18], l[6] = l[6], l[18]
        l[15], l[3] = l[3], l[15]

        self.conversion_dic = dict()

        for i, x in enumerate(l):
            self.conversion_dic[string.ascii_lowercase[i]] = x
        self.reverse_conversion_dic = {v: k for k, v in self.conversion_dic.items()}

    def encrypt(self, plaintext):
        return self.reflect(plaintext, False)

    def decrypt(self, ciptext):
        return self.reflect(ciptext, True)

    def reflect(self, plaintext: str, is_decrypt=False) -> str:
        new_text = ""
        for s in plaintext:
            # Rotate Rotor
            self.rotor_list[0].rotate()
            if self.rotor_list[0].is_latch:
                self.rotor_list[1].rotate()

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

            new_text += z
        return new_text


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

    def rotate(self, n=1):
        self.position += n

    @property
    def is_latch(self) -> bool:
        return self.position == self.latch_position


if __name__ == "__main__":
    # make rotor instance
    l1 = list(string.ascii_lowercase)
    random.shuffle(l1)
    l2 = list(string.ascii_lowercase)
    random.shuffle(l2)
    r1 = Rotor(1, l1, 3)
    r2 = Rotor(3, l2, 3)
    rotor_list = [r1, r2]

    enigma = Enigma(rotor_list)
    import copy

    enigma_copy = copy.deepcopy(enigma)
    plain_text = "abcaaaaaaaa"

    ciphertext = enigma.encrypt(plain_text)
    print(plain_text)
    print(ciphertext)
    print(enigma_copy.decrypt(ciphertext))

