import importlib
from importlib.abc import SourceLoader, InspectLoader
from importlib.resources.abc import TraversableResources

from srctools import FileSystem


class Importer( SourceLoader, InspectLoader, TraversableResources ):
	""" "Small" class to overwrite the concept of `import` for plugins """
	_fs: FileSystem

	def __init__( self, fs: FileSystem ) -> None:
		self._fs = fs

	def get_data( self, path: bytes | str ) -> bytes:
		with self._fs.open_bin( path ) as file:
			return file.read()

	def get_filename( self, fullname: str ) -> bytes | str:
		pass

	def files( self ) -> importlib.resources.abc.Traversable:
		return importlib.resources.abc.Traversable()
