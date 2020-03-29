from config import *

def boolcmp(value):
    r"""
    a small function to compare bool values
    """
    if value in [True, "true", 1]:
        return True
    elif value in [False, "false", 0]:
        return False
    else:
        raise ValueError("invalid input!")


def isonline():
	try:
	    get("www.google.com")
	    return True
	except:
	    return False


def toNumbers(arg=None):
	nums = []
	for i in arg:
	    if i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.']:
	        nums.append(i)
	return int("".join(nums))

tkRoot = None
