import abc
from importlib.abc import SourceLoader, InspectLoader
from importlib.resources.abc import TraversableResources, Traversable


class Importer( SourceLoader, InspectLoader, TraversableResources, metaclass=abc.ABCMeta ):
	""" "Small" abstract class to overwrite the concept of `import` for plugins """

	@abc.abstractmethod
	def get_data( self, path: str ) -> bytes:
		"""
		Abstract method which returns the bytes for the specified path.
		:param path: path of the file to read the data from.
		:returns: the bytes read for that file.
		"""

	@abc.abstractmethod
	def get_filename( self, fullname: str ) -> bytes | str:
		"""

		"""

	@abc.abstractmethod
	def files( self ) -> Traversable:
		"""

		"""


from .sandboxedImporter import SandboxedImporter
