import pypresence
import config
import time
import asyncio
import servepy
import requests
from srctools.logger import get_logger

logger = get_logger()
richPresence: pypresence.Presence = None
lastUpdate: dict = {"start": int(time.time()), "state": None, "details": None, "palette": None}
auth = None
client: pypresence.Client = None

async def rich():
      #rpc = pypresence.Presence(config.discordToken)
      client = pypresence.Client(config.discordToken)
      while True:
            try:
                  client.start()
                  break
            except:
                  logger.warning(r"can't connect to discord, retry in 20s")
                  await asyncio.sleep(20)
      logger.info('successfully connected to discord!')
      logger.info('waiting for authorization...')
      if config.load('OAuth2') == None:
            while True:
                  try:
                        logger.debug('sending RPC command "authorize"')
                        auth = client.authorize(config.discordToken, ['rpc'])
                        break
                  except:
                        asyncio.sleep(20)
            logger.info('authorization recived!')
            logger.debug('sending POST authorization code to discord servers')
            
            client.authenticate(auth['data']['code'])
      update({})


async def loadPalette():
      update()

def update(updateData: dict):
      for key, data in updateData:
            lastUpdate[key] = data
      client.set_activity(state=lastUpdate['state'],
                          details=lastUpdate['details'],
                          start=updateData['start'])

def init():
      asyncio.run(rich())

#def startEventListener():
#      app = servepy.App()
#      app.all('BMEVTHANDLER', eventListener)
#
#def eventListener(req: servepy.Request, res: servepy.Response):
#      logger.info(f'recived data on event listener: {req.body}')
#



if __name__ == "__main__":
      init()
