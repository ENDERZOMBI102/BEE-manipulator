from requests import *
from subprocess import *
from zipfile import *
from threading import Thread
from sys import platform
from config import config
import json
import io

os=platform

class beeManager(Thread):
	
	def checkUpdates():#return true if an update is available, false if there isn't'
		latestjson = get('https://api.github.com/repos/BEEmod/BEE2.4/releases/latest').json()
		onlineVersion=latestjson['tag_name']
		currentVersion = config.load('beeVersion','beeVersion')
		if(currentVersion>=onlineVersion):
			return False
		else:
			return True
		

	def start(os, state,self):
		nd = 0
	checkUpdates()