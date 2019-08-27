from requests import * #for downloading stuff
from zipfile import * #for operations with zip files
from subprocess import * #for start applications
from sys import platform #for checking the os
from threading import Thread #for multithreading option
from ucpParser import ucpParser
from beeManager import beeManager
import io #base lib
import json #for operations with json data

#program start
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
	