#include <cs50.h>
#include <stdio.h>

int get_1_to_8_int (string prompt);

int main(void)
{
    int n = get_1_to_8_int("Enter an integer between 1 and 8: ");
    
    for (int i = 0; i < n; i++) 
    {      
        // prints required spaces before #
        for (int k = n - i; k > 1; k--)
        {
            printf(" ");
        }
        
        // prints #s, spaces, then #s again
        for (int j = 0; j <= i; j++)
        {                                
            printf("#");
        }
        
        printf("  ");
        
        for (int ending = 0; ending <= i; ending++)
        {
            printf("#");
        }
        
        printf("\n");
    }  
}

// get integer from 1 to 8
int get_1_to_8_int (string prompt) 
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n < 1 || n > 8);
    return n;
}

