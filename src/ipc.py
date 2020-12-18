import threading
import time
from multiprocessing.connection import PipeConnection
from typing import Callable, List, Dict, Tuple

import ipc_mngr

from srctools.logger import get_logger

logger = get_logger()
# TODO: test all this


class Command:
	"""
	A data class for transmitting and receiving inter process
	communication command data, ex. used by "open with bm"
	"""

	origin: Tuple[ str, int ]
	protocol: str
	parameters: List[ str ]

	def __init__( self, origin: Tuple[ str, int ], url: str ):
		self.origin = ('127.0.0.1', 30206) if origin is None else origin
		url = url.replace('bm://', '', 1)
		self.protocol = url.split('/')[0]
		self.parameters = url.split('/')[1:]


def sendToServer( origin: Tuple[ str, int ], url: str ):
	"""
	Very simple function to send a bmurl to another instance of BM
	:param origin: origin's ip
	:param url: the url to send
	"""
	# create client
	conn = ipc_mngr.Client( address=('127.0.0.1', 30206), authkey='bm-ipc' )
	# wait to be writable
	while not conn.writable:
		time.sleep( 0.2 )
	# send object
	conn.send( Command( origin, url ) )


class ipcManager:

	_handlers: Dict[ str, List[ Callable[ [ PipeConnection, Command ], None ] ] ] = {}
	queue: List[str]
	_listener: ipc_mngr.Listener = None
	_thread: threading.Thread

	def __init__( self, port: int = 30206 ):
		self.port = port
		self.queue = []

	def _msg_handler( self, sock: PipeConnection, cmd: Command):
		"""
		PRIVATE

		makes sure to manage the call correctly
		"""
		logger.info(f'Call received from {cmd.origin} on port {self._listener.last_accepted}')
		if cmd.protocol not in self._handlers.keys():
			logger.warning(
				f'{cmd.origin} is trying to use an unregistered protocol "{cmd.protocol}", is it implemented in a plugin?'
			)
		else:
			for handler in self._handlers[cmd.protocol]:
				handler(sock, cmd)

	def listen(self):
		if self._listener is None:
			def run():
				self._listener = ipc_mngr.Listener( ('127.0.0.1', self.port), authkey='bm-ipc' )
				self._listener.msg_handler = self._msg_handler
				self._listener.listen()  # Listen forever
			self._thread = threading.Thread(target=run)
			self._thread.run()
		else:
			raise RuntimeError( 'called ipcManager.start() when the server is already listening.' )

	def addHandler(self, protocol: str, hdlr: Callable[ [PipeConnection, Command], None ]):
		# check if the given protocol list exist
		if protocol not in self._handlers.keys():
			# doesn't exist: create it
			self._handlers[ protocol ] = []
		# add the handler
		self._handlers[ protocol ].append( hdlr )

	def rmHandler(self, protocol: str, hdlr: Callable[ [PipeConnection, Command], None ] ):
		i = 0
		for i in range( len( self._handlers[ protocol ] ) ):
			if self._handlers[ protocol ][ i ] == hdlr:
				break
		del self._handlers[ protocol ][ i ]

	def stop(self):
		if self._listener is ipc_mngr.Listener:
			self._listener.stop()
			self._thread.join()
		else:
			raise RuntimeError('called ipcManager.stop() before starting it.')
