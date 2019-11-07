import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from config import *

class root(tk.Tk):
      def __init__(self):
            super().__init__()
            self.title("BEE Manipulator "+str(config.load("appVersion")))
            self.geometry("500x400")

            #the main container
            self.notebook = Notebook(self)

            #create all the tabs
            updater_tab = tk.Frame(self.notebook)
            app_tab = tk.Frame(self.notebook)
            settings_tab = tk.Frame(self.notebook)
            BEE_tab = tk.Frame(self.notebook)
            package_browser_tab = tk.Frame(self.notebook)

            coming_soon_label = tk.Label(package_browser_tab, text="Coming Soon")
            coming_soon_label.pack()

            self.notebook.add(app_tab, text="App")
            self.notebook.add(updater_tab, text="BEE")
            self.notebook.add(package_browser_tab, text="package Browser")
            self.notebook.add(settings_tab, text="settings")

            self.notebook.pack(fill=tk.BOTH, expand=1)
if __name__=="__main__":
      root = root()
      root.mainloop()
