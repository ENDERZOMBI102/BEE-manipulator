import tkinter as tk
from tkinter import ttk

class logger(tk.Tk):
	r"""
	the logger class,nothing special.
	"""
	def __init__(self):
		super().__init__()
		self.title("BEE Manipulator log")
		self.geometry("400x600")
		
		# the log box
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		logBox = tk.Text(self, name='text_box', width=50, height=15)
		logBox.grid(row=0, column=0, sticky='NSEW')
		#frame to hold the clear button
		button_zone = ttk.Frame(self, name='button_zone')
		button_zone.grid(row=1, column=0, columnspan=2, sticky='EW')
		# clear button
		ttk.Button(button_zone, name='clear_btn', text='Clear', command=self.btn_clear).grid(row=0,column=1)
		
	
	def log(self, txt):
		self.text.append(txt)
		
	def btn_clear(self):
		"""clear the console."""
		self.logBox

		
if __name__ == "__main__":
	main = logger()
	main.mainloop()