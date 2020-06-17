from sys import argv

import wx

import config
import srctools.logger
from uiWX import root

# to start without entering the venv shell
# pipenv run py BEEManipulator.py
# to enter the venv shell
# "C:\Users\Flavia\.virtualenvs\BEE-manipulator-xMPheCny\Scripts\activate.bat"
# to start with venv shell
# py BEEManipulator.py

# some data initialization
app = wx.App()

srctools.logger.init_logging("./logs/latest.log")
LOGGER = srctools.logger.get_logger('BEE Manipulator')
# if we started with --dev parameter, set loglevel to debug
try:
    if '--dev' in argv:
        config.overwrite('logLevel', 'DEBUG')
        config.overwrite('logWindowVisibility', True)
        env = 'dev'
except: pass
# app init
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
LOGGER.info('starting ui!')
# start the ui + main loop
root = root()
root.Show()
app.SetTopWindow(root)
app.MainLoop()
