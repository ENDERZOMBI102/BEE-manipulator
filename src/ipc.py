import threading
from multiprocessing.connection import PipeConnection
from typing import Callable, List, Dict

import ipc_mngr

from srctools.logger import get_logger

logger = get_logger()
# TODO: test all this


class Command:

	origin: str
	protocol: str
	parameters: List[ str ]


class ipcManager:

	_handlers: Dict[ str, List[ Callable[ [ PipeConnection, Command ], None ] ] ] = {}
	_listener: ipc_mngr.Listener = None
	_thread: threading.Thread

	def __init__( self, port: int = 30206 ):
		self.port = port

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
		sock.close()

	def listen(self):

		if self._listener is None:
			def run():
				self._listener = ipc_mngr.Listener( ('127.0.0.1', self.port), authkey='bm-ipc' )
				self._listener.msg_handler = self._msg_handler
				self._listener.listen()  # Listen forever
			self._thread = threading.Thread(target=run)
			self._thread.run()
		else:
			raise SyntaxError( 'called ipcManager.start() when the server is already listening.' )

	def addHandler(self, protocol: str, hdlr: Callable[ [PipeConnection, Command], None ]):
		# check if the given protocol list exist
		if self._handlers[ protocol ] is not []:
			# doesn't exist: create it
			self._handlers[ protocol ] = []
		# add the handler
		self._handlers[ protocol ].append( hdlr )

	def rmHandler(self, name: str, hdlr: Callable[ [PipeConnection, Command], None ] ):
		i = 0
		for i in range( len( self._handlers[name] ) ):
			if self._handlers[ name ][ i ] == hdlr:
				break
		del self._handlers[ name ][ i ]

	def stop(self):
		if self._listener is ipc_mngr.Listener:
			self._listener.stop()
			self._thread.join()
		else:
			raise SyntaxError('called ipcManager.stop() before starting it.')
