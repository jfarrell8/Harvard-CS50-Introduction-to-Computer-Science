from cs50 import get_string
from sys import argv

def main():

    if len(argv) != 2:
        sys.exit("Usage: python caesar.py key")


    key = int(argv[1])
    code = get_string("plaintext: ")
    print("ciphertext: ", end="")

    for c in code:

        if c.islower():

            c_cipher = ((ord(c) + key - ord('a')) % 26) + 97
            print(f"{chr(c_cipher)}", end="")

        elif c.isupper():

            c_cipher = ((ord(c) + key - ord('A')) % 26) + 65
            print(f"{chr(c_cipher)}", end="")

        else:

            if (ord(c) >= 65 and ord(c) <= 90) or (ord(c) >= 97 and ord(c) <= 122):
                print(f"{chr(c)}", end="")
            else:
                print(c, end="")

    print()
    return 0

if __name__ == "__main__":
    main()