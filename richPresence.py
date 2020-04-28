import pypresence
import config
from utilities import startTime
from srctools.logger import get_logger
from time import sleep

presence = None
logger = get_logger()

class richPresence:
      global logger
      rpc: pypresence.Presence
      def __init__(self):
            logger.info('loading discord integration..')
            self.rpc = pypresence.Presence(config.discordToken)
            logger.debug('rich presence integration loaded!')
            self._connect()
            logger.info('connected to discord!')
            logger.debug('updating discord rich presence')
            self.rpc.update(start=startTime)

      def _connect(self) -> None:
            try:
                  logger.debug(f'making discord connection attempt...')
                  self.rpc.connect()
            except:
                  logger.warning("can't connect to discord! making new attempt in 20s")
                  sleep(20)
                  self._connect()

def init() -> None:
      global presence
      presence = richPresence()

def getRpc() -> pypresence.Presence:
      return presence.rpc

      
if __name__ == "__main__":
      pass
