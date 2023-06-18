from importlib.resources.abc import Traversable
from srctools import FileSystem

from . import Importer


class SandboxedImporter( Importer ):
	""" "Small" class to overwrite the concept of `import` for plugins """
	_fs: FileSystem

	def __init__( self, fs: FileSystem ) -> None:
		self._fs = fs

	def get_data( self, path: bytes | str ) -> bytes:
		with self._fs.open_bin( path ) as file:
			return file.read()

	def get_filename( self, fullname: str ) -> bytes | str:
		pass

	def files( self ) -> Traversable:
		return importlib.resources.abc.Traversable()
