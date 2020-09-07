#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        //ask for height
        height = get_int("Height: "); 
    }
    while (height < 1 || height > 8);
    for (int i = 1; i <= height; i++)
    {
        //print spaces
        for (int j = height - i; j > 0; j--)
        {
            printf(" ");
        }
        //print #
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        // New row
        printf("\n");
    }
}

