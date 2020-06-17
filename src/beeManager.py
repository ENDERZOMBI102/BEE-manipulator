import configparser
import io
import os
from pathlib import Path
from sys import platform
from zipfile import *

from requests import *

import config
from utilities import boolcmp


def checkBeeUpdates():  # return true if an update is available, false if there isn't or the pc is offline
    if not config.load("beeUpdateUrl") == "None":
        return True
    try:  # get the latest metadata
        data = get("https://api.github.com/repos/BEEmod/BEE2.4/releases/latest")
    except:  # if an error is raised, the pc is offline, so we return False
        return False
    onlineVersion = []  # create empty list
    # iterate in every character in the version string, if there's a invalid character, we remove it
    for i in data["tag_name"]:
        if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            onlineVersion.append(i)  # add the char to the final list
    onlineVersion = "".join(onlineVersion)  # the list is converted to a string
    if int(onlineVersion) > config.version():  # is the online version more updated? if not, return False
        if boolcmp(data["draft"]):  # is the online version a draft? if yes return False
            config.save(None, "beeUpdateUrl")
            return False
        # else return true and save the download url
        config.save(getUrl(data), "beeUpdateUrl")
        return True


def getUrl(data):
    # cycle in the assets
    for asset in data["assets"]:
        # get the correct url for the OS we're on
        if "mac" in asset["name"] and "darwin" in platform:
            return asset["browser_download_url"]
        elif "win" in asset["name"] and "win" in platform:
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
        r = get(config.load("beeUpdateUrl"))  # download BEE
    except Exception as e:
        raise downloadError("failed to complete the download.\n" + e)
    zipdata = ZipFile(io.BytesIO(r.content))  # load and convert the data to a bytes stream
    zipdata.extractall("BEE2")  # extract BEE
    try:
        data = get('https://api.github.com/repos/BEEmod/BEE2-items/releases/latest').json()
    except Exception as e:
        raise downloadError("failed to complete the download.\n" + e)
    d_url = data['assets'][0]['browser_download_url']
    data = get(d_url)
    zipdata = ZipFile(io.BytesIO(data.content))
    zipdata.extractall(config.load("beePath"))


def verifyGameCache():
    # try to delete the bee2 folder ine p2 root dir
    pass

@property
def packageFolder():
    return './../packages/'



class configManager:
    r"""
    BEE2.4 config manager
    this definition contains some userful commands to
    manipulate the config files
    """

    @staticmethod
    def addGame(path='', name='Portal 2', overwrite=False):
        # the games.cfg file path (its where the games data is stored)
        gamescfgPath = os.getenv('APPDATA').replace('\\', '/') + '/BEEMOD2/config/games.cfg'
        # the cfg is a ini formatted file so import a std lib that can handle them
        data = configparser.ConfigParser()
        # open the cfg for reading
        file = open(gamescfgPath, 'r')
        # read the cfg
        data.read_file(file)
        # close the cfg
        file.close()
        # if the section that we want to write already exist raise an exception apart when overwrite is True
        if data.has_section(name) and overwrite:
            # apply the new game
            data[name] = {'steamid': '620', 'dir': path}
        elif not data.has_section(name):
            # apply the new game
            data[name] = {'steamid': '620', 'dir': path}
        else:
            raise GameAlreadyExistError(f'key name {name} already exist! use another name or overwrite!')
        # reopen the cfg for writing
        file = open(gamescfgPath, 'w')
        # write it
        data.write(file)
        # close it
        file.close()

    @staticmethod
    def createAndAddGame(name='Portal 2', loc='', steamid=620):
        # the games.cfg file path (its where the games data is stored)
        gamescfgPath = os.getenv('APPDATA').replace('\\', '/') + '/BEEMOD2/config/games.cfg'
        if Path(gamescfgPath).exists():
            raise FileExistsError("can' create the file, they already exist!")
        # create the necessary folders
        Path(gamescfgPath + '/../..').resolve().mkdir()
        Path(gamescfgPath + '/..').resolve().mkdir()
        data = configparser.ConfigParser()
        # create and open the file for writing
        file = open(gamescfgPath, 'x')
        # the data
        data[name] = {'steamid': steamid, 'dir': loc}
        # write it
        data.write(file)
        # close it
        file.close()


class downloadError(Exception): pass


class GameAlreadyExistError(Exception): pass


if __name__ == "__main__":
    configManager.addGame("c:/hellothere", 'test')
