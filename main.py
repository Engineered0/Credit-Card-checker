import re
from datetime import datetime

def luhn_checksum(card_number):
    """Calculate the checksum using Luhn's algorithm."""
    digits = [int(d) for d in str(card_number)]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    return checksum % 10 == 0

def get_card_type(card_number):
    """Determine the card type based on the number."""
    card_patterns = {
        "Visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
        "MasterCard": r"^(5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$",
        "American Express": r"^3[47][0-9]{13}$",
        "Discover": r"^6(?:011|5[0-9]{2})[0-9]{12}$"
    }
    for card_type, pattern in card_patterns.items():
        if re.match(pattern, card_number):
            return card_type
    return "Unknown"

def check_expiration_date(exp_date):
    """Check if the card's expiration date has passed."""
    try:
        exp_date_obj = datetime.strptime(exp_date, "%m/%y")
        return exp_date_obj > datetime.now()
    except ValueError:
        return False

def check_cvv(cvv, card_type):
    """Validate the CVV based on card type."""
    cvv_length = len(cvv)
    return (card_type == "American Express" and cvv_length == 4) or (card_type != "American Express" and cvv_length == 3)

def validate_input(card_number, exp_date, cvv):
    """Validate the inputs before proceeding."""
    if not card_number.isdigit() or not cvv.isdigit():
        return False, "Card number and CVV must contain only digits."
    if not luhn_checksum(card_number):
        return False, "Invalid card number."
    if not check_expiration_date(exp_date):
        return False, "Invalid or expired date."
    card_type = get_card_type(card_number)
    if card_type == "Unknown":
        return False, "Card type is unknown or unsupported."
    if not check_cvv(cvv, card_type):
        return False, f"Invalid CVV for {card_type}."
    return True, card_type

def credit_card_checker():
    card_number = input("Enter your credit card number: ").strip()
    exp_date = input("Enter the expiration date (MM/YY): ").strip()
    cvv = input("Enter the CVV: ").strip()
    
    is_valid, message = validate_input(card_number, exp_date, cvv)
    if not is_valid:
        return message
    return f"Card is valid. Type: {message}."

print(credit_card_checker())
