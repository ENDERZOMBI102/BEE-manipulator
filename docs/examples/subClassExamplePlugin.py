from semver import VersionInfo

from pluginSystem import BasePlugin


class ExamplePlugin( BasePlugin ):

	def getName( self ) -> str:
		return 'SubclassTest'

	async def unload( self ):
		print( 'UNLOADED' )

	def getVersion( self ):
		return VersionInfo.parse( '3.4.5-pre.2+build.4' )

	async def load( self ):
		print( 'LOADED' )
