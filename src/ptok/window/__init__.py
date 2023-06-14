from PySide6.QtWidgets import *

from ..plugin import eventSystem


class RootWindow( QMainWindow ):
	def __init__( self ) -> None:
		super().__init__( parent=None )
		self.setWindowTitle( 'Portal Toolkit' )
		self.setMinimumSize( 500, 600 )

		eventSystem.emit( 'ptok.window.root.init', window=self )

		self.show()

	def show( self ) -> None:
		eventSystem.emit( 'ptok.window.root.shown', window=self )
		super().show()

	def hide( self ) -> None:
		eventSystem.emit( 'ptok.window.root.hidden', window=self )
		super().hide()
