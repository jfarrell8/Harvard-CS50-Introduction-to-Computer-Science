#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Vigenere: Ask for a plaintext input and a keyword. Cipher the text using the keyword.

int main(int argc, string argv[])
{
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
                // update the character in the plaintext using the corresponding letter in the keyword
                cipher[i] = ((code[i] + argv[1][i % (n-1)] - 'a') % 26) + 'a';
                printf("%c", cipher[i]);
            }
            // check if character in the plaintext is an uppercase letter
            else if (isupper(code[i]))
            {
                // update the character in the plaintext using the corresponding letter in the keyword
                cipher[i] = ((code[i] + argv[1][i % (n-1)] - 'A') % 26) + 'A';
                printf("%c", cipher[i]);
            }
            // if character is not an upper- or lowercase letter, print as-is
            else
            {
                cipher[i] = code[i];
                printf("%c", cipher[i]);
            }
        }
        printf("\n");
        return 0;
    }
    // if two args aren't entered, print error message
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}