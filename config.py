import json#for manipulating json files
import os#for open files

"""list of the configs:
	-auto exit, boolean, exit the app after complete the current operation.
	-auto launch bee2, boolean, auto launch bee2 after complete the current operation.
	-bee2 current version, string-float, the version of the current installed bee2, if zero bee2 isn't installed.
	-packages corrent version, array-string, the version of the current istalled packages.
	-manipulator current version, float, current version of the app.
	-portal 2 path, string, self explaining.
	-bee2 is used, boolean, sef explaining, given by if the vbsp_original is present.
	-enable prerelease, boolean, self explaining enable prerelease as update.
	-auto update, boolean, self explaining auto update the app and bee2.4
"""

class config():
	def __init__(self):
		return

	def create_config(self):#create the config file
		cfg='{"config_type": "BEE2.4 Manipulator Config File","appVersion": "0.3","last_version": "false"}'
		with open('config.cfg', 'w', encoding="utf-8") as file:
			json.dump(json.loads(cfg), file, indent=3)
	
	def load(self, section):#load a config
		r""""
		loads a section of the config (json-formatted) and return the
		data.
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
			raise "error"
	
	def save(self, data, section):#save a config
		r""""
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
				cfg = json.load(file)#load the config file
				cfg[section]=data
			with open('config.cfg', 'w', encoding="utf-8") as file:
				json.dump(cfg, file, indent=3)
		except:
			self.create_config()
			self.save(data,section)
	def check(self):
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
