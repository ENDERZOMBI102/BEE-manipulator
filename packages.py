from json import *
from base64 import b64decode as decode

class beePackage:
	r"""
		rappresents a BEE2.4 package, with all its data; icon, author, file name and a description are
		stored here, with the others.
		the icon is stored as base64 string and then returned as image object when icon() is called
	"""
	def __init__(self, ID = None, icon64 = None, author = [], description = None, url = "None"):
		self.ID = ID
		self.author = author
		self.icon64 = icon64
		self.description  = description
		self.url = url
	"""
		this will return the used service, for now only github, dropbox and google drive
	"""
	def service(self):
		if "github" in self.url:
			return "github"
		elif "dropbox" in self.url:
			return "dropbox"
		elif "drive.google" in self.url:
			return "gdrive"
	"""
		this will return the repo link if the package is on github, if the package isn't on github will return None
	"""
	def repo(self):
		if self.service() == "github":
			splittedUrl = self.url.split("/")
			return "https://github.com/{0}/{1}/".format(splittedUrl[4],splittedUrl[5])
		else:
			return None
			
	def icon(self):
		return decode(self.icon64)
	
class bmPackage:
	r"""
		rappresents a BeeManipulator package, with all it's data and co.
	"""
	def __init__(self, ID = None, author = []):
		self.ID = ID
		self.author = author
		"""self.
		self.
		self.
		self.
		self."""

if __name__ == "__main__":
	x = beePackage(ID="id.id", url="https://api.github.com/repos/BEEmod/BEE2.4/releases/latest")
	print(x.repo())
