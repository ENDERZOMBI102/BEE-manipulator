import tkinter as tkinter
import tkinter.ttk as ttk

class window(tk.Toplevel):
      r"""
      a simple class to create windows
      """
      def __init__(self, master, name=str, geometry=str):
            super().__init__(master)
            self.winfo_toplevel().title(name)
            self.winfo_toplevel().geometry(geometry)
