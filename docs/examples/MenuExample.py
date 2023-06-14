import wx
import wx.py.dispatcher as dispatcher
from semver import VersionInfo

from pluginSystem import Plugin, Events, RegisterHandler


@Plugin(name='MenuBar Menu Example', version=VersionInfo(1, 0, 0) )
class MenuExample:

	exampleMenu: wx.Menu

	async def load(self):
		# create a menu object
		self.exampleMenu = wx.Menu()
		# add an item to it, and save it
		exampleItem = self.exampleMenu.Append(18, 'Example Item', 'This is the example item description')

		# bind the press of that item to a function
		self.exampleMenu.Bind(wx.EVT_MENU, self.pressed, exampleItem)

		# listen for the RegisterMenus event with the registerMenu method as callback
		dispatcher.connect( self.registerHandler, Events.RegisterEvent )

	def pressed(self, evt: wx.CommandEvent):
		wx.GenericMessageDialog(
			parent=wx.GetTopLevelWindows()[0],
			caption='Pressed!',
			message='The example item was pressed!'
		).ShowModal()

	async def unload(self):
		# unregister the menu from the menuBar
		dispatcher.send( Events.UnregisterMenu, menu='Example Menu' )
		# remove the menu
		self.exampleMenu.Destroy()

	def registerHandler( self, handler: RegisterHandler ):
		handler.RegisterMenu( self.exampleMenu, 'Example Menu' )
