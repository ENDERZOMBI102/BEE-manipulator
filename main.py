from requests import * #for downloading stuff
from zipfile import * #for operations with zip files
from subprocess import * #for start applications
from sys import platform, argv #for checking the os and aurgments
from threading import Thread #for multithreading option
from ucpParser import ucpParser
from beeManager import beeManager
from web import web
import io #base lib
import json #for operations with json data

reply=""
def checkUpdates():
	ov=get('https://api.github.com/repos/ENDERZOMBI102/BEE-manipulator/releases/latest').json()
	if(not config.load('app version','app version')>=ov['tag_name']):
		print('an update for BEE2.4 Manipular is avaiable!')
		while(not (reply=="no" and reply=="yes" and reply=="n" and reply=="y")):
			reply = input('do you want to install it?')
		

#program start
if(argv[0]=="-shortcutlaunch"):
	if(web.isonline):
		if(beeManager.checkUpdates):
			print('an update for BEE2.4 is avaiable!')
			while(not (reply=="n" and reply=="y")):
				reply = input('do you want to install it? (y/n)')
			
			
os = platform
state = 1
menu = 1
while menu>=1 :
	print('BEE2.4 manipulator by ENDERZOMBI102\n\n')
	if (state == 1) :
		print('1) install')
	elif(state == 2):
		print('1) update')
	else:
		print('1)unistall')
	print('2) user created packages manager')
	print('3) fixer')
	print('4) options')
	print('5) launch BEE2.4')
	print('6) launch Portal 2')
	print('7) quit')
	
	i = input('choose an option: ')
	if(i==1 or i==2 or i==3 or i==4 or i==5 or i==6 or i==7):
		if(i==1):
			beeManger.start(os, state)
	