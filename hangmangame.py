import random

w = ["bag", "colleges", "student", "board"]
l = random.choice(w)
display = ["_" for _ in l]
attempts = 6
wrongguess = 0
usedletter = []

while "_" in display and wrongguess < attempts:
    print(" ".join(display))
    a = input("Guess the letter: ").lower()

    if a in usedletter:
        print("You already guessed this letter.")
    elif a in l:
        for index, letter in enumerate(l):
            if letter == a:
                display[index] = a
        print(" ".join(display))
    else:
        wrongguess += 1
        print(f"Letter not in the word. You have {attempts - wrongguess} attempts left.")
    
    usedletter.append(a)

if wrongguess == attempts:
    print(f"You have run out of guesses. The word was '{l}'.")
else:
    print("Congratulations! You have guessed the word.")
