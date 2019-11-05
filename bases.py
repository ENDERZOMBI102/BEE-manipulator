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

	def installUpdates():
		print("")

class package():
	#this class rappresents a package, with all infos
	def __init__(self):
		name = ""
		repo_url = ""
		author = ""
		co_author = "Null"
		version = ""
		icon = ""
		direct_download = False
		api_latest_url = ""
