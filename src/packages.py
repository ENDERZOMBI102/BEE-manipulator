from pathlib import Path
from typing import List, Union

import wx
import wx.lib
from pydantic import BaseModel

import config
from srctools.logger import get_logger

logger = get_logger()


class BPackage(BaseModel):

	identifier: str
	authors: List[str]
	name: str
	description: str
	website: Union[str, None]
	repo: str


class BMPackage(BaseModel):

	identifier: str
	authors: List[str]
	name: str
	description: str
	website: Union[str, None]
	repo: str
	files: List[str]


class PackageLargeView(wx.Frame):

	#
	def __init__(self):
		super().__init__(

		)


class PackageView(wx.Panel):

	package: BPackage
	image: wx.StaticBitmap
	largeView: PackageLargeView

	def __init__(self, master: wx.ScrolledWindow, package: BPackage):
		self.package = package
		super().__init__(
			parent=master,
			name=f'VIEW_{self.package.identifier}'
		)
		# create sizers
		sizer = wx.BoxSizer(wx.VERTICAL)
		upsizer = wx.BoxSizer()
		bottomsizer = wx.BoxSizer()
		# image
		self.image = wx.StaticBitmap(
			parent=self,
			bitmap=getIcon(self.package.identifier)
		)
		upsizer.Add(
			self.image
		)

		# set the sizers inside the panel
		sizer.Add(
			upsizer,
			wx.SizerFlags(1).Top()
		)
		sizer.AddSpacer(10)
		sizer.Add(
			bottomsizer
		)
		self.SetSizer(sizer)


class PlaceHolderView(PackageView):

	image: wx.StaticBitmap

	def __init__(self, master: wx.ScrolledWindow):
		super().__init__( master )
		self.image = wx.StaticBitmap(
			parent=self,
			bitmap=wx.Bitmap(f'{config.assetsPath}nodb.png'),
			pos=wx.Point(100, 100),
			size=wx.Size(200, 200)
		)
		self.image.Show(True)


def getIcon(pid: str) -> wx.Bitmap:
	path = Path( f'{config.assetsPath}packages/{pid}/icon.png' )
	if path.exists():
		return wx.Bitmap( str( path ) )
	else:
		return wx.Bitmap()
