import PySide6.QtGui
from PySide6.QtCore import SIGNAL
from PySide6.QtWidgets import *

from ..plugin import eventSystem


class RootWindow( QMainWindow ):
	def __init__( self ) -> None:
		super().__init__( parent=None )
		self.setWindowTitle( 'Portal Toolkit' )
		self.setMinimumSize( 500, 600 )

		eventSystem.emit( 'ptok.window.root.init', window=self )

		self.show()

	def closeEvent( self, evt: PySide6.QtGui.QCloseEvent ) -> None:
		eventSystem.emit( '' )

	def showEvent( self, event: PySide6.QtGui.QShowEvent ) -> None:
		eventSystem.emit( 'ptok.window.root.shown', window=self )

	def hideEvent( self, evt: PySide6.QtGui.QHideEvent ) -> None:
		eventSystem.emit( 'ptok.window.root.hidden', window=self )
