import pypresence
import config
import time
import asyncio
import servepy
import requests
from srctools.logger import get_logger

logger = get_logger()
rpc: pypresence.Presence = None
lastUpdate: dict = {
						'start': int(time.time()),
						'state': None,
						'details': None,
						'largeImage': None,
						'largeText': None,
						'smallImage': None,
						'smallText': None
				   }

async def loadPalette():
	update({})

async def update(updateData: dict):
	for key, data in updateData:
		lastUpdate[key] = data
	logger.debug(
f'''
updating discord activity\n
- new state: {lastUpdate['state']}\n
- new details: {lastUpdate['details']}
''')# a giant log :P
	rpc.update(
				state = lastUpdate['state'],
				details = lastUpdate['details'],
				start = lastUpdate['start'],
				large_image = lastUpdate['largeImage'],
				large_text = lastUpdate['largeText'],
				small_image = lastUpdate['smallImage'],
				small_text = lastUpdate['smallText']
			  )

def simpleInit():
	logger.debug('starting "asyncio" thread for "rich presence"')
	asyncio.run(simpleRich())

async def simpleRich():  
	rpc = pypresence.Presence(config.discordToken)
	while True:
		try:
			logger.info('attempting to connect to discord..')
			await rpc.connect()
			break
		except:
			logger.warning(r"can't connect to discord, retry in 20s")
			await asyncio.sleep(20)
	logger.info('successfully connected to discord!')
	if config.devMode():
		update({'details': 'Developing new features!', 'state': 'why is UI difficult?'})
	else: update({'details': 'idle'})

if __name__ == "__main__":
	simpleInit()
	time.sleep(30)
	update({"state": "hi world!", "details": "making new features"})
