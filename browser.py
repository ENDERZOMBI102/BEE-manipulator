import tkinter as tk
from tkinter import messagebox as msg
from tkinter.ttk import *
from config import *
from json import *
from base64 import b64encode as encode
from packages import *



class browser(tk.Frame):
	r"""
		the package browser, this will download the database.json file from the repo
	"""
	def __init__(self, baseClass):
		super().__init__(baseClass)
		try:
			self.database = database()
			self.database = self.database.loadObj()
		except:
			pass


class database:
	r"""
		check, download, upload, and load the database
	"""
	def __init__(self):
		self.databasepath = "./assets/database.json"
		try:
			self.check()
		except:
			self.download()		

	def check(self):
		r"""
			check the database
		"""
		try:
			with open(self.databasepath, "r") as file:
				json.load(file)
		except:
			raise Exception
	
	def download(self):
		r"""
			download the database
		"""
		if not reconfig.isonline():
			raise ConnectionError
		try:
			with open(self.databasepath, "w") as file:
				self.databaseJSON = get("https://raw.githubusercontent.com/ENDERZOMBI102/ucpDatabase/master/Database.json").json()
		except:
			raise Exception("how did you get here?")

	def loadObj(self):
		r"""
			create the correct package object for each one of the packages in the json
		"""
		self.database = []
		for pkg in self.databaseJSON:
			# if is a BEE package load those info
			if pkg["type"] == "BEE" or pkg["type"] == "bee":
				package = beePackage()
				package.ID = pkg["ID"]
				package.author = pkg["author"]
				package.name = pkg["name"]
				package.description = pkg["desc"]
				package.coAuthors = pkg["co_author"]
				package.version = pkg["version"]
				package.url = pkg["api_latest_url"]
				# or those if is a BM package
			elif pkg["type"] == "BM" or pkg["type"] == "bm":
				package = bmPackage()
				package.ID = pkg["ID"]
				package.author = pkg["author"]
				package.name = pkg["name"]
				package.coAuthors = pkg["co_author"]
				package.desc = pkg["desc"]
				package.version = pkg["version"]
				package.url = pkg["api_latest_url"]
				package.contents = pkg["contents"]
				package.config = pkg["config"]
			# now that we have our package object, we have to verify and load some thing from the internet
			# take the file name from the api latest OR from the database if the package isn't on github 
			if package.service() == "github" and package.filename and not pkg["filename"]:
				tmp = get(package.url)
				package.filename == tmp["assets"][0]["name"]
			elif package.filename:
				package.filename == pkg["filename"]
			# obtain the icon url
			if package.service() == "github":
				iconurl = package.repo() + "raw\\master\\icon.png"
			elif pkg["icon_url"]:
				iconurl = pkg["icon_url"]
			# obtain the icon
			icon = get(iconurl)
			# convert it to base64
			package.icon64 = encode(icon)
			# check the validity of coAuthors
			if package.coAuthors in ["null", ""]
				package.coAuthors = []

