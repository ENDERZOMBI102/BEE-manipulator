import json#for manipulating json files
from os import path#for open files
from sys import platform

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
		cfg='{"config_type": "BEE2.4 Manipulator Config File","appVersion": "0.1","last_version": "false","enableBee2Prereleases":"false","steamDir":"None","portal2Dir":"None"}'
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
			raise configError("There's no config with that ID")
	
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
			raise configError("")
	
	def check():
		r"""
		check if the config file exist and if is a BM config file.
		"""
		try:
			with open('config.cfg', 'r') as file:#
				cfg = json.load(file)  # load the config file
				if cfg['config_type'] == "BEE2.4 Manipulator Config File":
					return "ok"
				else:
					return "error"
		except:
			return "error"

class reconfig():
	r"""
		some hardcoded configs are necessary even if i would like to create a fully modular application.
		
		in this section are present hardcoded config and value-searching config
	"""
	def osType():
		return platform
	
	def steamDir():
		r"""
			this funcion return the steam installation folder
		"""
		if config.load("steamDir") is not "None":
			return config.load("steamDir")
		elif platform == "win32":
			# steam is installed on C?
			if path.exists("C:\Program Files(x86)\Steam\steam.exe"):
				return "C:\Program Files(x86)\Steam\steam.exe"
			# steam is installed on D?
			elif path.exists("D:\Program Files(x86)\Steam\steam.exe"):
				return "D:\Program Files(x86)\Steam\steam.exe"
			else:
				return "error, can't automatically determine steam path"

			
	def portal2Dir():
		if config.load("portal2Dir") is not "None":
			return config.load("portal2Dir")
		else:
			pass
			
class configError(BaseException):
	pass


			
			
