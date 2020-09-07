from cs50 import get_int

while True:
    x = get_int("Height: ")
    if x >= 1 and x <= 8:
        break

i = 1
j = x - 1
k = 1

while i <= x:
    print(f" " * j, end="")
    j -= 1
    print(f"#" * k, end="")
    k += 1
    print()
    i += 1







