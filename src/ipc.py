import asyncio
import socket
from typing import Callable, List

from srctools.logger import get_logger

logger = get_logger()


def connection(self, conn: socket.socket, addr: str, master: object):
	closed: bool = False
	logger.debug(f'opened connection with {addr}.')
	logger.debug('waiting for data..')
	while not closed:
		length = self.conn.recv(30).decode()
		logger.debug(f'receiving data (length: {length}).')
		data = self.conn.recv(length).decode()
		logger.debug(f'received data from {addr}.')
		if data == '!DiSCONNECT':
			conn.close()
			closed = True
		else:
			for handle in master.handles:
				handle(data)


class ipcServer:
	"""
	this class represents an IPC socket server.
	"""
	handlers: List[Callable]
	listening: bool
	port: int = 20306

	def __init__(self, port: int = None):
		if port:
			self.port = port
		logger.info(f'starting IPC server on port {self.port}')
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('localhost', self.port))
		asyncio.run(self.run())

	def listen(self):
		self.socket.listen()
		self.listening = True

	async def run(self):
		"""
		this function starts the IPC server
		"""
		self.listening()
		while self.listening:
			conn, addr = self.socket.accept()
			connection(conn, addr, self)
