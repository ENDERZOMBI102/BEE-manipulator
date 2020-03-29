from requests import *
from subprocess import *
from zipfile import *
from threading import Thread
from sys import platform as os
from config import *
from utilities import boolcmp
import io

def checkUpdates():#return true if an update is available, false if there isn't or the pc is offline
    if not load("beeUpdateUrl") == None:
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
    if int(onlineVersion) > reconfig.version():# is the online version more updated? if not, return False
        if boolcmp(data["draft"]):# is the online version a draft? if yes return False
            return False
        # check if a prerelease is avaiable, return True if beePresereleases and prerelease values are true
        elif boolcmp(data["prerelease"]):
            if boolcmp(load("beePrereleases")):
                save(getUrl(data), "beeUpdateUrl")
                return True
            else:
                return False
        else:
            save(getUrl(data), "beeUpdateUrl")
            return True

def getUrl(data):
    # cicle in the assets
    for asset in data["assets"]:
        # get the correct url
        if "mac" in asset["name"] and "darwin" in os:
            return asset["browser_download_url"]
        elif "win" in asset["name"] and "win" in os:
            return asset["browser_download_url"]
    raise Exception("how this happened?, you're on linux?")        

def update():
    r"""
    this will update BEE, when called, the function
    will download the latest version based on the
    os is running on and unzip it
    """
    # get the json data
    try:
        r = get(load("beeUpdateUrl"))#download BEE
    except Exception as e:
        raise downloadError("filed to complete the download.\n"+e)
    zipdata = ZipFile(io.BytesIO(r.content)) # load and convert the data to a bytes stream
    zipdata.extractall("BEE2")# extract BEE
    try:
        data = get('https://api.github.com/repos/BEEmod/BEE2-items/releases/latest').json()
    except Exception as e:
        raise downloadError("failed to complete the donwload.\n"+e)
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
        call([load('BEEpath'), ''])
    else:
        call(['.\BEE2', ''])


class configManager():
    r"""
    BEE2.4 config manager
    this definition contains some userful commands to
    manipulate the config files
    """

class downloadError(Exception):
    pass