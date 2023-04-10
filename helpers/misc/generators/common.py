from string import ascii_letters, digits
from random import choices


def generate_random_string(prefix=None, suffix=None, length=10):
    symbols = ascii_letters + digits
    result = ''.join(choices(population=symbols, k=length))

    if prefix:
        result = f"{prefix}_{result}"

    if suffix:
        result = f"{result}_{suffix}"

    return result
