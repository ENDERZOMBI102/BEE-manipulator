import pypresence
import config
import time
import asyncio
from srctools.logger import get_logger

logger = get_logger()

async def rich():
      rpc = pypresence.Presence()

# Python 3.7+
def init():
      asyncio.run(rich())


      
if __name__ == "__main__":
      init()
