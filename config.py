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
	
	def load(section):#load a config
		with open('config.cfg', 'r') as file:
			cfg = file.json()#indicate to python thats a json file
			readedata = cfg[section]# take the requested field
		return readedata #return the readed data
	
	def save(data,section):#save a config
		try:
			print("0")
			with open('config.cfg', 'r', encoding="utf-8") as file:
				r = file.readlines()
				print(1)
				print(r)
				f = r.json()#indicate to python thats a json file
				print("2")
				cfg = dict(f)
				print("3")
				cfg[section]=data
				print("4")
			with open('config.cfg', 'w') as file:
				json.dump(data, file)
				print("5")
			return True#return true if the save is done
		except:
			return False#return false if the save fail
	
r = config.load("last_version")
if(r==False):
	print("error")
else:
	print("saved")