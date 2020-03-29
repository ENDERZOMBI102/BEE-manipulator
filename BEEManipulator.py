import srctools.logger
import config
from logWindow import logWindow
from utilities import tkRoot
from ui import root

LOGGER = srctools.logger.get_logger('BEE Manipulator')
LOGGER.info('Starting BEE Manipulator!')
LOGGER.info('Checking config file..')
try:
      config.check()
      LOGGER.info('Valid config file found!')
except:
      LOGGER.error('Invalid config file detected! Creating new one..')
      config.create_config()
      LOGGER.info('Config file created!')
LOGGER.info('Initilizing UI!')
LOGGER.debug('Creating root object..')
tkRoot = root()
LOGGER.debug('Created root object!')
LOGGER.info('Starting log window..')
logWin = logWindow()
logWin.start()
LOGGER.info('Log window started!')
tkRoot.mainloop()
