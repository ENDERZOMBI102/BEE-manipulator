import sys
from argparse import ArgumentParser
from typing import Optional, cast

import config
import utilities

_parser = ArgumentParser(
	prog='BEEManipulator.exe',
	description='Something cool'
)

# DEFAULT ARGUMENTS

_parser.add_argument(
	'--dev',
	help='Start BEE Manipulator in development mode, useful when debugging',
	action='store_true',
	dest='dev',
	default=False
)

_parser.add_argument(
	'--lang',
	help='Forces BEE Manipulator to start the specified language',
	action='store',
	dest='lang',
	default=None,
	type=str
)

_parser.add_argument(
	'--time',
	help='Logs how much time BEE Manipulator takes to start',
	action='store_true',
	dest='time',
	default=False
)

_parser.add_argument(
	'--port',
	help='Forces the IPC server to operate on the specified port',
	action='store',
	dest='port',
	default=20309,
	type=int
)

_parser.add_argument(
	'--flags',
	help='Sets the flags for the current BEE Manipulator session',
	action='store',
	dest='flags',
	default=None,
	type=str
)

_parser.add_argument(
	'-v',
	'--version',
	help='Show the program version and exits',
	action='version',
	version=str( config.version )
)

# BEE MANIPULATOR ARGUMENTS

_parser.add_argument(
	'--bmurl',
	help='Url for processing',
	action='store',
	dest='bmurl',
	default=None,
	type=str
)


class _result:
	dev: bool
	""" True if --dev was passed """
	lang: Optional[str]
	""" The lang passed to --lang """
	time: bool
	""" True if --time was passed """
	port: int
	""" The port passed to --port """
	flags: Optional[str]
	""" The flags passed to --flags """
	bmurl: Optional[str]
	""" The url for processing """


parsedArguments: _result = cast( _result, _parser.parse_args( sys.argv if utilities.devEnv else sys.argv[1:] ) )
