from tkinter import *  # ui library
from tkinter import ttk  # themed ui components that match the OS

class logger:
    def __init__(self):
        log_text=""
        debug_color="gray"
        info_color="black"
        warning_color="orange"
        error_color="red"
        enable_debug=False


    def log(self):
        