import random
import string

def random_text(length):
    """
    Generate a random string of specified length consisting of letters and digits.

    Parameters:
    length (int): The length of the random string to be generated.

    Returns:
    str: A random string of specified length consisting of letters and digits.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))