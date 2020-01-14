import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from config import *

class updateui(tk.Frame):
	"""
	the update tab inside the app.
	this will manage the update ui
	"""
	def __init__(self, baseClass):
		# create the frame on the main class
		super().__init__(baseClass)
		pass
		
if __name__ == "__main__":
	t = tk.Tk()
	t.title("test")
	h = Notebook(t)
	h.add(updateui(h), "text")
	h.pack()
	t.mainloop()
				