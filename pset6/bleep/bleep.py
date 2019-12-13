from cs50 import get_string
from sys import argv


def main():

    if len(argv) != 2:
        sys.exit("Usage: python bleep.py dictionary")

    # creates a "set" of words from argv[1]
    words = set()
    file = open(argv[1], "r")
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()


    message = get_string("What message would you like to censor? ")
    tokens = message.split() # creates a list called "tokens" and tokenizes (splits) the message into a list of the individual words

    for word in tokens:
        if word.lower() in words:
           for s in word:
               print("*", end="")
           print(" ", end="")
        else:
            print(f"{word} ", end="")

    print()

if __name__ == "__main__":
    main()
