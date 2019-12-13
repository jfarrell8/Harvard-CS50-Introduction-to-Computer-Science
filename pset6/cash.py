from cs50 import get_float

# ask how much change is owed, then print min # of coins with which change can be made
def main():
    owed = get_positive_float("Change owed: ");
    cents = round(owed * 100);

    counter = 0

    while cents >= 25:

        counter = counter + 1
        cents = cents - 25
        if cents < 25:
            break


    while cents >= 10:

        counter = counter + 1
        cents = cents - 10
        if cents < 10:
            break


    while cents >= 5:

        counter = counter + 1
        cents = cents - 5
        if cents < 5:
            break

    while cents > 0:

        counter = counter + 1
        cents = cents - 1



    print(f"{counter}")


def get_positive_float(prompt):

    while True:
        n = get_float(prompt)
        if n > 0:
            return n

if __name__ == "__main__":
    main()
