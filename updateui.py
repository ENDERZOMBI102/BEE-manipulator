import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from config import *
#from bases import web

class updateui(tk.Frame):
	"""
	the update tab inside the app.
	this will manage the update ui
	"""
	def __init__(self, baseClass):
		# create the frame on the main class
		super().__init__(baseClass.notebook)
		
		
				