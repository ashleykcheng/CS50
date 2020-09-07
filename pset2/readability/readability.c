#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int main(void)
{

    //index = 0.0588 * L - 0.296 * S - 15.8

    string s = get_string("Text: ");

    //average numbers of letters per 100 words: L
    int n = strlen(s);
    int space = 1;
    int letter = 0;
    int punct = 0;

    for (int i = 0; i < n; i++)
    {

        //number of letters
        if ((s[i] >= 'a' && s[i] <= 'z') || (s[i] >= 'A' && s[i] <= 'Z'))
        {
            letter = letter + 1;
        }

        //number of words
        else if (isspace(s[i]))
        {
            space = space + 1;
        }

        else if ((s[i]) == '!' || s[i] == '.' || s[i] == '?')
        {
            punct = punct + 1;

        }
    }



    //calculate L
    float L = 100 * ((float) letter / (float) space);



    //average number of sentences per 100 words in the text: S
    float S = ((float) punct / (float) space) * 100;

    printf("%i\n", letter);
    printf("%i\n", space);
    printf("%i\n", punct);
    printf("%f\n", L);
    printf("%f", S);
    

    //calculate readability
    int readability = round(.0588 * L - 0.296 * S - 15.8);

    if (readability >= 16)
    {

        printf("Grade 16+\n");
    }
    else if (readability < 1)
    {

        printf("Before Grade 1\n");
    }
    else
    {

        printf("Grade %i\n", readability);
    }
}

