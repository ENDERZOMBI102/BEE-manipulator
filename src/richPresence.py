import pypresence
import config
import time
import wx
import asyncio
import servepy
import requests
from srctools.logger import get_logger

logger = get_logger()


class richPresence:
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

	def __init__(self, token: str, oauth: str=None):
		self.rpc = pypresence.Presence(token)
		self.rpc.connect()

	def update(self, **kwargs):
		# cycle in the args
		for key, value in kwargs.items():
			if key not in self.lastUpdate.keys():
				continue  # update the value only if it exist in the lastUpdate dict
			self.lastUpdate[key] = value
		#
		self.rpc.update(
			start = self.lastUpdate['start'],
			state = self.lastUpdate['state'],
			details = self.lastUpdate['details'],
			large_image = self.lastUpdate['largeImage'],
			large_text = self.lastUpdate['largeText'],
			small_image = self.lastUpdate['smallImage'],
			small_text = self.lastUpdate['smallText']
		)

	def close(self):
		self.rpc.close()




if __name__=='__main__':
	import asyncio
	r = richPresence(config.discordToken)
	r.update()

	while True:
		eval(input('>'))
