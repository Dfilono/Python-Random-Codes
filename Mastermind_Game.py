import random


# Constants
COLORS = ["R", "G", "B", "Y", "W", "O"]
TRIES = 10
CODE_LENGTH = 4

# Generate random code
def generate_code():
    code = []

    for i in range(CODE_LENGTH):
        color = random.choice(COLORS)
        code.append(color)

    return code

# Guess the code
def guess_code():
    while True:
        guess = input("Guess: ").upper().split(" ")

        if len(guess) != CODE_LENGTH:
            print(f"Please guess {CODE_LENGTH} colors")
            continue

        for color in guess:
            if color not in COLORS:
                print(f"Invalid color: {color}. Try a color from {COLORS}.")
                break
        else:
            break
    return guess

# Check if guess is correct
def check_guess(guess, real_code):
    color_counts = {}
    correct_pos = 0
    incorrect_pos = 0

    for color in real_code:
        if color not in color_counts:
            color_counts[color] = 0
        color_counts[color] += 1

    for guess_color, real_color in zip(guess, real_code):
        if guess_color == real_color:
            correct_pos += 1
            color_counts[guess_color] -= 1
    
    for guess_color, real_color in zip(guess, real_code):
        if guess_color in color_counts and color_counts[guess_color] > 0:
            incorrect_pos += 1
            color_counts[guess_color] -= 1
    
    return correct_pos, incorrect_pos

# Main game
def game():
    print(f"Welcome to Mastermind, you have {TRIES} attempts to guess the code.")
    print("The valid colors are: ", *COLORS)
    code = generate_code()
    for attempt in range(1, TRIES + 1):
        guess = guess_code()
        correct_pos, incorrect_pos = check_guess(guess, code)

        if correct_pos == CODE_LENGTH:
            print(f"You guessed the code in {attempt} tries!")
            break

        print(f"Correct Positions: {correct_pos} | Incorrect Positions: {incorrect_pos}")

    else:
        print("You ran out of tries, the correct code was: ", *code)

if __name__ == "__main__":
    game()
