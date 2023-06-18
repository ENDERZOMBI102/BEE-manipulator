import random
import zipfile
from dataclasses import dataclass
import logging
from pathlib import Path

import pydantic
import srctools
import tomlkit
from pydantic import BaseModel, constr
from srctools import FileSystem
from srctools.filesys import ZipFileSystem

import ptok
from . import imporlib


class Manifest(BaseModel):
	id: constr( regex='[a-z0-9_-]{4,}' )
	name: str
	description: str
	authors: tuple[ str, ... ]
	tags: tuple[ str, ... ]
	version: str
	entrypoints: dict[ str, str ]
	dependencies: dict[ str, str ]

	class Config:
		allow_mutation = False


@dataclass( frozen=True )
class PluginContainer:
	path: Path
	contents: FileSystem
	manifest: Manifest
	importer: 'imporlib.SandboxedImporter'
	builtin: bool = False

	def __post_init__( self ) -> None:
		if ( 'builtin' in self.manifest.tags or 'base' in self.manifest.tags ) and not self.builtin:
			raise ValueError( 'External plugins cannot have the "base" or "builtin" tags.' )


class PluginSystem:
	_logger: logging.Logger

	def __init__( self ) -> None:
		self._logger = srctools.logger.get_logger( 'PluginSystem' )

	@property
	def pluginFolder( self ) -> Path:
		return Path( './plugins' )

	def init( self ) -> None:
		"""
		Initializes the plugin system by executing these steps.
		 - [x] Search for possible plugins in the `./plugins/` folder
		 - [x] Load the manifests
		 - [x] Add builtin plugins
		 - [ ] Check dependencies
		 - [ ] Load core
		 - [ ] Load plugins
		"""
		candidates = self._search()
		containers = self._load( candidates )
		random.shuffle( containers )
		containers += self._loadBuiltins()
		containers.reverse()  # make sure builtins are the first plugins

		self._checkDependencies( containers )

	def _search( self ) -> list[Path]:
		self.pluginFolder.mkdir( exist_ok=True )
		candidates = [  ]
		for path in self.pluginFolder.glob( '*.pt-plugin' ):
			try:
				with zipfile.ZipFile( path ) as zipped:
					zipped.getinfo( 'plugin.toml' )
				candidates.append( path )
				self._logger.debug( f'Found candidate {path.name}' )
			except ( KeyError, zipfile.BadZipfile ):
				self._logger.warning( f'Bad plugin file: `{path}` please remove or fix.' )
		return candidates

	def _load( self, candidates: list[Path] ) -> list[PluginContainer]:
		containers = [ ]
		for candidate in candidates:
			zipped = zipfile.ZipFile( candidate )
			fs = ZipFileSystem( candidate, zipped )

			try:
				with fs.open_str( 'plugin.toml' ) as file:
					doc = tomlkit.parse( file.read() )

				manifest = Manifest( **doc['plugin'].unwrap() )
				self._logger.debug( f'Created manifest for `{manifest.id}`' )
			except pydantic.ValidationError:
				self._logger.error( f'Plugin located at {candidate.absolute()} has an invalid id: {doc["plugin"]["id"]} ( IDs must match the regex `[a-z0-9_-]{{4,}}` )' )
				if ptok.config.get().fastFailDuringLoad:
					raise
				continue
			except Exception as e:
				self._logger.exception( 'Error during manifest loading:' )
				if ptok.config.get().fastFailDuringLoad:
					raise
				continue

			try:
				importer = ptok.plugin.imporlib.SandboxedImporter( fs )
				self._logger.debug( f'Created Importer for `{manifest.id}`' )
			except Exception as e:
				self._logger.exception( 'Error during manifest loading:', e )
				if ptok.config.get().fastFailDuringLoad:
					raise
				continue

			self._logger.debug( f'Created container for `{manifest.id}`' )
			containers.append( PluginContainer( candidate, fs, manifest, importer ) )
		return containers

	def _loadBuiltins( self ) -> list[PluginContainer]:
		base = PluginContainer(
			path=Path( ptok.__file__ ),
			contents=None,
			manifest=Manifest(
				id='portal-toolkit',
				name='Portal Toolkit',
				description='A modular and pluggable set of tools for the games of the Portal series.',
				authors=( 'ENDERZOMBI102 <enderzombi102.end@gmail.com>', ),
				tags=( 'builtin', 'base' ),
				version='0.1.0',
				entrypoints={ },
				dependencies={ },
			),
			importer=None,
			builtin=True
		)

		doc = tomlkit.parse( ( Path( __file__ ).parent / '../core/plugin.toml' ).resolve().read_text() )
		core = PluginContainer(
			path=Path(),
			contents=None,
			manifest=Manifest( **doc['plugin'].unwrap() ),
			importer=None,
			builtin=True
		)
		builtins = [ base, core ]

		self._logger.debug( f'Loaded {len( builtins )} builtin plugins ( {", ".join( map( lambda builtin: builtin.manifest.id, builtins ) )} )' )
		return builtins

	def _checkDependencies( self, containers ):
		pass


pluginSystem = PluginSystem = PluginSystem()
