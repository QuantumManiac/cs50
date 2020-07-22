# Makes stairs like the one at the end of World 1-1 in Super Mario Bros.

from cs50 import get_int

while True:
    h = get_int("Height:")
    if h >= 0 and h <= 23:
        break

for i in range(h):

    for j in range(h - i - 1):
        print(" ", end="")

    for k in range(i + 2):
        print("#", end="")

    print("")