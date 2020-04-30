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
        super().__init__(master,title='About BEE Manipulator', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetIcon(wx.Icon('./assets/icon.ico'))
        self.box = wx.html.HtmlWindow(self)
        try:
            self.logger.debug('trying to load about.html..')
            open('./assets/about.html').close()
            self.box.LoadFile('./assets/about.html')
        except:
            self.logger.warning('failed to open about.html! falling back to about.md')
            self.logger.debug('opening about.md..')
            # set the page to the converted markdown text
            with open('./assets/about.md', 'r') as file:
                self.logger.debug('converting markdown to html..')
                data = markdown(file.read())
            data = data.replace(r'{0}', config.version())
            self.box.SetPage(data)
            with open('./assets/about.html', 'w') as file:
                file.write(data)
        self.CenterOnParent()
        self.Raise()
        self.Show()
        self.box.OnLinkClicked = self.linkHandler

    def linkHandler(self, link):
        wb.open(link.GetHref())

