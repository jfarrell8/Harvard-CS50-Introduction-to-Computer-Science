from cs50 import get_int

def main():

    n = get_1_to_8_int("Enter an integer between 1 and 8: ");

    for i in range(n):
        for k in range(n - i, 1, -1):
            print(" ", end="")

        for j in range(i + 1):
            print("#", end="")
        print()


# get integer from 1 to 8
def get_1_to_8_int (prompt):

    while True:
        n = get_int(prompt)
        if n >= 1 and n <= 8:
            return n

if __name__ == "__main__":
    main()