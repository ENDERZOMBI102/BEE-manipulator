from config import *

def boolcmp(val):
    r"""
    a small function to compare bool values
    """
    if value in [True, "true", 1]:
        return True
    elif value in [False, "false", 0]:
        return False
    else:
        raise ValueError("invalid input!")