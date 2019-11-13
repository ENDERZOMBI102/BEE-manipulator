import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook, Progressbar as pbar
from requests import get
from config import *
from bases import web


class updateui(tk.Tk):

      def __init__(self):
            super().__init__()
            self.geometry("240x100")
            self.title("BM Updater")
            # create the loading bar
            self.loading_bar = pbar(self)
            self.loading_bar.start(interval=8)
            self.loading_bar.pack()
            # check updates
            if(web.isonline == False):
                  self.root.destroy()
            ov = get('https://api.github.com/repos/ENDERZOMBI102/BEE-manipulator/releases/latest').json()
            if(not config.load('appVersion') >= ov['tag_name']):
                  print("")
                  
if __name__ == "__main__":
      updateui = updateui()
      updateui.mainloop()
