#include <cs50.h>
#include <stdio.h>
#include <math.h>

float get_positive_float(string prompt);

//ask how much change is owed, then print min # of coins with which change can be made

int main(void)
{
    //call function to get positive amount of change owed, multiply by 100 and assing to 'cents'
    float owed = get_positive_float("Change owed: ");
    int cents = round(owed * 100);

    int counter = 0;

    // account for quarters: whittle dollars to cents 25 or less; updating counter and cents along the way
    while (cents >= 25)
    {
        counter++;
        cents = cents - 25;
        if (cents < 25)
        {
            break;
        }
    }

    // account for dimes
    while (cents >= 10)
    {
        counter++;
        cents = cents - 10;
        if (cents < 10)
        {
            break;
        }

    }

    // account for nickels
    while (cents >= 5)
    {
        counter++;
        cents = cents - 5;
        if (cents < 5)
        {
            break;
        }
    }

    // account for pennies
    while (cents > 0)
    {
        counter++;
        cents = cents - 1;
    }

    printf("%i\n", counter);
}

// function to get positive float value to represent dollars and/or cents of change owed
float get_positive_float(string prompt)
    {
        float n;
        do
        {
            n = get_float("%s", prompt);
        }
        while (n < 0);
        return n;
    }
