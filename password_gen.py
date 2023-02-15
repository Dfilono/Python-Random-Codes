import string
import random

def generate_pass(min_length, numbers = True, special = True):
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    chars = letters
    if numbers:
        chars += digits
    if special:
        chars += special_chars
    
    pswd = ''
    criteria = False
    has_num = False
    has_spec = False

    while not criteria or len(pswd) < min_length:
        new_char = random.choice(chars)
        pswd += new_char

        if new_char in digits:
            has_num = True
        elif new_char in special_chars:
            has_spec = True

        criteria = True
        if numbers:
            criteria = has_num
        if special:
            criteria = criteria and has_spec

    return pswd

min_length = int(input("Enter the minimum length: "))
has_number = input("Does the password contain numbers? (y/n)").lower()  == 'y'
has_spec = input("Does the password contain special characters? (y/n)").lower()  == 'y'
pwd = generate_pass(min_length, has_number, has_spec)
print("The generated password is: ", pwd)
