#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // assign key of the cipher to integer variable 'key'
    int key = atoi(argv[1]);

    // check if two command line arguments have been entered
    if (argc == 2)
    {
        // get a string from user and print the ciphered string with code that follows
        string code = get_string("plaintext: ");
        printf("ciphertext: ");

        int n = strlen(code);
        int cipher[n];

        for (int i = 0; i < n; i++)
        {
            // check if character in the plaintext is a lowercase letter
            if (islower(code[i]))
            {
                // update cipher array with transformed letter and print it
                cipher[i] = ((code[i] + key - 'a') % 26) + 97;
                printf("%c", cipher[i]);
            }
            // check if character in the plaintext is an uppercase letter
            else if (isupper(code[i]))
            {
                // update cipher array with transformed letter and print it
                cipher[i] = ((code[i] + key - 'A') % 26) + 65;
                printf("%c", cipher[i]);
            }
            // if the character is neither a lowercase or uppercase letter, print it as-is
            else
            {
                cipher[i] = code[i];
                printf("%c", cipher[i]);
            }
        }
        printf("\n");
        return 0;
    }
    // if two command line args aren't enter, print error message
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
