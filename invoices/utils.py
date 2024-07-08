import random
import string


def generate_reference():
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choices(characters, k=8))
    return f"{random_string}"
