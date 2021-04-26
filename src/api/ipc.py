from multiprocessing.connection import PipeConnection
from typing import Tuple, List, Callable

from api.manager import Manager


class Command:
	"""
	A data class for transmitting and receiving inter process
	communication command data, ex. used by "open with bm"
	"""

	origin: Tuple[ str, int ]
	protocol: str
	parameters: List[ str ]


def sendToServer( origin: Tuple[ str, int ], url: str ) -> None:
	"""
	Very simple function to send a bmurl to another instance of BM
	:param origin: origin's socket (ip, port)
	:param url: the url to send
	"""


class ipcManager(Manager):

	queue: List[str]

	def __init__( self, port: int = 30206 ):
		self.port = port
		self.queue = []

	def init( self ):
		""" Initialize the ipc server """

	def addHandler(self, protocol: str, hdlr: Callable[ [PipeConnection, Command], None ]) -> None:
		"""
		Adds an handler to the ipc server
		:param protocol: protocol the this callable will handle
		:param hdlr:
		"""

	def rmHandler(self, protocol: str, hdlr: Callable[ [PipeConnection, Command], None ] ) -> None:
		"""
		Removes an handler from a protocol
		:param protocol: protocol to search the handler in
		:param hdlr: handler to remove
		"""

	def stop(self):
		""" Stops the ipc server """


manager: ipcManager
