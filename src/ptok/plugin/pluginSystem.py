from __future__ import annotations

from dataclasses import dataclass
from logging import Logger
from pathlib import Path

import srctools.logger



class PluginSystem:
	_logger: Logger

	def __init__( self ) -> None:
		self._logger = srctools.logger.get_logger( 'PluginSystem' )

	def init( self ) -> None:
		"""
		Initializes the plugin system by executing these steps.
		 - Search for possible plugins in the `./plugins/` folder
		 - Load the manifests
		 - Check dependencies
		 - Load core
		 - Load plugins
		"""
		candidates = self._search()

	def reloadAll( self ) -> None:
		""" Reload all plugins. """

	def reload( self, pluginid: str ) -> None:
		"""
		Reload a specific plugin.
		:param pluginid: the id of the plugin to load.
		"""

	def _search( self ) -> list[PluginCandidate]:
		for path in Path( './plugins' ).glob( '*.pt-plugin' ):
			self._logger.debug( f'Found candidate {path.name}' )



@dataclass
class PluginCandidate:
	pass


pluginSystem = PluginSystem = PluginSystem()
