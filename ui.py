import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from config import *
# import all the tabs
from updateui import updateui
from compilerFailHandler import compilerFailHandler

class root(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("BEE Manipulator v"+str(config.load("appVersion")))
		self.geometry("600x500")
		#the main container
		self.notebook=Notebook(self)
		#create all the tabs
		BEE_tab = compilerFailHandler(self)
		updater_tab = updateui(self)
		app_tab = tk.Frame(self.notebook)
		settings_tab = tk.Frame(self.notebook)
		#BEE_tab = tk.Frame(self.notebook)
		package_browser_tab = tk.Frame(self.notebook)
		about_tab = tk.Frame(self.notebook)
		#
		coming_soon_label = tk.Label(package_browser_tab,text="Coming Soon")
		coming_soon_label.pack()
		#
		self.notebook.add(app_tab, text="App")
		self.notebook.add(BEE_tab, text="BEE")
		self.notebook.add(updater_tab, text="Update")
		self.notebook.add(package_browser_tab, text="Package Browser")
		self.notebook.add(settings_tab, text="Settings")
		self.notebook.add(about_tab, text="About")
		#
		self.notebook.pack(fill=tk.BOTH, expand=1)
	#
if __name__=="__main__":
	root=root()
	root.mainloop()
