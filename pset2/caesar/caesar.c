#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <math.h>

bool check_valid_key(string s);

//check to see if usage is correct
int main(int argc, string argv[])
{
    //ask for key
    if (argc != 2 || !check_valid_key(argv[1]))
    {
        printf("Usage: ./caesar key");
        printf("\n");
        return 1;
    }
    //convert to number
    int key = atoi(argv[1]);
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    int n = strlen(plaintext);
    for (int i = 0;  i < n; i++)
    {

        char c = plaintext[i];
        if (isalpha(c))

        {

            char m = 'A';
            if (islower(c))

            {

                m = 'a';

            }

            printf("%c", (c - m + key) % 26 + m);

        }
        else
        {
            printf("%c", c);
        }
    }

    printf("\n");
}

bool check_valid_key(string s)
{

    for (int i = 0, len = strlen(s); i < len; i++)
        if (!isdigit(s[i]))
        {

        return false;

       }


    return true;
}