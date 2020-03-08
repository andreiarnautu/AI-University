user_string = input("Enter your string:\n")

#  Subpunctul a
print("Task one:")
for i in range(len(user_string)):
    print(user_string[i:] + user_string[:i])

print("\nTask two:")
for i in range(1, len(user_string)):
    print(user_string[-i:] + user_string[:-i])

for (i, j) in zip(range(0, len(user_string)), range(len(user_string) - 1, -1, -1)):
    if i >= j:
        break
    print(user_string[:i + 1] + "|" + user_string[j:])
