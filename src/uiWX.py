import asyncio
import os
import webbrowser as wb
from pathlib import Path
from typing import Dict

import wx
import wx.adv
import wx.py.dispatcher as dispatcher

import aboutWindow
import beeManager
import browser
import config
import logWindow
import pluginSystem
import settingsUI
import utilities
from pluginSystem import Events
from srctools.logger import get_logger

if utilities.devEnv:
	import importlib


wx.InitAllImageHandlers()

# global variables
LOGGER = get_logger()
_menuIndex: int = 0


def newMenuIndex() -> int:
	global _menuIndex
	_menuIndex += 1
	return _menuIndex - 1


class root(wx.Frame):

	instance: 'root'
	settingsWindowInstance: settingsUI.window = None
	menus: Dict[str, wx.MenuItem] = {}

	def __init__(self):
		# load plugins
		super().__init__( None, title=f'BEE Manipulator {str(config.version)}' )
		# sets the app icon
		self.SetIcon( utilities.icon )
		# init the logging window
		asyncio.run( logWindow.init() )
		asyncio.run( appDateCheck() )
		# set the utilities.root pointer to the object of this class
		root.instance = self
		try:
			self.SetPosition( wx.Point( config.load('mainWindowPos') ) )
		except config.ConfigError:
			self.CenterOnScreen()
		self.SetSize(width=600, height=500)
		self.SetMinSize( wx.Size(width=600, height=500) )
		LOGGER.info(f'internet connected: {utilities.isonline()}')
		pluginSystem.systemObj.startSync()
		"""
		A menu bar is composed of menus, which are composed of menu items.
		This section builds the menu bar and binds actions to them
		"""
		# file menu bar
		self.fileMenu = wx.Menu()
		self.menus['openPortalDir'] = self.fileMenu.Append( newMenuIndex(), loc('menu.file.openportaldir.name')+'\tCtrl-P', loc('menu.file.openportaldir.description') )
		self.menus['openBeeDir'] = self.fileMenu.Append( newMenuIndex(), loc('menu.file.openbeedir.name')+"\tCtrl-B", loc('menu.file.openbeedir.description') )
		self.menus['syncGames'] = self.fileMenu.Append( newMenuIndex(), loc('menu.file.syncgames.name'), loc('menu.file.syncgames.description') )
		self.menus['exit'] = self.fileMenu.Append( newMenuIndex(), loc('menu.file.exit.name'), loc('menu.file.exit.description') )

		# options menu bar
		self.optionsMenu = wx.Menu()
		self.menus['settings'] = self.optionsMenu.Append( newMenuIndex(), loc('menu.options.settings.name')+'\tCtrl-S', loc('menu.options.settings.description') )
		self.menus['toggleLogWindow'] = self.optionsMenu.Append( newMenuIndex(), loc('menu.options.logtoggle.name')+'\tCtrl-L', loc('menu.options.logtoggle.description') )
		self.menus['reloadPlugins'] = self.optionsMenu.Append( newMenuIndex(), loc('menu.options.reloadplugins.name')+'\tCtrl-R', loc('menu.options.reloadplugins.description') )
		self.menus['reloadPackages'] = self.optionsMenu.Append( newMenuIndex(), loc('menu.options.reloadpackages.name'), loc('menu.options.reloadpackages.description') )

		# portal 2 menu bar
		self.portalMenu = wx.Menu()
		self.menus['verifyGameFiles'] = self.portalMenu.Append( newMenuIndex(), loc('menu.portal.vgf.name'), loc('menu.portal.vgf.description') )
		self.menus['uninstallBee'] = self.portalMenu.Append( newMenuIndex(), loc('menu.portal.uninstallbee.name'), loc('menu.portal.uninstallbee.description') )
		self.menus['installBee'] = self.portalMenu.Append( newMenuIndex(), loc('menu.portal.installbee.name'), loc('menu.portal.installbee.description') )
		self.menus['openP2'] = self.portalMenu.Append( newMenuIndex(), loc( 'menu.portal.openp2.name' ), loc( 'menu.portal.openp2.description' ) )
		self.menus['openBee'] = self.portalMenu.Append( newMenuIndex(), loc( 'menu.portal.openbee.name' ), loc( 'menu.portal.openbee.description' ) )

		# help menu bar
		self.helpMenu = wx.Menu()
		self.menus['about'] = self.helpMenu.Append( newMenuIndex(), loc('menu.help.about.name'), loc('menu.help.about.description') )
		self.menus['checkUpdates'] = self.helpMenu.Append( newMenuIndex(), loc('menu.help.cupdates.name'), loc('menu.help.cupdates.description') )
		self.menus['wiki'] = self.helpMenu.Append( newMenuIndex(), loc('menu.help.wiki.name'), loc('menu.help.wiki.description') )
		self.menus['github'] = self.helpMenu.Append( newMenuIndex(), loc('menu.help.github.name'), loc('menu.help.github.description') )
		self.menus['discord'] = self.helpMenu.Append( newMenuIndex(), loc('menu.help.discord.name'), loc('menu.help.discord.description') )

		# set menu item icons
		self.menus['about'].SetBitmap( wx.Bitmap(f'{config.resourcesPath}icons/menu_bm.png' ) )
		self.menus['checkUpdates'].SetBitmap( wx.Bitmap( f'{config.resourcesPath}icons/materialdesign/menu_update_black.png' ) )
		self.menus['wiki'].SetBitmap( wx.Bitmap(f'{config.resourcesPath}icons/menu_github.png' ) )
		self.menus['github'].SetBitmap( wx.Bitmap(f'{config.resourcesPath}icons/menu_github.png' ) )
		self.menus['discord'].SetBitmap( wx.Bitmap(f'{config.resourcesPath}icons/menu_discord.png' ) )

		# makes the menu bar
		self.menuBar = wx.MenuBar()
		self.menuBar.Append( self.fileMenu, loc('menu.file.name') )
		self.menuBar.Append( self.optionsMenu, loc('menu.options.name') )
		self.menuBar.Append( self.portalMenu, loc('menu.portal.name') )
		self.menuBar.Append( self.helpMenu, loc('menu.help.name') )

		# Give the menu bar to the frame
		self.SetMenuBar(self.menuBar)
		self.CreateStatusBar()
		self.SetStatusText( loc('statusbar.text', username=config.steamUsername() ) )

		# file menu
		self.Bind( wx.EVT_MENU, self.openp2dir, self.menus['openPortalDir'] )
		self.Bind( wx.EVT_MENU, self.openBEEdir, self.menus['openBeeDir'] )
		self.Bind( wx.EVT_MENU, self.syncGames, self.menus['syncGames'] )
		self.Bind( wx.EVT_MENU, self.exit, self.menus['exit'] )
		# options menu
		self.Bind( wx.EVT_MENU, self.openSettingsWindow, self.menus['settings'] )
		self.Bind( wx.EVT_MENU, logWindow.toggleVisibility, self.menus['toggleLogWindow'] )
		self.Bind( wx.EVT_MENU, self.reloadPlugins, self.menus['reloadPlugins'] )
		self.Bind( wx.EVT_MENU, self.reloadPackages, self.menus['reloadPackages'] )
		# portal 2 menu
		self.Bind( wx.EVT_MENU, self.verifyGameFiles, self.menus['verifyGameFiles'] )
		self.Bind( wx.EVT_MENU, self.uninstallBee, self.menus['uninstallBee'] )
		self.Bind( wx.EVT_MENU, self.installBee, self.menus['installBee'] )
		self.Bind( wx.EVT_MENU, self.openP2, self.menus['openP2'] )
		self.Bind( wx.EVT_MENU, self.openBee, self.menus['openBee'] )
		# help menu
		self.Bind( wx.EVT_MENU, self.openAboutWindow, self.menus['about'] )
		self.Bind( wx.EVT_MENU, self.checkUpdates, self.menus['checkUpdates'] )
		self.Bind( wx.EVT_MENU, self.openWiki, self.menus['wiki'] )
		self.Bind( wx.EVT_MENU, self.openGithub, self.menus['github'] )
		self.Bind( wx.EVT_MENU, self.openDiscord, self.menus['discord'] )
		# other events
		self.Bind( wx.EVT_CLOSE, self.OnClose, self )
		self.Bind( wx.EVT_SIZING, self.OnResize, self )
		self.Bind( wx.EVT_MAXIMIZE, self.OnMaximize, self )

		if config.load('beePath') is None:
			self.menus['uninstallBee'].Enable(False)
			self.menus['openBeeDir'].Enable(False)
		else:
			self.menus['installBee'].Enable(False)

		# register event handlers
		dispatcher.connect( receiver=self.RemoveMenu, signal=Events.UnregisterMenu )
		dispatcher.connect( receiver=self.RemoveBookPage, signal=Events.UnregisterBookPage )
		"""
		A notebook is a controller which manages multiple windows with associated tabs.
		This section makes the notebook
		"""
		self.book = wx.Notebook(
			self,
			name='Main Menu',
			size=wx.Size( self.GetSize().GetWidth(), self.GetSize().GetHeight() )
		)
		self.browserTab = PackageBrowserPage(self.book)
		self.book.AddPage( self.browserTab, 'Package Browser' )
		# trigger the register event
		dispatcher.send( Events.RegisterEvent, handler=pluginSystem.RegisterHandler() )

	# wx event callbacks
	def OnClose(self, evt: wx.CloseEvent):
		"""
		called when the window/application is about to close
		:param evt: placeholder
		"""
		# stop all plugins
		asyncio.run( pluginSystem.systemObj.unloadAndStop() )
		# get the window position and save it
		pos = list(self.GetPosition().Get())
		LOGGER.debug( f'saved main window position: {pos}' )
		config.save( pos, 'mainWindowPos' )
		config.save( None, 'placeholderForSaving' )
		self.Destroy()

	def OnResize( self, evt: wx.Event ):
		"""
		called when resizing the window, this permits to internal windows to resize aswell
		:param evt: placeholder
		"""
		self.book.SetSize( self.GetSize() )
		self.browserTab.browserObj.OnResize( self.GetSize() )

	def OnMaximize( self, evt: wx.MaximizeEvent ):
		self.browserTab.browserObj.OnResize( self.GetSize() )

	# file menu items actions
	@staticmethod
	def openp2dir(evt: wx.CommandEvent):
		"""
		opens the Portal 2 directory with the default file explorer
		:param evt: placeholder
		"""
		os.startfile( config.portalDir() )

	@staticmethod
	def openBEEdir(evt: wx.CommandEvent):
		"""
		opens the BEE2.4 directory with the default file explorer
		:param evt: placeholder
		"""
		os.startfile(
			Path( config.load('beePath') ).parent
			if config.load('beePath').lower().endswith('.exe')
			else Path( config.load('beePath') )
		)

	@staticmethod
	def syncGames(evt: wx.CommandEvent):
		"""
		still not know what this does
		:param evt: placeholder
		"""
		utilities.notimplementedyet()

	def exit(self, evt: wx.CommandEvent):
		"""
		called by the exit button, fowards to the root.OnClose() method
		:param evt: placeholder
		"""
		self.OnClose( wx.CloseEvent() )  # there's already an handler, so use that

	# options menu items actions
	def openSettingsWindow(self, evt: wx.CommandEvent):
		"""
		this function opens the settings window.
		when this is called for the first time create an instance of the window, so when
		called again it will be faster, because it don't have to create everything again
		:param evt: placeholder
		"""

		if utilities.devEnv:
			try:
				# reload the settings window
				importlib.reload( settingsUI )
				settingsUI.window().Show(self)
			except:
				pass
		else:
			if self.settingsWindowInstance is None:  # if the window was opened at least once, this isn't None
				self.settingsWindowInstance = settingsUI.window()  # create a new settings window instance
			self.settingsWindowInstance.show()  # show the window

	@staticmethod
	def reloadPlugins(evt: wx.CommandEvent):
		""" reloads the plugins """
		asyncio.run( pluginSystem.systemObj.reload() )

	def reloadPackages(self, evt: wx.CommandEvent):
		""" reloads the package view """
		self.browserTab.reload()
		self.book.Refresh()
		self.Update()
		self.Refresh()

	# portal 2 items actions
	def verifyGameFiles(self, evt: wx.CommandEvent):
		""" triggers the verify game cache dialog + event """
		if not config.load('showVerifyDialog'):
			# user really wants to verify the game files?
			dialog = wx.RichMessageDialog(
				parent=self,
				message='''This will remove EVERYTHING non stock from portal 2!\nclick yes ONLY if you are sure!''',
				caption='WARNING!',
				style=wx.YES_NO | wx.CENTRE | wx.ICON_WARNING | wx.STAY_ON_TOP | wx.NO_DEFAULT
			)
			dialog.ShowDetailedText(
				"if you don't want this dialog to show check this checkbox, but be aware, this is here to protect you"
			)
			dialog.ShowCheckBox("Don't show again")
			choice = dialog.ShowModal()
			if dialog.IsCheckBoxChecked():
				config.save( False, 'showVerifyDialog' )
			if choice == wx.ID_NO:
				return
		# yes he wants to
		print('YES')
		utilities.notimplementedyet()

	def uninstallBee(self, evt: wx.CommandEvent):
		""" called when the uninstall bee button is pressed """
		if config.load('showUninstallDialog', default=True):
			# the user really wants to uninstall BEE?
			diag = wx.MessageDialog(
				parent=self,
				message="You're sure to want to uninstall BEE?",
				caption='Warning!',
				style=wx.YES_NO | wx.STAY_ON_TOP | wx.CENTRE | wx.ICON_WARNING
			)
			if diag.ShowModal() == wx.ID_NO:
				return
		# uninstall BEE
		beeManager.uninstall()
		# toggle buttons
		self.menus['installBee'].Enable(True)
		self.menus['uninstallBee'].Enable(False)
		self.menus['openBeeDir'].Enable(False)

	def installBee(self, evt: wx.CommandEvent):
		""" called when the install bee button is pressed """
		# check if is installed
		if beeManager.beeIsPresent() and beeManager.packagesAreInstalled():
			wx.GenericMessageDialog(
				self,
				message='BEE2.4 has been found on default install path!\nNo need to install again :D',
				caption='Notice!',
				style=wx.OK | wx.STAY_ON_TOP | wx.CENTRE
			).ShowModal()
			config.save(f'{utilities.defBeePath}/BEE2/', 'beePath')
		elif beeManager.beeIsPresent() and not beeManager.packagesAreInstalled():
			wx.GenericMessageDialog(
				self,
				message='BEE2.4 has been found on default install path, but not the packages.\nThe packages will be downloaded',
				caption='Notice!',
				style=wx.OK | wx.STAY_ON_TOP | wx.CENTRE
			).ShowModal()
			config.save( f'{utilities.defBeePath}/BEE2/', 'beePath' )
			beeManager.installDefPackages()
		else:  # not installed
			dial = wx.DirDialog(
				self,
				message='Select where to install BEE (a BEE2 folder will be created)',
				# this gets the APPDATA path, go from Roaming to Local and then return the Programs folder full path
				defaultPath=utilities.defBeePath
			)
			# show the dialog and wait
			if dial.ShowModal() == wx.ID_CANCEL:
				return  # don't want to install anymore
			path = Path(dial.GetPath() + '/BEE2/')
			# create the missing folders
			if not path.exists():
				path.mkdir()
			# save the BEE path
			config.save( str( path.resolve() ).replace(r'\\', '/'), 'beePath' )
			# install BEE without messages
			beeManager.checkAndInstallUpdate(True)
		self.menus['installBee'].Enable(True)
		self.menus['uninstallBee'].Enable(False)
		self.menus['openBeeDir'].Enable(True)

	@staticmethod
	def openP2( evt: wx.CommandEvent ):
		path = f'{config.portalDir()}portal2.exe'
		LOGGER.info(f'starting Portal 2 ({path})')
		os.startfile( path )

	@staticmethod
	def openBee( evt: wx.CommandEvent ):
		path = f'{config.load("beePath")}BEE2.exe'
		LOGGER.info( f'starting BEE2 ({path})' )
		os.startfile( path )

	# help menu items actions
	@staticmethod
	def openAboutWindow(evt: wx.CommandEvent):
		aboutWindow.init()

	@staticmethod
	def checkUpdates(evt: wx.CommandEvent):
		asyncio.run( appDateCheck() )

	@staticmethod
	def openWiki(evt: wx.CommandEvent):
		openUrl('https://github.com/ENDERZOMBI102/BEE-manipulator/wiki')

	@staticmethod
	def openGithub(evt: wx.CommandEvent):
		openUrl('https://github.com/ENDERZOMBI102/BEE-manipulator')

	@staticmethod
	def openDiscord(evt: wx.CommandEvent):
		openUrl('https://discord.gg/hnGFJrz')

	# API methods
	def RemoveBookPage( self, page: wx.Panel ):
		index: int = self.book.FindPage(page)
		if index == wx.NOT_FOUND:
			raise pluginSystem.Errors.PageNotFoundException( f'unknown page "{page.GetName()}"' )
		else:
			self.book.RemovePage( index )

	def RemoveMenu(self, menu: str):
		"""
		Removes a menu from the main menubar
		:param menu: the name of the menu to remove
		:raises pluginSystem.Errors.MenuNotFoundException:
		"""
		index = self.menuBar.FindMenu(menu)
		if index == wx.NOT_FOUND:
			raise pluginSystem.Errors.MenuNotFoundException(f'unknown menu "{menu}"')
		else:
			self.menuBar.Remove(index)

	def AddMenu(self, menu: wx.Menu, title: str):
		"""
		Adds a menu to the main menubar
		:param menu: the menu object
		:param title: the menu name
		"""
		menuBar: wx.MenuBar = self.GetMenuBar()
		menuBar.Append(menu, title)
		menuBar.Refresh()


