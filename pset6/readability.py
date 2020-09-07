from cs50 import get_string
from sys import argv, exit


s = get_string("Text: ");


n = len(s);
space = 1;
letter = 0;
punct = 0;

for i in range(n):

    if s[i].isalnum()==True:
        letter += 1

    if s[i].isspace()==True:
        space += 1

    if s[i]=="?" or s[i]=="." or s[i]=="!":
        punct += 1

    i += 1


#calculate L and S
L = 100 * (letter / space);
S = (punct / space) * 100


readability = round(.0588 * L - 0.296 * S - 15.8)

if readability >= 16:
    print(f"Grade 16+")

elif readability < 1:
    print(f"Before Grade 1")

else:
    print(f"Grade", readability)
