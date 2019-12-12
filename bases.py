import http.client as httplib
from requests import *
from threading import Thread
from config import config


class web:
	
	def isonline():
	  conn = httplib.HTTPConnection("www.google.com", timeout=5)
	  try:
		  conn.request("HEAD", "/")
		  conn.close()
		  return True
	  except:
		  conn.close()
		  return False
		  
		  
	def checkUpdates():
		if(web.isonline==False):
			return False
		ov=get('https://api.github.com/repos/ENDERZOMBI102/BEE-manipulator/releases/latest').json()
		if(not config.load('appVersion')>=ov['tag_name']):
			return True
		else:
			return False

	def installUpdates():
		print("")

class package():
	#this class rappresents a package, with all infos
	def __init__(self):
		self.name = ""
		self.repo_url = ""
		self.author = ""
		self.co_author = "Null"
		self.version = ""
		self.icon = ""
		self.direct_download = False
		self.api_latest_url = ""
