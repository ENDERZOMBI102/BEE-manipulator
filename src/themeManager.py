from typing import Dict, Set

import wx

import config
from api.themeManager import ThemeManager as AbstractThemeManager, Theme


# ----------------------------------------------------------------------
def getWidgets( parent: wx.Window ):
	"""
	Return a list of all the child widgets
	"""
	items: Set[wx.Window] = { parent }
	for child in parent.GetChildren():
		items = items.union( getWidgets(child) )

	return items


# ----------------------------------------------------------------------
def darkRowFormatter( listctrl, dark=False ):
	"""
	Toggles the rows in a ListCtrl or ObjectListView widget.
	"""

	listItems = [ listctrl.GetItem( i ) for i in range( listctrl.GetItemCount() ) ]
	for index, item in enumerate( listItems ):
		if dark:
			if index % 2:
				item.SetBackgroundColour( "Dark Grey" )
			else:
				item.SetBackgroundColour( "Light Grey" )
		else:
			if index % 2:
				item.SetBackgroundColour( "Light Blue" )
			else:
				item.SetBackgroundColour( "Yellow" )
		listctrl.SetItem( item )


def darkMode( self, normalPanelColor ):
	"""
	Toggles dark mode
	"""
	widgets = getWidgets( self )
	dark_mode = True
	background = 'Dark Gray' if dark_mode else wx.NullColour
	foreground = 'White' if dark_mode else 'Black'

	for widget in widgets:
			if isinstance( widget, wx.ListCtrl ):
				darkRowFormatter( widget, dark=dark_mode )
				continue
			if isinstance( widget, wx.TextCtrl ):
				continue
			widget.SetBackgroundColour( background )
			widget.SetForegroundColour( foreground )
	self.Refresh()
	return dark_mode


class ThemeManager(AbstractThemeManager):

	themes: Dict[str, Theme] = {  }
	colordb: wx.ColourDatabase

	def init( self ) -> None:
		self.themes['Night'] = Theme( 'dark gray', 'white' )
		self.colordb = wx.ColourDatabase()

	def stop( self ) -> None:
		pass

	def onReload( self ) -> None:
		pass

	def registerTheme( self, theme: Theme ) -> None:
		pass

	def getThemes( self ) -> Dict[ str, Theme ]:
		return self.themes

	def getTheme( self ) -> Theme:
		pass

	def onWindowLoad( self, wndw: wx.Window ):
		theme = self.themes[ config.load('theme', 'Night') ]

		darkMode(wndw, wx.NullColour)

	def GetColor( self, color: str ) -> wx.Colour:
		clr: wx.Colour = self.colordb.Find(color)
		if not clr.IsOk():
			self.colordb.AddColour(color, wx.Colour(color) )
			clr = self.colordb.Find( color )
		return clr


manager: ThemeManager = ThemeManager()
