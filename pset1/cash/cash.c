#include <cs50.h>
#include <stdio.h>
#include <math.h>

int coins = 0;
int main (void)

{
    //ask for change
    float dollar = get_float("Change owed:");
    while (dollar < 0)
    {
        dollar = get_float("Change owed:");
    }

int change = round(dollar * 100);


    //while loops
while (change > 0)
{
        if (change >= 25)
        {
            change = change - 25;
            coins = coins + 1;

        } 
        
        else if (change >= 10)
        {
            change = change-10;
            coins = coins + 1;
        } 
        else if (change >= 5)
        
        {
            change = change-5;
            coins = coins + 1;
        } 
        else if (change >= 1)
        
        {
            change = change - 1;
            coins = coins + 1;
        }
    
}
    printf("%i\n", coins);
}
