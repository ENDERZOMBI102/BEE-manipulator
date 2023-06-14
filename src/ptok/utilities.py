import sys


def isFrozen() -> bool:
	"""
	If running in a frozen state, returns True
	:return: True if it is, otherwise false
	"""
	return hasattr( sys, 'frozen' )
