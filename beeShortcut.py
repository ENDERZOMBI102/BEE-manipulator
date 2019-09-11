from bases import web
from beeManager import beeManager
from config import config
import subprocess

"""
this script is responsible for the bee2 shortcut, if the online repo has updates,
launching from this will cause the updater to be launched, and install the update.
launching from this cause the ucpUpdater to be launched too, and check if the database
have some updated packages.

this will be a 'standalone' executable
"""
if(beeManager.checkUpdates()==True)
    print("an update for BEE2 is available, update now?")
    if(input() in {"yes", "y", "YES", "Y"})
        print("updating BEE2...")
        beeManager.
subprocess.call(executable=config.load("p2path"),timeout=1)
exit()