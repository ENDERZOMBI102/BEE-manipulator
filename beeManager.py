from requests import *
from subprocess import *
from zipfile import *
from threading import Thread
from sys import platform as os
from config import *
from utilities import boolcmp
import io


class beeManager:
	
	def checkUpdates():#return true if an update is available, false if there isn't or the pc is offline
        if not config.load("beeUpdateUrl") == None:
            return True 
		try:# get the latest metadata
            data = get("https://api.github.com/repos/BEEmod/BEE2.4/releases/latest")
        except:# if an error is raised, the pc is offline, so we return False
            return False
        onlineVersion = []# create empty list
        # iterate in every character in the version string, if there's a invalid character, its removed
        for i in data["tag_name"]:
            if i in ['0','1','2','3','4','5','6','7','8','9','.']:
                onlineVersion.append(i)# add the char to the final list
        onlineVersion = "".join(onlineVersion)# the list is converted to a string
        if not int(onlineVersion) > reconfig.version():# is the online version more updated? if not, return False
            return False
        elif boolcmp(data["draft"]):# is the online version a draft? if yes return False
            return False
        # check if a prerelease is avaiable, return True if beePresereleases and prerelease values are true
        elif boolcmp(data["prerelease"]):
            if boolcmp(config.load("beePrereleases"):
                config.save(getUrl(data), "beeUpdateUrl")
                return True
            else:
                return False
        else:
            return True

    def getUrl(data):
        # cicle in the assets
        for asset in data["assets"]:
            # get the correct url
            if "mac" in asset["name"]:
                return asset["browser_download_url"]
            elif "win" in asset["name"]:
                return asset["browser_download_url"]
        raise Exception("how this happened?")        
    
    # TODO: rewrite all ths code bellow to optimize it
	def update():
		r"""
		this will update BEE, when called, the function
		will download the latest version based on the
		os is running on and unzip it
		"""
		# get the json data
        try:
		    r = get(config.load("beeUpdateUrl"))
        except:
            return
		
		zipdata = ZipFile(io.BytesIO(r.content))
		zipdata.extractall("BEE2")
		data = get('https://api.github.com/repos/BEEmod/BEE2-items/releases/latest').json()
		d_url = data['assets'][0]['browser_download_url']
		data = get(d_url)	
		zipdata = ZipFile(io.BytesIO(data.content))
		zipdata.extractall("BEE2")

	def startBee():
		r"""
		Use this to start BEE2
		this is dynamic, call a exec if is on 
		windows and another one if is on MacOS
		"""
		if os == "win32":
		    call(['.\BEE2.exe', ''])
		else:
 		   call(['.\BEE2', ''])
