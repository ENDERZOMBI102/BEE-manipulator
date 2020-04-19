import wx
import wx.html
import wx.richtext
from markdown2 import markdown
import webbrowser as wb
import config
from requests import get
from srctools.logger import get_logger



def init(master):
    window=aboutWindow(master)
    
    
    
    
    
class aboutWindow(wx.Frame):
    #
    logger = get_logger()
    #
    def __init__(self, master):
        super().__init__(master,title='About BEE Manipulator')
        self.SetIcon(wx.Icon('./assets/icon.ico'))
        self.box = wx.html.HtmlWindow(master)
        self.logger.debug('opening about.md..')
        # set the page to the converted markdown text
        if not self.box.LoadFile('./assets/about.html'):
            self.logger.error(f'failed to read the about.html file')
            self.Destroy()
            return
        self.Show()

