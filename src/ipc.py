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

	def __init__(self, conn: socket.socket, server: ipcServer):
		self.conn = conn
		self.server = server
		self.thread = threading.Thread( target=self.rcv, daemon=True )
		self.thread.start()

	def rcv(self):
		while not self.closed:
			raw_size = self.conn.recv(64)
			size = int( raw_size.decode() )
			data = self.conn.recv(size)

			if data == '!SHUTDOWN_CONNECTION':
				self.closed = True
				continue
			parts = data.split('/')
			if parts[2] in self.server.handlers.keys():
				for hdlr in self.server.handlers[parts[2]]:
					hdlr(data)
		# close
		self.conn.close()
		self.thread.join()

	def shutdown(self):
		self.closed = True
		self.conn.close()
		self.thread.join()


class ipcServer:
	"""
	this class represents an IPC socket server.
	"""
	handlers: Dict[str, List[Callable] ]
	listening: bool
	port: int = 20306
	connections: List[ weakref.ref ]

	def __init__(self, port: int = None):
		if port:
			self.port = port
		logger.info(f'starting IPC server on port {self.port}')
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind( ('localhost', self.port) )
		logger.debug('starting listener')
		threading.Thread( target=self.serve_forever )

	def serve_forever(self):
		"""
		this function starts the IPC server
		"""
		while self.listening:
			conn, addr = self.socket.accept()
			self.connections.append( weakref.ref( Connection(conn, self) ) )

	def registerHandler(self, handler: Callable, proc: str):
		if proc in self.handlers.keys():
			self.handlers[proc].append(handler)
		else:
			self.handlers[proc] = []
			self.handlers.append(handler)





server = ipcServer()

