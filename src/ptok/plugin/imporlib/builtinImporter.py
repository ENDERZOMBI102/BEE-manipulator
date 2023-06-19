import types

from importlib.resources.abc import Traversable

from . import Importer


class BuiltinImporter( Importer ):
	""" Tiny wrapper around the standard import mechanism. """
	_root: str

	def __init__( self, package: str ) -> None:
		self._root = package

	def load( self, path: str, last: bool = False ) -> types.ModuleType:
		mod = __import__( path )
		if last:
			for sect in path.split('.')[ 1 :]:
				mod = getattr( mod, sect )
		return mod

	def get_data( self, path: bytes | str ) -> bytes:
		return __loader__.get_data( path )

	def get_filename( self, fullname: str ) -> bytes | str:
		return __loader__.get_filename( path )

	def files( self ) -> Traversable:
		return __loader__.files()
