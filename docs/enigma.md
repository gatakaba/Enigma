# Enigma

```plantuml
class Enigma{
    + Enigma(Rotor rotor_list,PlugBoard)
    + str encrypt(str plaintext)
    + str decrypt(str ciphertext)
    - list<Rotor> rotor_list
    - str encrypt_single_char(str s)
    - str decrypt_single_char(str s)
}

class PlugBoard{
    + PlugBoard()
}
class Rotor{
    + Rotor(list conversion_table,int initial_position)
    + str convert(str s)
    + void shift(int n)
    + bool is_latch
}

Enigma o-- Rotor
Enigma o-- PlugBoard
```
