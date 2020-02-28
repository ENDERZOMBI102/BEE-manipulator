from config import *
from utilities import tkRoot
import tkinter as tk
import tkinter.ttk as ttk

class logWindow(tk.Toplevel):
      def __init__(self):
            pass
      def start(self):
            super().__init__(tkRoot, name='logs')
            self.widgetName = 'Log Window'
      