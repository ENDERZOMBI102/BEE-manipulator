from requests import * #for downloading stuff
from zipfile import * #for operations with zip files
from subprocess import * #for start applications
from sys import platform, argv#for checking the os and aurgments
from threading import Thread #for multithreading option
from ucpParser import ucpParser
from beeManager import beeManager
from config import config
from web import web
import io #base lib
import json #for operations with json data




#program start
reply=""
if(web.checkUpdates()==True):
	print('an update for BEE2.4 Manipulator is avaiable!')
	while(not (reply=="no" and reply=="yes" and reply=="n" and reply=="y")):
		reply = input('do you want to install it?')
	if(reply=='yes' or reply=='y'):
		web.installUpdates()
	else:
		print('ok, i don\'t install this update now')
				
				
				
				
				
				
os = platform
state = config.load('bee state')
if(beeManager.checkUpdates()==True):
	state = 2
menu = 1
while menu>=1 :
	print('BEE2.4 manipulator by ENDERZOMBI102\n\n')
	if (state == 1) :
		print('1) install BEE2.4')
	elif(state == 2):
		print('1) update BEE2.4')
	else:
		print('1)unistall BEE2.4')
	print('2) user created packages manager')
	print('3) fixer')
	print('4) options')
	print('5) launch BEE2.4')
	print('6) launch Portal 2')
	print('7) quit')
	
	i = input('choose an option: ')
	if(i==1 or i==2 or i==3 or i==4 or i==5 or i==6 or i==7):
		if(i==1):
			beeManager.start(os, state)
		
	