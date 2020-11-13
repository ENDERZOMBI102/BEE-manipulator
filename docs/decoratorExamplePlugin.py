from semver import VersionInfo

from pluginSystem import Plugin


@Plugin('test', VersionInfo.parse('3.4.5-pre.2+build.4') )
class test:

	async def load(self):
		print(__name__+' loaded!!')

	async def unload(self):
		print(__name__ + ' unloaded!!')
