import random
random_number = random.randint(0, 100)

x = 8
for i in range(x):
    user_guess = int(input("Guess:\n"))
    if user_guess == random_number:
        print("Correct!")
        break
    elif user_guess < random_number:
        print("The random number is bigger.")
    else:
        print("The random number is smaller.")

