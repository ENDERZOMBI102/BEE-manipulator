import datetime
from logging import Logger
from pathlib import Path

import srctools.logger
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyleFactory

import ptok.util
import ptok.config
from ptok.plugin import pluginSystem
from ptok.window import RootWindow


logger: Logger


def main( argv: list[str] ) -> int:
	if not ptok.util.isFrozen():
		# avoid running anywhere but inside `run`
		cwd = Path.cwd()
		shouldExit = False
		if cwd.name != 'run':
			shouldExit = True
		elif 'src' in cwd.parts:
			path = Path( cwd.root )
			for part in cwd.parts[ 1 :]:
				if part == 'src':
					break
				path /= part
			shouldExit = ( path / 'run' ).exists()

		if shouldExit:
			print( '[F] startup: Started with working directory not set to `$REPO/run`, do not do this! aborting...', file=sys.stderr )
			return 1

		# overwrite stdout log level if launched from source
		import os
		os.environ[ 'SRCTOOLS_DEBUG' ] = '1'
		print( f'[I] startup: Running in a developer environment.' )
	else:
		print( f'[I] startup: Running in a packed environment.' )

	global logger
	logger = srctools.logger.init_logging( filename='./logs/latest.log', main_logger='PortalTk', error=onUncaughtException )

	logger.info( f'Initialized logging at {datetime.datetime.now().strftime("%H:%M:%S")}' )
	QApplication( argv )
	QApplication.setStyle( QStyleFactory.create( 'Fusion' ) )
	QApplication.setWindowIcon( QIcon( 'resources/icon.png' ) )
	QApplication.setApplicationName( 'PortalToolkit' )
	QApplication.setApplicationDisplayName( 'Portal Toolkit' )
	QApplication.setApplicationVersion( '0.1.0' )
	pluginSystem.init()
	pluginSystem.getEntrypoints( 'main' )()
	root = RootWindow()
	logger.info( 'Startup completed!' )

	code = QApplication.exec()

	ptok.config.save()
	return code


def onUncaughtException( exc: BaseException ) -> None:
	pass


if __name__ == '__main__':
	import sys
	sys.exit( main( sys.argv ) )
