import srctools.logger
import config
from utilities import argv as argvUT
import wx
from uiWX import root
import logging
from sys import argv as argv

# py BEEManipulator.py

argvUT = argv

srctools.logger.init_logging("./logs/latest.log")
LOGGER = srctools.logger.get_logger('BEE Manipulator')

LOGGER.info('Checking config file..')
if config.check():
      LOGGER.info('Valid config file found!')
else:
      LOGGER.error('Invalid or inesistent config file detected! Creating new one..')
      config.createConfig()
      LOGGER.info('Config file created!')
LOGGER.info(f'Starting BEE Manipulator v{config.version()}!')
LOGGER.info('started ui!')
app = wx.App()
root = root()
root.Show()
app.MainLoop()
