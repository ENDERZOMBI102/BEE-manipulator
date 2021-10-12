from dataclasses import dataclass
from pprint import pprint

import eparser


class Version:
	major, minor, patch, build = 0, 0, 0, ''

	def __init__( self, string: str ):
		tmp = string.split('.', 2)
		tmp2 = tmp[2].split('+')
		tmp[2], self.build = tmp2[0], tmp2[1].replace('build.', '') if len( tmp2 ) == 2 else ''
		self.major, self.minor, self.patch = [ int(x) for x in tmp ]

	def __toe__( self ) -> str:
		return f'{self.major}.{self.minor}.{self.patch}{f"+build.{self.build}" if self.build else ""}'

	def __repr__(self) -> str:
		return f'Version(major={self.major}, minor={self.minor}, patch={self.patch}, build=\'{self.build}\')'


@dataclass
class Package:
	name: str
	version: Version
	optional: bool


@dataclass
class Plugin:
	id: str
	url: str
	version: Version


testCaseObj = {
	'name': 'Test Plugin',
	'id': 'bm.enderzombi102.jsrefactor',
	'desc': 'Polyfills for BM\'s CEF widgets',
	'authors': [ 'ENDERZOMBI102' ],
	'entrypoints': {
		'main': 'self.src.main',
		'event': 'self.src.event'
	},
	'dependencies': [
		Package(
			'Pillow',
			Version('1.7.0'),
			False
		),
		Plugin(
			'bm.enderzombi102.jsengine',
			'github.com/ENDERZOMBI102/plugins$jsengine',
			Version('1.0.0+build.24')
		)
	]
}


testCaseStr = '''name: Test Plugin
id: bm.enderzombi102.jsrefactor
desc: Polyfills for BM's CEF widgets
authors:
	ENDERZOMBI102
entrypoints:
	main: self.src.main
	event: self.src.event
dependencies:
	.Package:
		name: Pillow
		version: 1.7.0
		optional: false
	.Plugin:
		id: bm.enderzombi102.jsengine
		url: github.com/ENDERZOMBI102/plugins$jsengine
		version: 1.0.0+build.24'''


if __name__ == '__main__':
	print( eparser.dumps(testCaseObj) )
	pprint( eparser.loads( testCaseStr, 'test.e', [Version, Package, Plugin] ) )
