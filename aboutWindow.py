import wx
import wx.html2
from markdown2 import markdown
import webbrowser as wb
import config
from requests import get
from srctools.logger import get_logger



def init(master):
    window=wx.html2.WebView
    logger = get_logger()
    logger.debug('opening about.md..')
    try:
        with open('./assets/about.md', 'r') as file:
            text: str = file.read(len(file))
    except:
        return
    html = markdown(text.replace(r'{0}', config.version()))
    window.setPage(html=html)
    window.SetHTMLBackgroundColour(wx.Colour(50, 168, 160))
