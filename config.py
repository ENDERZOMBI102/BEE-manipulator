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
	data ={}
	def cconfig():#create the config file
		print('')
	
	def load(self, type):#load a config
	#	if(type=="all"):
		return '4.3.4'
	
	def save(data,type):#save a config
		print('')
	
		