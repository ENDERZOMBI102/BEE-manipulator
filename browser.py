import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from config import *
from json import *
from bases import web
from packages import *



class browser(tk.Frame):
	r"""
		the package browser, this will download the database.json file from the repo
	"""
	def __init__(self, baseClass):
		super().__init__(baseClass.notebook)
        
		