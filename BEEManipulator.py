import srctools.logger
import config
from utilities import argv as argvUT
import wx
from uiWX import root
import logging
from sys import argv as argv

# pipenv run py BEEManipulator.py


argvUT = argv
app = wx.App()

srctools.logger.init_logging("./logs/latest.log")
LOGGER = srctools.logger.get_logger('BEE Manipulator')
try:
      LOGGER.debug("setting application name..")
      app.SetAppName("BEE Manipulator")
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
app.MainLoop()
