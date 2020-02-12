from json import *
from base64 import b64decode as decode

class beePackage:
	r"""
		rappresents a BEE2.4 package, with all its data; icon, author, file name and a description are
		stored here, with the others.
		the icon is stored as base64 string and then returned as image object when icon() is called
	"""
	def __init__(self, ID = None, icon64 = None, version = 0, author = [], description = None, url = "None", filename = None, name =  None):
		self.ID = ID
		self.author = author
		self.icon64 = icon64
		self.version = version
		self.description  = description
		self.url = url
		self.filename = filename
		self.name = name
		self.coAuthors = []
	
	r"""
		this will return the used service, for now only github, dropbox and google drive
	"""
	def service(self):
		if "github" in self.url:
			return "github"
		elif "dropbox" in self.url:
			return "dropbox"
		elif "drive.google" in self.url:
			return "gdrive"
	
	r"""
		this will return the repo link if the package is on github, if the package isn't on github will return None
	"""
	def repo(self):
		if self.service() == "github":
			splittedUrl = self.url.split("/")
			return "https://github.com/{0}/{1}/".format(splittedUrl[4],splittedUrl[5])
		else:
			return None
	
	r"""
		return the package icon as image object
	"""
	def icon(self):
		return decode(self.icon64)
	
class bmPackage:
	r"""
		rappresents a BeeManipulator package, with all it's data and co.
		the icon is stored as base64 string and then returned as image object when icon() is called
	"""

	def __init__(self, ID=None, author=[], icon64=None, version=0, info={"name": None, "desc": None, "url": None}, content=[], config={}, name=None):
		self.ID = ID
		self.author = author
		self.icon64 = icon64
		self.version = version
		self.info = info
		self.contents = content
		self.config = config
		self.name = name
		self.coAuthors = []
	
	r"""
		return the package icon as image object
	"""
	def icon(self):
		return decode(self.icon64)

	r"""
		this will return the used service, for now only github, dropbox and google drive
	"""
	def service(self):
		if "github" in self.url:
			return "github"
		elif "dropbox" in self.url:
			return "dropbox"
		elif "drive.google" in self.url:
			return "gdrive"

	r"""
		this will return the repo link if the package is on github, if the package isn't on github will return None
	"""
	def repo(self):
		if self.service() == "github":
			splittedUrl = self.url.split("/")
			return "https://github.com/{0}/{1}/".format(splittedUrl[4], splittedUrl[5])
		else:
			return None
	r"""
		for ConFiG OPerations, you can access the config dict directly, but this is the better method, i hope.
		if no operation aurgment is given, use the default operation, r (read).
		on read, if the requested "type" doesn't exist, a None is returned.
	"""
	def cfgOP(self, type = None, data = None, operation = "r"):
		if operation == "w":
			self.config[type] == data
		else:
			if self.config[type]:
				return self.config[type]
			else:
				return None
	
if __name__ == "__main__":
	x = beePackage(ID="id.id", url="https://api.github.com/repos/BEEmod/BEE2.4/releases/latest")
	print(x.repo())
	print(x.ID)
