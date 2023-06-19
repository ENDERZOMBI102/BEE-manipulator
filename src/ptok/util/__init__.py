import sys
from typing import NoReturn


def TODO( name: str ) -> NoReturn:
	raise NotImplementedError( f'{name} is not yet implemented.' )


def isFrozen() -> bool:
	"""
	If running in a frozen state, returns True
	:returns: True if it is, otherwise false
	"""
	return hasattr( sys, 'frozen' )
