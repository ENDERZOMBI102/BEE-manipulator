from config import *
from sys import platform
import tkinter as tk
from tkinter.ttk import Notebook

class compilerFailHandler(tk.Frame):
	r"""
		a crafted library used as a BEEmod 2.4's compiler fail handler,
		when fail() is called, the *latest* error log is loaded and an attempt
		to parse it is done, if done correctly, another line is appended to
		the file, "[compilerFailHandler] File parsed successufully"
	"""
	def __init__(self,baseClass):
		super().__init__(baseClass.notebook)
		
	def fail(arg = None):
		pass
				
