from io import BytesIO
from threading import Thread, Condition
from typing import List, Callable, Dict

import wx
import wx.py.dispatcher as dispatcher
from requests import get

from pluginSystem import Events


class downloadThread(Thread):

	url: str = None
	callback: Callable[ ['downloadThread'], None]

	pauser: Condition = Condition()
	# state properties: those indicate the current state of the thread
	paused: bool = False
	finished: bool = False
	shouldStop: bool = False
	# data: this indicates the data and statistics of the thread
	bytesDone: int = 0
	speed: int = 0
	percentDone: int = 0
	totalLength: int = 0
	data: BytesIO

	def __init__( self, url: str, callback: Callable[ ['downloadThread'], None] ):
		super().__init__()
		self.url = url
		if callback is None:
			raise ValueError('callback have to be a function')
		self.callback = callback

	def run( self ):
		request = get( self.url, stream=True )
		self.totalLength = int( request.headers.get( 'content-length' ) )
		# download!
		for data in request.iter_content( chunk_size=1024 ):
			self.bytesDone += len( data )
			self.data.write( data )
			self.percentDone = int( 100 * self.bytesDone / self.totalLength )
			self.callback(self)
			if self.shouldStop:
				break
			self.pauser.wait()
		else:
			self.finished = True
			self.callback(self)
			wx.CallAfter(
				# func to call
				dispatcher.send,
				# func args
				Events.DownloadCompleted,  # event to trigger
				url=self.url,  # event args
				downloadID=self.getName().replace('DownloadThread-', '')
			)
			# print( f'total: {self.totalLength}, dl: {self.bytesDone}, done: {self.percentDone}' )


class downloadManager:

	downloads: Dict[int, downloadThread] = []
	syncMode: bool = False

	def __init__(self):
		pass

	def startDownload( self, url: str, callback: Callable[ [downloadThread], None] ) -> int:
		"""
		This method starts a new download
		:param url: the url of the file to download
		:param callback: the callback that will be called every time the download progresses or finishes
		:return: the id of the download
		"""
		downloadId = len( self.downloads )
		minusDone = False
		# search for a free ID
		while downloadId in self.downloads.keys():
			if minusDone:
				downloadId -= 1
			else:
				downloadId += 1
		# setup and start the download thread
		self.downloads[ downloadId ] = downloadThread(url, callback)
		self.downloads[ downloadId ].setName(f'DownloadThread-{downloadId}')
		self.downloads[ downloadId ].start()
		dispatcher.send( Events.DownloadStarted, url=url, downloadId=downloadId )
		return downloadId

	def stopDownload( self, downloadId: int ):
		"""
		Abort a download and stops its thread
		:param downloadId: download to stop
		"""
		# tell the thread that he should stop
		self.downloads[ downloadId ].shouldStop = True
		# stop it
		self.downloads[ downloadId ].join()
		del self.downloads[ downloadId ]

	def pauseDownload( self, downloadId: int ):
		"""
		Pauses or resumes a download
		:param downloadId: the download to pause/unpause
		"""
		# toggle the download paused state
		if self.downloads[downloadId].paused:
			self.downloads[ downloadId ].pauser.release()
			self.downloads[ downloadId ].paused = False
		else:
			self.downloads[ downloadId ].pauser.acquire(True)
			self.downloads[ downloadId ].paused = True

	def getDownloads( self ) -> List[str]:
		"""
		Returns a list with all download urls
		:return: List[str]
		"""
		dl: downloadThread
		return [ dl.url for dl in self.downloads ]



