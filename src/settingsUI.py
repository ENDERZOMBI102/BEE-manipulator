import wx

from srctools.logger import get_logger

logger = get_logger()


class window(wx.PreferencesEditor):
    r"""
        this is the window for the settings
    """

    def __init__(self):
        logger.debug('initializing settings window..')
        super().__init__()
        self.AddPage(GeneralPage())
        logger.debug('settings window initialized!')

    def show(self):
        self.Show(wx.GetTopLevelWindows()[0])


class GeneralPage(wx.PreferencesPage):
    """
    see
    - https://github.com/domdfcoding/GunShotMatch/blob/master/GuiV2/GSMatch2_Core/GUI/settings_panel.py
    - https://github.com/domdfcoding/GunShotMatch/blob/master/GuiV2/GSMatch2_Core/Old/Preferences.py
    - https://docs.wxpython.org/wx.PreferencesEditor.html?highlight=addpage#wx.PreferencesEditor.AddPage
    """
    def GetName(self):
        return 'General'

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        panel.SetMinSize( (600, 300) )

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(
            wx.StaticText(panel, -1, "general page"),
                  wx.SizerFlags(1).TripleBorder())
        panel.SetSizer(sizer)
        return panel


if __name__ == '__main__':
    app = wx.App()
    settings = window()
    settings.show()
    app.MainLoop()
