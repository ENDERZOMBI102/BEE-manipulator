from requests import *
from subprocess import *
from zipfile import *
from threading import Thread
from sys import platform
from config import config
from bases import web
import io

os=platform

class beeManager(Thread):
	
	def checkUpdates():#return true if an update is available, false if there isn't or the pc is offline
		if(web.isonline==True):
			latestjson = get('https://api.github.com/repos/BEEmod/BEE2.4/releases/latest').json()
			onlineVersion=latestjson['tag_name']
			currentVersion = config.load('beeVersion')
			if(currentVersion < onlineVersion):#check if online is present a newer version
				return True
			elif(latestjson["draft"]=="true"):
				return False
			elif(latestjson["prerelease"]=="true" and config.load("enablePrereleases")=="true"):
				return True
			else:
				return False
		else:
			return False

	def update():
		"""
		this will update BEE, when called, the function
		will download the latest version based on the
		os is running on and unzip it
		"""
		# get the os, (macos, win32, linux)
		os = platform
		# get the json data
		data = get('https://api.github.com/repos/BEEmod/BEE2.4/releases/latest').json()
		# check the os for know witch one download
		if os == "win32":
			url = data['assets'][1]['browser_download_url']
		else:
			url = data['assets'][0]['browser_download_url']
		z = ZipFile(io.BytesIO(r.content))
		z.extractall("BEE2")
		data = get('https://api.github.com/repos/BEEmod/BEE2-items/releases/latest').json()
		d_url = data['assets'][0]['browser_download_url']
		data = get(d_url)	
		z = ZipFile(io.BytesIO(r.content))
		z.extractall("BEE2")

	def startBee():
		"""
		Use this to start BEE2
		this is dynamic, call a exec if is on 
		windows and another one if is on MacOS
		"""
		if os == "win32":
		    call(['.\BEE2.exe', ''])
		else:
 		   call(['.\BEE2', ''])
