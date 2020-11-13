import asyncio
import os
import webbrowser as wb
from pathlib import Path

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

# init important things
LOGGER = get_logger()

if utilities.env == 'dev':
	import importlib


wx.InitAllImageHandlers()


class root(wx.Frame):

	instance: 'root'
	settingsWindowInstance: settingsUI.window = None

	def __init__(self):
		# load plugins
		super().__init__( None, title=f'BEE Manipulator {str(config.version)}' )
		# sets the app icon
		self.SetIcon(utilities.icon)
		# init the logging window
		asyncio.run( logWindow.init() )
		asyncio.run( appDateCheck() )
		# set the utilities.root pointer to the object of this class
		root.instance = self
		try:
			self.SetPosition(wx.Point(config.load('mainWindowPos')))
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
		openPortalDirItem = self.fileMenu.Append(0, loc('menu.file.openportaldir.name')+'\tCtrl-P', loc('menu.file.openportaldir.description') )
		openBeeDirItem = self.fileMenu.Append(1, loc('menu.file.openbeedir.name')+"\tCtrl-B", loc('menu.file.openbeedir.description') )
		syncGamesItem = self.fileMenu.Append(2, loc('menu.file.syncgames.name'), loc('menu.file.syncgames.description') )
		exitItem = self.fileMenu.Append(3, loc('menu.file.exit.name'), loc('menu.file.exit.description') )

		# options menu bar
		self.optionsMenu = wx.Menu()
		settingsItem = self.optionsMenu.Append(4, loc('menu.options.settings.name')+'\tCtrl-S', loc('menu.options.settings.description') )
		toggleLogWindowItem = self.optionsMenu.Append(5, loc('menu.options.logtoggle.name')+'\tCtrl-L', loc('menu.options.logtoggle.description') )
		reloadPluginsItem = self.optionsMenu.Append(6, loc('menu.options.reloadplugins.name'), loc('menu.options.reloadplugins.description') )
		reloadPackagesItem = self.optionsMenu.Append(7, loc('menu.options.reloadpackages.name'), loc('menu.options.reloadpackages.description') )

		# portal 2 menu bar
		self.portalMenu = wx.Menu()
		verifyGameFilesItem = self.portalMenu.Append(8, loc('menu.portal.vgf.name'), loc('menu.portal.vgf.description') )
		uninstallBeeItem = self.portalMenu.Append(9, loc('menu.portal.uninstallbee.name'), loc('menu.portal.uninstallbee.description') )
		installBeeItem = self.portalMenu.Append(10, loc('menu.portal.installbee.name'), loc('menu.portal.installbee.description') )
		openP2Item = self.portalMenu.Append( 11, loc( 'menu.portal.openp2.name' ), loc( 'menu.portal.openp2.description' ) )
		openBeeItem = self.portalMenu.Append( 12, loc( 'menu.portal.openbee.name' ), loc( 'menu.portal.openbee.description' ) )

		# help menu bar
		self.helpMenu = wx.Menu()
		aboutItem = self.helpMenu.Append(13, loc('menu.help.about.name'), loc('menu.help.about.description') )
		checkUpdatesItem = self.helpMenu.Append(14, loc('menu.help.cupdates.name'), loc('menu.help.cupdates.description') )
		wikiItem = self.helpMenu.Append(15, loc('menu.help.wiki.name'), loc('menu.help.wiki.description') )
		githubItem = self.helpMenu.Append(16, loc('menu.help.github.name'), loc('menu.help.github.description') )
		discordItem = self.helpMenu.Append(17, loc('menu.help.discord.name'), loc('menu.help.discord.description') )

		# set menu item icons
		self.helpMenu.FindItemById(13).SetBitmap( wx.Bitmap(f'{config.assetsPath}icons/menu_bm.png') )
		self.helpMenu.FindItemById(15).SetBitmap( wx.Bitmap(f'{config.assetsPath}icons/menu_github.png') )
		self.helpMenu.FindItemById(16).SetBitmap( wx.Bitmap(f'{config.assetsPath}icons/menu_github.png') )
		self.helpMenu.FindItemById(17).SetBitmap( wx.Bitmap(f'{config.assetsPath}icons/menu_discord.png') )

		# makes the menu bar
		self.menuBar = wx.MenuBar()
		self.menuBar.Append(self.fileMenu, loc('menu.file.name') )
		self.menuBar.Append(self.optionsMenu, loc('menu.options.name') )
		self.menuBar.Append(self.portalMenu, loc('menu.portal.name') )
		self.menuBar.Append(self.helpMenu, loc('menu.help.name') )

		# Give the menu bar to the frame
		self.SetMenuBar(self.menuBar)
		self.CreateStatusBar()
		self.SetStatusText( loc('statusbar.text').replace('{username}', config.steamUsername() ) )

		# file menu
		self.Bind( wx.EVT_MENU, self.openp2dir, openPortalDirItem )
		self.Bind( wx.EVT_MENU, self.openBEEdir, openBeeDirItem )
		self.Bind( wx.EVT_MENU, self.syncGames, syncGamesItem )
		self.Bind( wx.EVT_MENU, self.exit, exitItem )
		# options menu
		self.Bind( wx.EVT_MENU, self.openSettingsWindow, settingsItem )
		self.Bind( wx.EVT_MENU, logWindow.toggleVisibility, toggleLogWindowItem )
		self.Bind( wx.EVT_MENU, self.reloadPlugins, reloadPluginsItem )
		self.Bind( wx.EVT_MENU, self.reloadPackages, reloadPackagesItem )
		# portal 2 menu
		self.Bind( wx.EVT_MENU, self.verifyGameFiles, verifyGameFilesItem )
		self.Bind( wx.EVT_MENU, self.uninstallBee, uninstallBeeItem )
		self.Bind( wx.EVT_MENU, self.installBee, installBeeItem )
		self.Bind( wx.EVT_MENU, self.openP2, openP2Item )
		self.Bind( wx.EVT_MENU, self.openBee, openBeeItem )
		# help menu
		self.Bind( wx.EVT_MENU, self.openAboutWindow, aboutItem )
		self.Bind( wx.EVT_MENU, self.checkUpdates, checkUpdatesItem )
		self.Bind( wx.EVT_MENU, self.openWiki, wikiItem )
		self.Bind( wx.EVT_MENU, self.openGithub, githubItem )
		self.Bind( wx.EVT_MENU, self.openDiscord, discordItem )
		# other events
		self.Bind(wx.EVT_CLOSE, self.OnClose, self)
		self.Bind( wx.EVT_SIZING, self.OnResize, self )
		if config.load('beePath') is None:
			self.portalMenu.Enable(9, False)
			self.fileMenu.Enable(1, False)
		else:
			self.portalMenu.Enable(10, False)
		# register event handlers
		dispatcher.connect( receiver=self.RemoveMenu, signal=Events.UnregisterMenu )
		# trigger the registerMenu event
		dispatcher.send( Events.RegisterEvent, RegisterHandler=pluginSystem.RegisterHandler() )
		"""
		A notebook is a controller which manages multiple windows with associated tabs.
		This section makes the notebook
		"""
		self.book = wx.Notebook(
			self,
			name="Main Menu",
			size=wx.Size( self.GetSize().GetWidth(), self.GetSize().GetHeight() )
		)
		self.browserTab = PackageBrowserPage(self.book)
		self.book.AddPage(self.browserTab, "Package Browser")

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
		LOGGER.debug(f'saved main window position: {pos}')
		config.save(pos, 'mainWindowPos')
		config.save(None, 'placeholderForSaving')
		self.Destroy()

	def OnResize( self, evt: wx.Event ):
		"""
		called when resizing the window, this permits to internal windows to resize aswell
		:param evt: placeholder
		"""
		self.book.SetSize( self.GetSize() )

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

		if utilities.env == 'dev':
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
		"""
		reloads the plugins
		:param evt: placeholder
		"""
		asyncio.run( pluginSystem.systemObj.reload('all') )

	def reloadPackages(self, evt: wx.CommandEvent):
		"""
		reloads the package view
		:param evt: placeholder
		"""
		self.browserTab.reload()
		self.book.Refresh()
		self.Update()
		self.Refresh()

	# portal 2 items actions
	def verifyGameFiles(self, evt: wx.CommandEvent):
		"""
		triggers the verify game cache dialog + event
		:param evt: placeholder
		"""
		if not config.load("showVerifyDialog"):
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
				config.save(False, 'showVerifyDialog')
			if choice == wx.ID_NO:
				return
		# yes he wants to
		print('YES')

	def uninstallBee(self, evt: wx.CommandEvent):
		"""
		called when the uninstall bee button is pressed
		:param evt: placeholder
		"""
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
		self.portalMenu.Enable(10, True)
		self.portalMenu.Enable(9, False)
		self.fileMenu.Enable(1, False)

	def installBee(self, evt: wx.CommandEvent):
		"""
		called when the install bee button is pressed
		:param evt: placeholder
		"""
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
			config.save(str(path.resolve()).replace(r'\\', '/'), 'beePath')
			# install BEE without messages
			beeManager.checkAndInstallUpdate(True)
		self.portalMenu.Enable(9, True)
		self.portalMenu.Enable(10, False)
		self.fileMenu.Enable(1, True)

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
	def openAboutWindow(self, evt: wx.CommandEvent):
		aboutWindow.init()

	@staticmethod
	def checkUpdates(evt: wx.CommandEvent):
		asyncio.run(appDateCheck())

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
		:param menu: the menu obejct
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
	"""
	Checks app updates
	"""
	if not utilities.isonline():  # if we're not online return false
		return False
	data = utilities.checkUpdate( 'https://github.com/ENDERZOMBI102/BEE-manipulator', config.version )
	if data.url is None:
		return
	data = wx.GenericMessageDialog(
		parent=root.instance,
		message=f'An update for the app is available, do you want to update now?\n\n{data.description}',
		caption=f'Update Available - new version: {data.version}',
		style=wx.YES_NO | wx.ICON_WARNING | wx.STAY_ON_TOP | wx.NO_DEFAULT
	)
	if data.ShowModal() == wx.ID_NO:
		return  # user don't want to update
	utilities.update()


class PackageBrowserPage(wx.Window):

	loadingGif: wx.adv.AnimationCtrl
	browserObj: browser.Browser

	def __init__(self, master: wx.Notebook):
		super().__init__(
			parent=master
		)
		self.browserObj = browser.Browser(self)

	def reload(self):
		"""
		reloads the browser window by creating a new object
		"""
		if utilities.env == 'dev':
			try:
				importlib.reload(browser)
			except:
				pass
		self.browserObj = browser.Browser