def openUrl(url: str):
	"""
	opens an url with the default browser
	:param url: the url to open
	"""
	LOGGER.info(f'opening "{url}" with default browser')
	wb.open(url)


async def appDateCheck():
	"""	Checks app updates """
	if not utilities.isonline():  # if we're not online return false
		return False
	data = utilities.checkUpdate( 'https://github.com/ENDERZOMBI102/BEE-manipulator', config.version )
	if data.url is None:
		if getattr(root, 'instance', False):
			wx.MessageBox(
				parent=root.instance,
				message='No updates found!',
				caption='BEE Manipulator'
			)
		return
	data = wx.GenericMessageDialog(
		parent=getattr(root, 'instance', None),
		message=f'An update for the app is available, do you want to update now?\n\n{data.description}',
		caption=f'Update Available - new version: {data.version}',
		style=wx.YES_NO | wx.ICON_WARNING | wx.STAY_ON_TOP | wx.NO_DEFAULT
	)
	if data.ShowModal() == wx.ID_NO:
		return  # user don't want to update
	# utilities.update()


class PackageBrowserPage(wx.Panel):

	loadingGif: wx.adv.AnimationCtrl
	browserObj: browser.Browser

	def __init__(self, master: wx.Notebook):
		super().__init__(
			parent=master,
			size=master.GetSize()
		)
		self.browserObj = browser.Browser(self)

	def reload(self):
		""" Reloads the browser window by creating a new object """
		if utilities.devEnv:
			try:
				importlib.reload(browser)
			except:
				pass
		self.browserObj = browser.Browser(self)
