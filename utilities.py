from config import *
from typing import Union
import tkinter as tk

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


def set_window_icon(window: Union[tk.Toplevel, tk.Tk]):
	"""Set the window icon."""
	import ctypes
	# Use Windows APIs to tell the taskbar to group us as our own program,
	# not with python.exe. Then our icon will apply, and also won't group
	# with other scripts.
	try:
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
			'BEEMANIPULATOR.application',
		)
	except (AttributeError, WindowsError, ValueError) as e:
		print(e)
		pass  # It's not too bad if it fails.

	LISTBOX_BG_SEL_COLOR = '#0078D7'
	LISTBOX_BG_COLOR = 'white'

argv = []
tkRoot = None
