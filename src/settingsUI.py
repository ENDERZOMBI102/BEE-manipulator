import wx

from srctools.logger import get_logger

logger = get_logger()
"""
   see
   - https://github.com/domdfcoding/GunShotMatch/blob/master/GuiV2/GSMatch2_Core/GUI/settings_panel.py
   - https://github.com/domdfcoding/GunShotMatch/blob/master/GuiV2/GSMatch2_Core/Old/Preferences.py
   - https://docs.wxpython.org/wx.PreferencesEditor.html?highlight=addpage#wx.PreferencesEditor.AddPage
"""


class window(wx.PreferencesEditor):
    r"""
        this is the window for the settings
    """

    def __init__(self):
        logger.debug('initializing settings window..')
        super().__init__(title='Settings')
        self.AddPage(GeneralPage())
        self.AddPage(PathsPage())
        self.AddPage(AdvPage())
        logger.debug('settings window initialized!')

    def show(self):
        self.Show(wx.GetTopLevelWindows()[0])


class GeneralPage(wx.PreferencesPage):

    def GetName(self):
        return 'General'

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        panel.SetMinSize((600, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(
            wx.StaticText(panel, -1, "General Settings"),
            wx.SizerFlags(1).Center()
        )

        s0 = wx.BoxSizer()
        #self._s0_disable_verify_dialog_text = wx.StaticText

        panel.SetSizer(sizer)
        return panel


class PathsPage(wx.PreferencesPage):
    def __init__(self):
        super().__init__()

    def GetName(self):
        return "Paths"

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        panel.SetMinSize((600, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(
            wx.StaticText(panel, -1, "Paths Settings"),
            wx.SizerFlags(1).Center()
        )
        panel.SetSizer(sizer)
        return panel


class AdvPage(wx.PreferencesPage):

    def __init__(self):
        super().__init__()

    def GetName(self):
        return "Advanced"

    def CreateWindow(self, parent):
        panel = wx.Panel(parent)
        panel.SetMinSize((600, 300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(
            wx.StaticText(panel, -1, "Advanced Settings"),
            wx.SizerFlags(1).Center()
        )
        panel.SetSizer(sizer)
        return panel


if __name__ == '__main__':
    app = wx.App()
    settings = window()
    settings.show()
    app.MainLoop()
