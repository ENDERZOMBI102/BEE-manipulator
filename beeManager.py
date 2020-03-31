from requests import *
from subprocess import *
from zipfile import *
from threading import Thread
from sys import platform as os
from os import getenv
from config import *
from utilities import boolcmp
from io import BytesIO

def checkBeeUpdates():#return true if an update is available, false if there isn't or the pc is offline
    if not load("beeUpdateUrl") == "None":
        return True 
    try:# get the latest metadata
        data = get("https://api.github.com/repos/BEEmod/BEE2.4/releases/latest")
    except:# if an error is raised, the pc is offline, so we return False
        return False
    onlineVersion = []# create empty list
    # iterate in every character in the version string, if there's a invalid character, we remove it
    for i in data["tag_name"]:
        if i in ['0','1','2','3','4','5','6','7','8','9','.']:
            onlineVersion.append(i)# add the char to the final list
    onlineVersion = "".join(onlineVersion)# the list is converted to a string
    if int(onlineVersion) > version():# is the online version more updated? if not, return False
        if boolcmp(data["draft"]):# is the online version a draft? if yes return False
            save("None", "beeUpdateUrl")
            return False
        # check if a prerelease is avaiable, return false if it is
        elif boolcmp(data["prerelease"]):
            save("None", "beeUpdateUrl")
            return False
        else:# else return true and save the download url
            save(getUrl(data), "beeUpdateUrl")
            return True

def getUrl(data):
    # cicle in the assets
    for asset in data["assets"]:
        # get the correct url for the OS we're on
        if "mac" in asset["name"] and "darwin" in os:
            return asset["browser_download_url"]
        elif "win" in asset["name"] and "win" in os:
            return asset["browser_download_url"]
    raise Exception("how this happened?, you're on linux?")        

def updateBee():
    r"""
    this will update BEE, when called, the function
    will download the latest version based on the
    os is running on and unzip it
    """
    # get the json data
    try:
        r = get(load("beeUpdateUrl"))#download BEE
    except Exception as e:
        raise downloadError("failed to complete the download.\n"+e)
    zipdata = ZipFile(BytesIO(r.content)) # load and convert the data to a bytes stream
    zipdata.extractall("BEE2")# extract BEE
    try:
        data = get('https://api.github.com/repos/BEEmod/BEE2-items/releases/latest').json()
    except Exception as e:
        raise downloadError("failed to complete the donwload.\n"+e)
    d_url = data['assets'][0]['browser_download_url']
    data = get(d_url)	
    zipdata = ZipFile(BytesIO(data.content))
    zipdata.extractall(load("beePath"))

async def startBee():
    r"""
    Use this to start BEE2
    raise an exception if we're not on windows
    """
    if os == "win32":
        await run(load('BEEpath')+"/BEE2.exe")
    else:
        raise Exception("you should use this with windows")

def verifyGameCache():
    # try to delete the bee2 folder ine p2 root dir
    try:
        os.rmdir(portalDir() + "/bee2")
    except:
        pass
    # try to remove the bee2 dir inside the bin folder
    try:
        os.rmdir(portalDir() + "/bin/bee2")
    except:
        pass
    # try to remove the bee2 compilers
    try:
        os.remove()
    except:
        pass

class configManager:
    r"""
    BEE2.4 config manager
    this definition contains some userful commands to
    manipulate the config files
    """
    def addGame(path = ""):
        data = r"""[Portal 2]
steamid = 620
dir = {0}
""".format(path)
        with open(getenv('APPDATA').replace("\\", "/") + "/BEEMOD2/config/games.cfg", "w") as file:
            file.write(data)

            


class downloadError(Exception):
    pass
if __name__ == "__main__":
    configManager.addGame("c:/hellothere")
