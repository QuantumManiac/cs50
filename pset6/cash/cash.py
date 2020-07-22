# Takes cash value and gives minimum number of coins to get amount
from cs50 import get_float

while True:
    n = get_float("Change owed: ") * 100
    if n >= 0:
        break

o = 0

while n - 25 >= 0:
    n -= 25
    o += 1

while n - 10 >= 0:
    n -= 10
    o += 1

while n - 5 >= 0:
    n -= 5
    o += 1

while n - 1 >= 0:
    n -= 1
    o += 1

print(o)