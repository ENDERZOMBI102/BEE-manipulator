from dataclasses import dataclass
from typing import Callable

import srctools


def emit( evt: str, *args, **kwargs ) -> None:
	""" Emits an event. """
	if evt in __listeners:
		__logger.debug( f'invoked {evt} with args={args} and kwargs={kwargs} on {len(__listeners[evt])} listeners' )
		for listener in __listeners[evt]:
			listener( *args, **kwargs )
	else:
		__logger.debug( f'invoked {evt} with args={args} and kwargs={kwargs} on 0 listeners' )


def on( evt: str, owner: str, listener: Callable[[...], None] ) -> None:
	"""
	Registers an event listener from plugin $owner for the event $evt.
	When the event is `emit()`ted the $listener callable will be invoked.
	"""
	if evt in __listeners:
		__listeners[evt].append( Listener( owner, listener ) )
	else:
		__listeners[evt] = [ Listener( owner, listener ) ]


@dataclass
class Listener:
	owner: str
	callback: Callable

	def __call__( self, *args, **kwargs ) -> None:
		self.callback( *args, **kwargs )


__listeners: dict[ str, list[ Listener ] ] = { }
__logger = srctools.logger.get_logger( 'eventSystem' )
