def get_card_number():
    """
    Prompts the user for a credit card number and ensures the input is
    a positive string of digits that is not empty.
    """
    while True:
        # Gets input as a string (easier for slicing and prefix checks)
        # Added .strip() to both ends for robustness against accidental spaces/newlines
        card_num_str = input("Enter credit card number: ").strip()

        # Checks if the string contains only digits and is not empty
        if card_num_str.isdigit() and len(card_num_str) > 0:
            return card_num_str
        else:
            print("Invalid input. Please enter a number containing only digits.")


def check_luhn(card_num_str):
    """
    Implements Luhn's Algorithm to determine if the number is potentially valid.
    """
    # Convert the string of digits into a list of integers,
    digits = [int(d) for d in card_num_str]

    digits.reverse()

    # Initialized sum for the two main components of the algorithm
    sum_multiplied = 0
    sum_unmultiplied = 0

    # Phase 2 logic:
    for index, digit in enumerate(digits):
        # checking from the second-to-last digit, which is at
        # index 1 (odd indices in the reversed list).
        if index % 2 != 0:
            # Multiply every second digit by 2
            multiplied = digit * 2

            # Add the digits of the multiplied product
            if multiplied > 9:
                sum_multiplied += (multiplied // 10) + (multiplied % 10)
            else:
                sum_multiplied += multiplied
        else:
            #Sum the digits that were not multiplied
            sum_unmultiplied += digit

    total_sum = sum_multiplied + sum_unmultiplied

    return total_sum % 10 == 0

# Get the validated card number string
card_number = get_card_number()

# Perform the Luhn Check
if not check_luhn(card_number):
    print("INVALID")
else:
    # Perform Prefix and Length Check
    length = len(card_number)

    # AMEX Check (15 digits, starts with 34 or 37)
    if length == 15 and card_number.startswith(('34', '37')):
        print("AMEX")

    # VISA Check (13 or 16 digits, starts with 4)
    elif (length == 13 or length == 16) and card_number.startswith('4'):
        print("VISA")

    # MASTERCARD Check (16 digits, starts with 51-55)
    elif length == 16 and card_number.startswith(('51', '52', '53', '54', '55')):
        print("MASTERCARD")

    else:
        # If Luhn passed but none of the lengths/prefixes matched, it's invalid.
        print("INVALID")
"""
check50
cs50/problems/2025/x/sentimental/credit

:) credit.py exists.
Log
checking that credit.py exists...

:) identifies 378282246310005 as AMEX
Log
running python3 credit.py...
sending input 378282246310005...
checking for output "AMEX\n"...

:) identifies 371449635398431 as AMEX
Log
running python3 credit.py...
sending input 371449635398431...
checking for output "AMEX\n"...

:) identifies 5555555555554444 as MASTERCARD
Log
running python3 credit.py...
sending input 5555555555554444...
checking for output "MASTERCARD\n"...

:) identifies 5105105105105100 as MASTERCARD
Log
running python3 credit.py...
sending input 5105105105105100...
checking for output "MASTERCARD\n"...

:) identifies 4111111111111111 as VISA
Log
running python3 credit.py...
sending input 4111111111111111...
checking for output "VISA\n"...

:) identifies 4012888888881881 as VISA
Log
running python3 credit.py...
sending input 4012888888881881...
checking for output "VISA\n"...

:) identifies 4222222222222 as VISA
Log
running python3 credit.py...
sending input 4222222222222...
checking for output "VISA\n"...

:) identifies 1234567890 as INVALID
Log
running python3 credit.py...
sending input 1234567890...
checking for output "INVALID\n"...

:) identifies 369421438430814 as INVALID
Log
running python3 credit.py...
sending input 369421438430814...
checking for output "INVALID\n"...

:) identifies 4062901840 as INVALID
Log
running python3 credit.py...
sending input 4062901840...
checking for output "INVALID\n"...

:) identifies 5673598276138003 as INVALID
Log
running python3 credit.py...
sending input 5673598276138003...
checking for output "INVALID\n"...

:) identifies 4111111111111113 as INVALID
Log
running python3 credit.py...
sending input 4111111111111113...
checking for output "INVALID\n"...

:) identifies 4222222222223 as INVALID
Log
running python3 credit.py...
sending input 4222222222223...
checking for output "INVALID\n"...
"""
