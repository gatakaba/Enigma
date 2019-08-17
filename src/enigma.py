# coding:utf-8
import random
import string

random.seed(0)


class Enigma:
    def __init__(self, rotor_list):
        self.rotor_list = rotor_list
        # set reflector parameter
        l = list(string.ascii_lowercase)
        l[1], l[3] = l[3], l[1]
        l[0], l[5] = l[5], l[0]
        l[2], l[7] = l[7], l[2]
        l[3], l[8] = l[8], l[3]
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
            for i in range(len(self.rotor_list)):
                self.rotor_list[i].rotate(3)
                if self.rotor_list[i].is_latch:
                    print(i)
                    continue
                else:
                    break

            # Foward
            for rotor in self.rotor_list:
                s = rotor.convert(s, reverse=False)

            # Reflect
            if not is_decrypt:
                s = self.conversion_dic[s]
            else:
                s = self.reverse_conversion_dic[s]

            # Reverse
            for rotor in self.rotor_list[::-1]:
                s = rotor.convert(s, reverse=True)

            new_text += s
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
        self.is_latch = self.position > self.latch_position
        self.position = self.position % 26


if __name__ == "__main__":
    # make rotor instance
    l1 = list(string.ascii_lowercase)
    random.shuffle(l1)
    l2 = list(string.ascii_lowercase)
    random.shuffle(l2)
    r1 = Rotor(1, l1, 3)
    r2 = Rotor(3, l2, 12)
    rotor_list = [r1, r2]
    import copy

    enigma = Enigma(rotor_list)

    enigma2 = Enigma(copy.deepcopy(rotor_list))

    plain_text = "abcaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    ciphertext = enigma.encrypt(plain_text)
    print(plain_text)
    print(ciphertext)
    print(enigma2.decrypt(ciphertext))

