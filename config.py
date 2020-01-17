import json#for manipulating json files
from os import path#for open files
from sys import platform
from srctools.property_parser import Property
from srctools.tokenizer import Tokenizer


"""list of the configs:
	-auto exit, boolean, exit the app after complete the current operation.
	-auto launch bee2, boolean, auto launch bee2 after complete the current operation.
	-bee2 current version, string-float, the version of the current installed bee2, if zero bee2 isn't installed.
	-packages corrent version, array-string, the version of the current installed packages.
	-manipulator current version, float, current version of the app.
	-portal 2 path, string, self explaining.
	-bee2 is used, boolean, sef explaining, given by if the vbsp_original file is present.
	-enable prerelease, boolean, self explaining, enable prerelease as update.
	-auto update, boolean, self explaining, auto update the app and bee2.4
"""

class config():
	
	def create_config():#create the config file
		cfg='{"config_type": "BEE2.4 Manipulator Config File","appVersion": "0.1","last_version": "false","beePrereleases":"false","beeUpdateUrl": "None", "steamDir":"None","portal2Dir":"None"}'
		with open('config.cfg', 'w', encoding="utf-8") as file:
			json.dump(json.loads(cfg), file, indent=3)
	
	def load(section):#load a config
		r"""
		loads a section of the config (json-formatted) and return the data.
		raise an exception if the config or the requested section doesn't exist
		example::

			>>> import config
			>>> print(config.load("version"))
			'2.6'
		"""
		try:
			with open('config.cfg', 'r', encoding="utf-8") as file:
				cfg = json.load(file)#iload the config
				readedata = cfg[section]# take the requested field
			return readedata #return the readed data
		except:
			raise configLoadError
	
	def save(data, section):#save a config
		r"""
		save the data on the config (json-formatted), re-create the config if no one is found.
		example::
			>>> import config
			>>> print(config.load("version"))
			'2.6'
			>>> config.save("2.5","version")
			>>> print(config.load("version"))
			'2.5'
		"""
		try:
			with open('config.cfg', 'r', encoding="utf-8") as file:
				cfg = json.load(file)# load the config file
				cfg[section]=data
			with open('config.cfg', 'w', encoding="utf-8") as file:
				json.dump(cfg, file, indent=3)
		except:
			raise configError
	
	def check(arg = None):
		r"""
		if no aurgment is present check if the config file exist and if is a BM config file, else will
		check if the given section exists.
		"""
		try:
			with open('config.cfg', 'r') as file:
				pass
		except:
			raise configDoesntExist
		if arg == None:# check the aurgment is present
			try:
				with open('config.cfg', 'r') as file:# try to open the config file
					cfg = json.load(file)  # load the config file
				# check if EVERY config exists
				x = cfg["beePrereleases"]
				x = cfg["appVersion"]
				x = cfg["last_version"]
				x = cfg["beePrereleases"]
				x = cfg["beeUpdateUrl"]
				x = cfg["steamDir"]
				x = cfg["portal2Dir"]
				if cfg['config_type'] == "BEE2.4 Manipulator Config File":
					return True # the check is made successfully
				else:
					raise configError # the config file is not a BM config file
			except:
				raise configDoesntExist # the config file doesn't exist
		else:
			try:
				with open("config.cfg", 'r') as file:  # try to open the config file
					cfg = json.load(file) # load the config file
					if cfg[arg]:
						return True
					else:
						return False
			except:
				raise configDoesntExist # the config file doesn't exist

class reconfig():
	r"""
		some hardcoded configs are necessary even if i would like to create a fully modular application.
		
		in this section are present hardcoded config and value-searching config
	"""
	def osType():
		return platform
	
	def steamDir():
		r"""
			this function return the steam installation folder
		"""
		if config.check("steamDir"):
			pass

		if not config.load("steamDir") == "None":
			return config.load("steamDir")
		elif platform == "win32":
			# steam is installed on C?
			if path.exists("C:\Program Files (x86)\Steam\steam.exe"):
				return "C:\Program Files (x86)\Steam"
			# steam is installed on D?
			elif path.exists("D:\Steam\steam.exe"):
				return "D:\Steam"
			else:
				return "error, can't automatically determine steam path"

			
	def portalDir():
		if not config.load("portal2Dir") == "None":
			return config.load("portal2Dir")
		else:

			with open(reconfig.steamDir() + "\steamapps\\appmanifest_620.acf", "r") as file:
				manifest = Property.parse(file, "appmanifest_620.acf")# parse the property file
				manifest = manifest.as_dict()# return the property as dictionary
				manifest = manifest["appstate"] #take only the data
				library = reconfig.libraryFolder()
				if manifest["installdir"] == "Portal 2":
					return library[0] + "\Portal 2\\"
	
	def discordToken():
		return "655075172767760384"
				
	def libraryFolder():
		paths = []
		paths.append(reconfig.steamDir())
		try:
			with open(reconfig.steamDir() + "\steamapps\libraryfolders.vdf", "r") as file:
				library = Property.parse(file, "libraryfolders.vdf").as_dict()
				
		except:
			pass
		
		
		return paths
	
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
		if(reconfig.isonline==False):
			return False
		ov=get('https://api.github.com/repos/ENDERZOMBI102/BEE-manipulator/releases/latest').json()
		if(not config.load('appVersion')>=ov['tag_name']):
			return True
		else:
			return False


class configError(BaseException):
	r"""
	base error for config operations
	"""
	pass
class configLoadError(BaseException):
	r"""
	There's no config with that ID!
	"""
	pass
class configDoesntExist(BaseException):
	r"""
	The config file doesn't exist!
	"""
	pass

if __name__ == "__main__":
	print(reconfig.portalDir())
			
			
