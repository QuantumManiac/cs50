string = "hello"
substring = []
n = 3
for i in range(len(string) - n + 1):
    substring.append(string[i:n + i])
print(substring)
