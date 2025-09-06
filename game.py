import random

count = 0

print("Welcome to the Number Guessing Game.\n")

a = int(input("enter the start point of the range of guess"))
b = int(input("enter the end point of guessing the number "))
right_number = random.randint(a, b)

print("I've picked a number for you to guess.")
print("The number is between", a, "and ", b, "\n")

guessed_number = int(input("Guess a number:"))


while guessed_number != right_number:
    count = count+1
    if guessed_number < 1 or guessed_number > 5:
        print("Invalid guess. Please enter a number between 1 and 5.")

    elif guessed_number > right_number:
        print("\nYour guess is not correct.")
        print("Give it another shot.")
        print("Choose a lower number.\n")
    else:
        print("\nYour guess is not correct.")
        print("Give it another shot.")
        print("Choose a higher number.\n")

    guessed_number = int(input("Enter guess number again:\n "))


print("\nCorrect guess.")
print("You won. Thank you for playing.")
print("you count score is ", count)
