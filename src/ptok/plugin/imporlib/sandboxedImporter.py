import types

from importlib.resources.abc import Traversable
from srctools import FileSystem

from . import Importer
from ...util import TODO


class SandboxedImporter( Importer ):
	""" "Small" class to overwrite the concept of `import` for plugins """
	_fs: FileSystem

	def __init__( self, fs: FileSystem ) -> None:
		self._fs = fs

	def load( self, path: str, last: bool = False ) -> types.ModuleType:
		TODO( 'SandboxedImporter::load' )

	def get_data( self, path: bytes | str ) -> bytes:
		with self._fs.open_bin( path ) as file:
			return file.read()

	def get_filename( self, fullname: str ) -> bytes | str:
		TODO( 'SandboxedImporter::get_filename' )

	def files( self ) -> Traversable:
		TODO( 'SandboxedImporter::files' )
		# return importlib.resources.abc.Traversable()
