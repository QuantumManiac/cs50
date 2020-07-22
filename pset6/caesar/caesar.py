# Program that encrypts messages using "Caesar's Cipher"
import sys
from cs50 import get_string


def main():
    if len(sys.argv) != 2 or int(sys.argv[1]) < 0:
        print("usage caesar.py k")
        sys.exit(1)
    else:
        key = int(sys.argv[1])
        plaintext = get_string("plaintext: ")
        cipher = []

    for c in plaintext:
        if c.isalpha():
            if c.isupper():
                cipher.append(chr(((ord(c) - ord('A') + key) % 26) + ord('A')))
            else:
                cipher.append(chr(((ord(c) - ord('a') + key) % 26) + ord('a')))
        else:
            cipher.append(c)
    print("ciphertext: " + ''.join(cipher))
    sys.exit(0)


if __name__ == "__main__":
    main()
