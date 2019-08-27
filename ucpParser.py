from requests import * #for downloading stuff
from threading import Thread #for multithreading option
import io #base lib
import json #for operations with json data

#program start

class ucpParser(Thread):
	db = ""
	def start(self, database):
		db = database.json()
		
	
	
	def package_parser (self, pckg):
		package = pckg.json()
		
		