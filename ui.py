import tkinter as tk

class root(tk.Tk):
      def __init__(self):
            super().__init__()
            version = 3
            self.title("BEE Manipulator "+str(version))
            self.geometry("500x400")

if __name__=="__main__":
      root = root()
      root.mainloop()