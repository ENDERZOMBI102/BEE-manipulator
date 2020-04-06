import wx
import config
import os
import webbrowser as wb
import logWindow
from srctools.logger import get_logger


class root (wx.Frame):
    
    def __init__(self):
        super().__init__(None, title="BEE Manipulator "+str(config.version()))

        # init logging and the logging window
        logWindow.init(self)
        self.CenterOnScreen()
        self.LOGGER = get_logger()
        
        """
        A menu bar is composed of menus, which are composed of menu items.
        This section builds the menu bar and binds actions to them
        """
        # file menu bar
        self.fileMenu = wx.Menu()
        openPortalDirItem = self.fileMenu.Append(0, "Open Portal 2 Directory\tCtrl-P"," ")
        openBeeDirItem = self.fileMenu.Append(1, "Open BEEmod Directory\tCtrl-B", " ")
        syncGamesItem = self.fileMenu.Append(2, "Sync Games", " ")
        exitItem = self.fileMenu.Append(3, "Exit", " ")

        # options menu bar
        self.optionsMenu = wx.Menu()
        settingsItem = self.optionsMenu.Append(4, "Settings\tCtrl-S", " ")
        toggleLogWindowItem = self.optionsMenu.Append(5, "Toggle Log Window\tCtrl-L", " ")
        reloadConfigItem = self.optionsMenu.Append(6, "Reload Configs (Restart)", " ")
        reloadPackagesItem  = self.optionsMenu.Append(7, "Reload Packages", " ")

        # portal 2 menu bar
        self.portalMenu = wx.Menu()
        verifyGameCacheItem = self.portalMenu.Append(8, "Verify Game Cache", " ")
        uninstallBeeItem = self.portalMenu.Append(9, "Uninstall BEE 2.4", " ")
        installBeeItem = self.portalMenu.Append(10, "Install BEE 2.4", " ")

        # help menu bar
        self.helpMenu = wx.Menu()
        aboutItem = self.helpMenu.Append(11, "About BEE Manipulator", " ")
        checkUpdatesItem = self.helpMenu.Append(12, "Check Updates", " ")
        wikiItem = self.helpMenu.Append(13, "Wiki", " ")
        githubItem = self.helpMenu.Append(14, "Github", " ")
        discordItem = self.helpMenu.Append(15, "Discord", " ")

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
        
        """
        A notebook is a controller which manages multiple windows with associated tabs.
        This section makes the notebook
        """
        self.book = wx.Notebook(self, name="Main Menu")
        browserTab = wx.Window(self.book)
        self.book.AddPage(browserTab, "Package Browser")





    # file menu items actions
    def openp2dir(self, event):
        os.startfile(config.portalDir())

    def openBEEdir(self, event):
        if(config.load("beePath") is None):
            pass
        else:
            pass

    def syncGames(self, event):
        self.LOGGER.info("hi")
        pass

    def exit(self, event):
        self.DestroyChildren()
        self.Destroy()

    # options menu items actions
    def openSettingsWindow(self, event):
        pass
        

    def reloadConfig(self, event):
        pass

    def reloadPackages(self, event):
        pass

    # portal 2 items actions
    def verifyGameCache(self, event):
        pass

    def uninstallBee(self, event):
        pass

    def installBee(self, event):
        pass

    # help menu items actions
    def openAboutWindow(self, event):
        pass

    def checkUpdates(self, event, window=True):
        # if there's an update open a popup, if not open another popup (if window = true)
        pass

    def openWiki(self, event):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/wiki")

    def openGithub(self, event):
        wb.open("https://github.com/ENDERZOMBI102/BEE-manipulator/")

    def openDiscord(self, event):
        wb.open("https://discord.gg/hnGFJrz")


if __name__ == "__main__":
    app = wx.App()
    root = root()
    root.Show()
    app.MainLoop()
