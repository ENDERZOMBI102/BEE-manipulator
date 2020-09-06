import os
import sys
import traceback
from pathlib import Path
from sys import argv

import wx

import config
import localization
import srctools.logger
import timeTest
import utilities

timeStartup = False
if '--time' in argv:
    timeStartup = True
    timeTest.start()

# use file dir as working dir
path = Path(__file__).resolve()
if getattr(sys, 'frozen', False):
    print(f"BM exe path: {path.parent}")
    os.chdir( path.parent )
else:
    print(f"BM source path: {path.parent}")
    os.chdir( path.parent )

# create the wx app obj
app = wx.App()


# custom unhandled exception handler for the "cool" error window
sys.excepthook = lambda etype, value, tb: \
    wx.SafeShowMessage( title='BM Error!', text=''.join( traceback.format_exception(etype, value, tb) ) )

instance = wx.SingleInstanceChecker('BM')
if instance.IsAnotherRunning():
    print('another instace of BM is running, aborting.')
    exit()


srctools.logger.init_logging("./logs/latest.log")
LOGGER = srctools.logger.get_logger('BEE Manipulator')
# if we started with --dev parameter, set loglevel to debug
if '--dev' in argv:
    config.overwrite('logLevel', 'DEBUG')
    config.overwrite('logWindowVisibility', True)
    config.overwrite('l18nFolderPath', './../langs')
    utilities.env = 'dev'
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
# start localizations
localization.Localize()
LOGGER.info(f'current lang: { loc("currentLang") }')
# create icon object
utilities.__setIcon()
# import after localize() object init so that loc() is already present
from uiWX import root
# start ui
LOGGER.info(f'Starting BEE Manipulator v{config.version()}!')
LOGGER.info('starting ui!')
# start the main loop
root = root()
root.Show()
app.SetTopWindow(root)
if timeStartup:
    timeTest.stop()
app.MainLoop()
