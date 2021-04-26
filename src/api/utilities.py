from dataclasses import dataclass

import wx
from semver import VersionInfo

icon: wx.Icon
""" BEE Manipulator icon as wx.Icon object """


class wxStyles:
	TITLEBAR_ONLY_BUTTON_CLOSE = wx.DEFAULT_FRAME_STYLE ^ wx.MINIMIZE_BOX ^ wx.MAXIMIZE_BOX


@dataclass
class UpdateInfo:

	version: VersionInfo
	url: str
	description: str


def isonline():
	"""
	simple function that checks if the pc is online or not
	:return: True if it is else False
	"""


def checkUpdate(url: str, curVer: VersionInfo) -> UpdateInfo:
	"""
	A function that check for updates, this doesn't include prereleases
	:param url: the api/repo github url
	:param curVer: current version
	:return: an object of class VersionInfo
	"""


def genReleasesApiUrl(url: str = None) -> str:
	"""
	A function that makes a github api latest release url from a repo url
	:param url: repo url to be transformed
	:return: the github api url
	"""


def frozen() -> bool:
	"""
	if BM is in a frozen state (exe), returns True
	:return: true if it is, otherwise false
	"""


def cacheDirPath() -> str:
	""" Retuns the path of the cache directory """


def getCorrectPath(path: str) -> str:
	""" Returns the right path for source and compiled runs """


def notimplementedyet():
	"""	Shows a dialog that says that this feature its not implemented """


def parseValue( param: str ) -> [str, int, float, None, bool]:
	"""
	Parses a string and returns its value
	:param param: string to parse
	:return: parsed value
	"""


defBeePath: str
devEnv: bool
