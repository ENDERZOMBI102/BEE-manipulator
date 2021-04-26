import threading
import time
from multiprocessing.connection import PipeConnection
from types import FunctionType
from typing import Callable, List, Dict, Tuple

import ipc_mngr
from wx.py import dispatcher

from api.manager import Manager
from srctools.logger import get_logger

logger = get_logger()


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


def sendToServer( origin: Tuple[ str, int ], url: str ) -> None:
	"""
	Very simple function to send a bmurl to another instance of BM
	:param origin: origin's socket (ip, port)
	:param url: the url to send
	"""
	# create client
	conn = ipc_mngr.Client( address=('127.0.0.1', 30206), authkey='bm-ipc' )
	# wait to be writable
	while not conn.writable:
		time.sleep( 0.2 )
	# send object
	conn.send( Command( origin, url ) )


class ipcManager(Manager):

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
		if cmd.protocol not in self._handlers:
			logger.warning(
				f'{cmd.origin} is trying to use an unregistered protocol "{cmd.protocol}", is it implemented in a plugin?'
			)
		else:
			if len( self._handlers ) > 0:
				for handler in self._handlers[cmd.protocol]:
					handler: FunctionType
					logger.debug(f'{handler.__name__} by {handler.__module__} is handling {cmd.parameters}')
					handler(sock, cmd)
			else:
				logger.warning(
					f'{cmd.origin} is trying to use a previously registered protocol "{cmd.protocol}" (implemented by a plugin).'
				)

	def init( self ):
		self._thread = threading.Thread(target=self.listen)
		self._thread.start()
		from pluginSystem import Events
		# use a lambda for security
		dispatcher.connect(lambda protocol, hdlr: self.rmHandler(protocol, hdlr), Events.UnregisterIpcHandler)

	def listen(self):
		self._listener = ipc_mngr.Listener( ('127.0.0.1', self.port), authkey='bm-ipc' )
		self._listener.msg_handler = self._msg_handler
		self._listener.listen()  # Listen forever

	def addHandler(self, protocol: str, hdlr: Callable[ [PipeConnection, Command], None ]):
		# check if the given protocol list exist
		if protocol not in self._handlers:
			# doesn't exist: create it
			self._handlers[ protocol ] = []
		# add the handler
		self._handlers[ protocol ].append( hdlr )

	def rmHandler(self, protocol: str, hdlr: Callable[ [PipeConnection, Command], None ] ):
		self._handlers[protocol].remove(hdlr)

	def stop(self):
		if isinstance(self._listener, ipc_mngr.Listener):
			self._listener.close()
			self._listener.stop()
			self._thread.join()
		else:
			raise RuntimeError('called ipcManager.stop() before starting it.')


manager: ipcManager = ipcManager()
manager.addHandler('view', lambda sock, cmd: logger.info( cmd.__dict__ ) )
