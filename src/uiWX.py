import asyncio
import os
import webbrowser as wb
from pathlib import Path

import wx

import aboutWindow
import beeManager
import browser
import config
import logWindow
import settingsUI
import utilities
from srctools.logger import get_logger, init_logging

LOGGER = get_logger()


class root (wx.Frame):

    settingsWindowInstance: settingsUI.window = None
    
    def __init__(self):
        super().__init__( None, title="BEE Manipulator "+str( config.version() ) )
        # sets the app icon
        self.SetIcon( wx.Icon(f'{config.assetsPath}icon.ico') )
        # init the logging window
        asyncio.run( logWindow.init() )
        asyncio.run( appDateCheck() )
        # set the utilities.root pointer to the object of this class
        utilities.root = self
        try:
            self.SetPosition(wx.Point(config.load('mainWindowPos')))
        except:
            self.CenterOnScreen()
        self.SetSize(width=600, height=500)
        LOGGER.info(f'internet connected: {utilities.isonline()}')
        """
        A menu bar is composed of menus, which are composed of menu items.
        This section builds the menu bar and binds actions to them
        """
        # file menu bar
        self.fileMenu = wx.Menu()
        openPortalDirItem = self.fileMenu.Append(0, "Open Portal 2 Directory\tCtrl-P","opens the portal 2 directory")
        openBeeDirItem = self.fileMenu.Append(1, "Open BEEmod Directory\tCtrl-B", "opens the BEEmod directory")
        syncGamesItem = self.fileMenu.Append(2, "Sync Games", " ")
        exitItem = self.fileMenu.Append(3, "Exit", " ")

        # options menu bar
        self.optionsMenu = wx.Menu()
        settingsItem = self.optionsMenu.Append(4, "Settings\tCtrl-S", "opens the settings window")
        toggleLogWindowItem = self.optionsMenu.Append(5, "Toggle Log Window\tCtrl-L", "toggle the log window visibility")
        reloadConfigItem = self.optionsMenu.Append(6, "Reload Configs (Restart)", "reload some configs")
        reloadPackagesItem  = self.optionsMenu.Append(7, "Reload Packages", "reload packages")

        # portal 2 menu bar
        self.portalMenu = wx.Menu()
        verifyGameCacheItem = self.portalMenu.Append(8, "Verify Game Cache", " ")
        uninstallBeeItem = self.portalMenu.Append(9, "Uninstall BEE 2.4", "remove BEE2 from disk")
        installBeeItem = self.portalMenu.Append(10, "Install BEE 2.4", "")

        # help menu bar
        self.helpMenu = wx.Menu()
        aboutItem = self.helpMenu.Append(11, "About BEE Manipulator", "opens the about window")
        checkUpdatesItem = self.helpMenu.Append(12, "Check Updates", "check for app updates")
        wikiItem = self.helpMenu.Append(13, "Wiki", "opens the online wiki")
        githubItem = self.helpMenu.Append(14, "Github", "opens the github page")
        discordItem = self.helpMenu.Append(15, "Discord", "invite to the BEEmod server")

        # makes the menu bar
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.fileMenu, "File")
        self.menuBar.Append(self.optionsMenu, "Options")
        self.menuBar.Append(self.portalMenu, "Portal 2")
        self.menuBar.Append(self.helpMenu, "Help")

        # Give the menu bar to the frame
        self.SetMenuBar(self.menuBar)
        self.CreateStatusBar()
        self.SetStatusText(f'Hi {config.steamUsername()}!')

        # file menu
        self.Bind(wx.EVT_MENU, self.openp2dir, openPortalDirItem)
        self.Bind(wx.EVT_MENU, self.openBEEdir,  openBeeDirItem)
        self.Bind(wx.EVT_MENU, self.syncGames, syncGamesItem)
        self.Bind(wx.EVT_MENU, self.exit, exitItem)
        # options menu
        self.Bind(wx.EVT_MENU, self.openSettingsWindow, settingsItem)
        self.Bind(wx.EVT_MENU, logWindow.toggleVisibility, toggleLogWindowItem)
        self.Bind(wx.EVT_MENU, self.reloadConfig, reloadConfigItem)
        self.Bind(wx.EVT_MENU, self.reloadPackages, reloadPackagesItem)
        # portal 2 menu
        self.Bind(wx.EVT_MENU, self.verifyGameCache, verifyGameCacheItem)
        self.Bind(wx.EVT_MENU, self.uninstallBee, uninstallBeeItem)
        self.Bind(wx.EVT_MENU, self.installBee, installBeeItem)
        # help menu
        self.Bind(wx.EVT_MENU, self.openAboutWindow, aboutItem)
        self.Bind(wx.EVT_MENU, self.checkUpdates, checkUpdatesItem)
        self.Bind(wx.EVT_MENU, self.openWiki, wikiItem)
        self.Bind(wx.EVT_MENU, self.openGithub, githubItem)
        self.Bind(wx.EVT_MENU, self.openDiscord, discordItem)
        # other events
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        if config.load('beePath') is None:
            self.portalMenu.Enable(9, False)
            self.fileMenu.Enable(1, False)
        else:
            self.portalMenu.Enable(10, False)
        
        """
        A notebook is a controller which manages multiple windows with associated tabs.
        This section makes the notebook
        """
        self.book = wx.Notebook(self, name="Main Menu")
        self.browserTab = browser.browser(self.book)
        self.book.AddPage(self.browserTab, "Package Browser")

    def OnClose(self, event: wx.CloseEvent):
        # get the window position as wx.Point and convert it to list
        try:
            pos = list(self.GetPosition().Get())
            LOGGER.debug(f'saved main window position: {pos}')
            config.save(pos, 'mainWindowPos')
        except:
            pass
        self.Destroy()

    # file menu items actions
    @staticmethod
    def openp2dir(event):
        os.startfile(config.portalDir())

    @staticmethod
    def openBEEdir(self, event):
        if config.load("beePath") is None:
            pass
        else:
            os.startfile( config.load("beePath") )

    def syncGames(self, event):
        notimplementedyet()

    def exit(self, event):
        self.OnClose( wx.CloseEvent )  # there's already an handler, so use that
    
    # options menu items actions
    def openSettingsWindow(self, event = None):
        """
        this function opens the settings window.
        when this is called for the first time create an instance of the window, so when
        called again it will be faster, because it don't have to create everything again
        :param event: wx.EVT_something
        """
        if self.settingsWindowInstance is None:  # if the window was opened once, this isn't None
            self.settingsWindowInstance = settingsUI.window()  # set it to the settings window instance
        self.settingsWindowInstance.show()  # show the window

    def reloadConfig(self, event):
        notimplementedyet()
        return
        if utilities.frozen():
            os.system('ping 127.0.0.1 100 && BEEManipulator.exe')  # can start the exe
        else:
            os.system('cmd /C "ping 127.0.0.1 100 && cd src && pipenv run py BEEManipulator.py"')  # can start the py
        self.OnClose( wx.CloseEvent )

    def reloadPackages(self, event):
        # remove the package browser window
        self.book.RemovePage(0)
        self.browserTab = browser.browser(self.book)
        self.book.AddPage(self.browserTab, "Package Browser")
        self.book.Refresh()
        self.Update()
        self.Refresh()

    # portal 2 items actions
    def verifyGameCache(self, event):
        if not config.load("noVerifyDialog"):
            dialog = wx.RichMessageDialog(
                self,
                '''This will remove EVERYTHING beemod-related from portal 2!
                click yes ONLY if you are sure!''',
                'WARNING!',
                wx.YES_NO | wx.ICON_WARNING | wx.STAY_ON_TOP | wx.NO_DEFAULT
            )
            dialog.ShowDetailedText(
                "if you don't want this dialog to show check this checkbox, but beware, this is here to protect you"
            )
            dialog.ShowCheckBox("Don't show again")
            choice = dialog.ShowModal()
            if dialog.IsCheckBoxChecked():
                config.save(True, 'noVerifyDialog')
            if choice == wx.ID_YES:
                print('yes')
            else:
                print('no')

    def uninstallBee(self, event):
        return
        print("uninstall")
        self.portalMenu.Enable(10, True)
        self.portalMenu.Enable(9, False)
        self.fileMenu.Enable(1, False)

    def installBee(self, event):
        print('install')
        dial = wx.DirDialog(
            self,
            message='Select where to install BEE (a BEE2 folder will be created)',
            # this gets the APPDATA path, go from Roaming to Local and then return the Programs folder full path
            defaultPath=str( Path( str( Path( os.getenv('appdata') ).parent.resolve() )+'/Local/Programs/').resolve() )
        )
        # show the dialog and wait
        if dial.ShowModal() == wx.ID_CANCEL:
            return  # don't want to install anymore
        path = Path( dial.GetPath() + '/BEE2/' )
        # create the missing folders
        if not path.exists():
            path.mkdir()
        # save the BEE path
        config.save(str( path.resolve() ).replace(r'\\', '/'), 'beePath')
        # install BEE without messages
        beeManager.checkAndInstallUpdate(True)
        self.portalMenu.Enable(9, True)
        self.portalMenu.Enable(10, False)
        self.fileMenu.Enable(1, True)

    # help menu items actions
    def openAboutWindow(self, event):
        aboutWindow.init(self)

    @staticmethod
    def checkUpdates(event):
        asyncio.run(appDateCheck())

    @staticmethod
    def openWiki(event):
        openUrl('https://github.com/ENDERZOMBI102/BEE-manipulator/wiki')

    @staticmethod
    def openGithub(event):
        openUrl('https://github.com/ENDERZOMBI102/BEE-manipulator')

    @staticmethod
    def openDiscord(event):
        openUrl('https://discord.gg/hnGFJrz')


def openUrl(url: str):
    LOGGER.info(f'opening "{url}" with default browser')
    wb.open(url)


def notimplementedyet():
    msg = wx.GenericMessageDialog(
        parent = wx.GetActiveWindow(),
        message = 'This feature is not yet implemented, return later!',
        caption = 'Not implemented',
        style = wx.ICON_INFORMATION | wx.STAY_ON_TOP | wx.OK
    )
    msg.ShowModal()


async def appDateCheck():
    if not ( config.checkUpdates() is True):  # update check
        return  # no updates, return
    data = wx.GenericMessageDialog(
        message = "An update for the app is avaiable, do you want to update now?)",
        caption = f'Update Avaiable - new version: {config.load("onlineVersion")}',
        style = wx.YES_NO | wx.ICON_WARNING | wx.STAY_ON_TOP | wx.NO_DEFAULT
    )
    if data.ShowModal() == wx.ID_NO:
        return  # user don't want to update
    utilities.update()
        

if __name__ == "__main__":
    init_logging("./logs/latest.log")
    LOGGER = get_logger('BEE Manipulator')
    app = wx.App()
    root = root()
    root.Show()
    app.MainLoop()
