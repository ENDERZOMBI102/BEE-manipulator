from requests import * #for downloading stuff
from threading import Thread #for multithreading option
from bases import package as package
import io #base lib
import json #for operations with json data

#program start

class ucpParser(Thread):
	db = list()
	def start(self, database):
		db_json = database.json()
		
	
	
	def package_parser (self, pckg):
		pckg.json()
		


		