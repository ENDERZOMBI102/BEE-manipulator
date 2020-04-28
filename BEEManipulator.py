from uiWX import root
import srctools.logger
import config
from utilities import startTime, argv as argvUT
import wx
import logging
import time
from sys import argv as argv

# to start without entering the venv shell
# pipenv run py BEEManipulator.py
# to enter the venv shell
# %userprofile%/Documents/GitHub/BEE-manipulator/.venv/Scripts/activate.bat
# to start with venv shell
# py BEEManipulator.py


argvUT = argv
startTime = int(time.time())
app = wx.App()

srctools.logger.init_logging("./logs/latest.log")
LOGGER = srctools.logger.get_logger('BEE Manipulator')
try:
      LOGGER.debug("setting application name..")
      app.SetAppName("BEE Manipulator")
      app.SetAppDisplayName("BEE Manipulator")
      LOGGER.debug("successfully setted app name")
except:
      LOGGER.debug("Can't set app name!")
LOGGER.info('Checking config file..')
if config.check():
      LOGGER.info('Valid config file found!')
else:
      LOGGER.error('Invalid or inesistent config file detected!')
      LOGGER.info('Creating new config file...')
      config.createConfig()
      LOGGER.info('Config file created!')
LOGGER.info(f'Starting BEE Manipulator v{config.version()}!')
LOGGER.info('started ui!') 
# start the ui + main loop
root = root()
root.Show()
app.SetTopWindow(root)
app.MainLoop()
