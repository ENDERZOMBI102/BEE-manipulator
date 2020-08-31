import socket
import threading
import weakref
from typing import Callable, List, Dict

from srctools.logger import get_logger

logger = get_logger()
# TODO: test all this


class Connection:

	conn: socket.socket
	port: int
	closed: bool = False
	thread: threading.Thread

	def __init__(self, conn: socket.socket, server: object):
		self.conn = conn
		self.server = server
		# create a thread, it'll make the object permanent until its closed
		self.thread = threading.Thread( target=self.rcv, daemon=True )
		# start the thread
		self.thread.start()

	def rcv(self):
		# if the connection isn't closed, loop
		while not self.closed:
			# wait and receive the header
			raw_size = self.conn.recv(64)
			# msg size
			size = int( raw_size.decode() )
			# receive the raw data (bytes)
			raw_data = self.conn.recv(size)
			# decode the raw data
			data: str = raw_data.decode()
			# this will close the connection
			if data == '!SHUTDOWN_CONNECTION':
				self.closed = True
				continue
			# remove "bm://"
			data = ''.join( data.split('/')[ 2:len(data) ] )
			# get the handler key
			hdlrkey = data.split('/')[0]
			# check if the hdlrkey is in the handlers
			if hdlrkey in self.server.handlers.keys():
				# cycle in the handlers in that key
				for hdlr in self.server.handlers[hdlrkey]:
					# execute handler with the data as parameter
					hdlr(data)
			else:
				# no key!
				logger.warning(f'unknown hdlrkey "{hdlrkey}" in ipc message, aborting processing')
		# close the connection
		self.conn.close()
		# close the thread
		self.thread.join()

	def shutdown(self):
		# stop the loop
		self.closed = True


class ipcServer:
	"""
	this class represents an IPC socket server.
	"""
	handlers: Dict[str, List[Callable] ]
	listening: bool
	port: int = 20306
	connections: List[ weakref.ref ]

	def __init__(self, port: int = None):
		# if port is specified, use that port
		if port is not None:
			self.port = port
		logger.info(f'starting IPC server on port {self.port}')
		logger.debug('binding socket..')
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind( ('localhost', self.port) )
		logger.debug('socket')
		logger.debug('starting listener thread..')
		self.thread = threading.Thread( target=self.serve_forever )
		self.thread.start()
		logger.debug('listener thread started')
		logger.info('IPC server started!')

	def serve_forever(self):
		"""
		this function starts the IPC server
		"""
		self.listening = True
		while self.listening:
			conn, addr = self.socket.accept()
			self.connections.append( weakref.ref( Connection(conn, self) ) )

	def registerHandler(self, handler: Callable, hdlrkey: str):
		"""
		register an handler
		:param handler: the callable that will be called
		:param hdlrkey: what the handler handle
		:return:
		"""
		if hdlrkey in self.handlers.keys():
			self.handlers[hdlrkey].append(handler)
		else:
			self.handlers[hdlrkey] = []
			self.handlers.append(handler)

	def shutdown(self):
		self.listening = False
		self.socket.close()


# ipcServer object
serverObj: ipcServer


def start(port: int = None):
	global serverObj
	if port is None:
		serverObj = ipcServer()
	else:
		serverObj = ipcServer(port)

