import config
import wx
from srctools.logger import get_logger

logger = get_logger()


class settingsWindow(wx.Frame):
    r"""
        this is the window for the settings
    """

    def __init__(self, master=None):
        logger.debug('initializing settings window..')
        super().__init__(master, name='Settings', title='Settings')
        sizer = wx.FlexGridSizer(10, 0, 0)
        # log window level
        logLevelTextEntry = wx.TextEntry()
        logLevelTextEntry.SetValue('Log window level: ')
        # TODO: finish this with setting entry templates
        #
        self.SetSizer(sizer)
        logger.debug('settings window initialized!')


class settingEntry:

    def __init__(self, label: str, type: int, **kwargs):
        # TODO: implement entry "template" class
        pass

#


if __name__ == '__main__':
    app = wx.App()
    settings = settingsWindow()
    settings.Show()
    app.MainLoop()