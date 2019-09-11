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

	def cconfig():#create the config file
		print('')
	
	def load(type):#load a config
		with open('config.cfg', 'r') as file:
			cfg = file.json()#indicate to python thats a json file
			readedata = cfg[type]# take the requested field
		return readedata #return the readed data
	
	def save(data,type):#save a config
		try:
			with open('config.cfg', 'rw') as file:
				cfg = file.json()#indicate to python thats a json file
				json.dump(data, outfile)
			return True#return true if the save is done
		except:
			return False#return false if the save fail
	
config.save("appVersion")