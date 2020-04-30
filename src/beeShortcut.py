from requests import get
from PIL import Image
from beeManager import *
import config
import subprocess

"""
this script is responsible for the bee2 shortcut, if the online repo has updates,
launching from this will cause the updater to be launched, and install the update.
launching from this cause the ucpUpdater to be launched too, and check if the database
have some updated packages.

this will be a 'standalone' executable
"""
class bee2UpdaterShortcut(tk.Tk):
    def __init__(self):
        pass
        

if __name__ == "__main__":
    pass