from requests import *# sending/reciving things from the web
import json # manage json
import base64 # for encrypt a text a image or data to text
import PIL# for managing images

class status:
'''
	this class is all about checking the status of a service.
	with this is possible to check: webhook, website, bot, api and  server status, just call
	the right function and get the response (maintenance, online or offline)
	info() is used to obtain server infos
'''
	def server():
		data=get('https://ucpdatabase.glitch.me/status/server')
		return data.content
		
	def api():
		data=get('https://ucpdatabase.glitch.me/status/api')
		return data.content
		
	def webhook():
		data=get('https://ucpdatabase.glitch.me/status/webhook')
		return data.content
		
	def info():
		data=get('https://ucpdatabase.glitch.me/status/info-server')
		return data.content
		
class ucpd:
'''
	this is the main class, used for much of the api work
'''
	def getfile(whatfile):
		data=get(
		
		
	def getdata(whatdata)