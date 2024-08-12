import random
import secrets
import string


def generate_company_slug():
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choices(characters, k=24))
    return random_string


def generate_company_reference():
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(8))
    return random_string.upper()
