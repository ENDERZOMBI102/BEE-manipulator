import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from config import *
from bases import web


class updateui(tk.Tk):

      def __init__(self):
            super.__init__()
            if(web.isonline == False):
                  self.root.destroy()
            ov = get('https://api.github.com/repos/ENDERZOMBI102/BEE-manipulator/releases/latest').json()
            if(not config.load('appVersion') >= ov['tag_name']):
                  return True
            else:
                  return False
