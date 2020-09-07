from cs50 import get_float

coins = 0;

dollar = get_float("Change owed: ");
while (dollar < 0):
    dollar = get_float("Change owed: ");

change = (dollar * 100);

while (change > 0):
    if (change >= 25):
        change = change - 25;
        coins = coins + 1;
    elif (change >= 10):
        change = change-10;
        coins = coins + 1;
    elif (change >= 5):
        change = change-5;
        coins = coins + 1;
    elif (change >= 1):
        change = change - 1;
        coins = coins + 1;

print(coins)
