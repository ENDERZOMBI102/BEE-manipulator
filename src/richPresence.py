import pypresence
import config
import time
import asyncio
import discord
import struct
from srctools.logger import get_logger

logger = get_logger()
richPresence: pypresence.Presence = None
lastUpdate: dict = {"start": int(time.time()), "state": None, "details": None, "spectate": None}

async def rich():
      rpc = pypresence.Presence(config.discordToken)
      while True:
            try:
                  rpc.connect()
                  break
            except:
                  logger.warning(r"can't connect to discord, retry in 20s")
                  await asyncio.sleep(20)
      

      update({})


async def loadPalette():
      richPresence.update()

def update(updateData: dict):
      for key, data in updateData:
            lastUpdate[key] = data
      



def init():
      asyncio.run(rich())


      
if __name__ == "__main__":
      init()
