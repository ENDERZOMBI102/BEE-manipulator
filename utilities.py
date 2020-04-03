from config import *
from typing import Union
import tkinter as tk
import tkinter.commondialog as cd
from srctools.logger import get_logger

LOGGER = get_logger("utils")

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
	global LOGGER
	try:
		get("www.google.com")
		LOGGER.debug("we're online folks!")
		return True
	except:
		LOGGER.debug("we're offline folks!")
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
		LOGGER.warning(f'failed for {window.title}')# It's not too bad if it fails.

	LISTBOX_BG_SEL_COLOR = '#0078D7'
	LISTBOX_BG_COLOR = 'white'

argv = []
tkRoot = None
