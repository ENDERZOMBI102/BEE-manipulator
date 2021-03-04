from io import BytesIO
from threading import Thread, Condition
from typing import List, Callable, Dict

import wx
import wx.py.dispatcher as dispatcher
from requests import get

from config import dynConfig
from pluginSystem import Events


class downloadThread(Thread):

	url: str = None
	callback: Callable[ ['downloadThread'], None]
	maxSpeed: int

	pauser: Condition = Condition()
	# state properties: those indicate the current state of the thread
	paused: bool = False
	finished: bool = False
	shouldStop: bool = False
	dataHasBeenRetrieved: bool = False
	# data: this indicates the data and statistics of the thread
	bytesDone: int = 0
	speed: int = 0
	percentDone: int = 0
	totalLength: int = 0
	data: BytesIO

	def __init__( self, url: str, callback: Callable[ ['downloadThread'], None], maxSpeed: int = 1024 ):
		super().__init__()
		self.url = url
		self.data = BytesIO()
		if isinstance(callback, Callable):
			raise ValueError('callback must be a function')
		self.callback = callback
		self.maxSpeed = maxSpeed

	def getData( self ) -> BytesIO:
		"""
		Returns the downloaded data
		:return: BytesIO containing the downloaded bytes
		"""
		self.dataHasBeenRetrieved = True
		return self.data

	def run( self ):
		request = get( self.url, stream=True )
		self.totalLength = int( request.headers.get( 'content-length' ) )
		# download!
		for data in request.iter_content( chunk_size=self.maxSpeed ):
			self.bytesDone += len( data )
			self.speed = len( data )
			self.data.write( data )
			self.percentDone = int( 100 * self.bytesDone / self.totalLength )
			self.callback(self)
			if self.shouldStop:
				request.close()
				break
			if self.paused:
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
			if dynConfig['printDownloadProgress']:
				print( f'total: {self.totalLength}, dl: {self.bytesDone}, done: {self.percentDone}' )


class downloadManager:

	downloads: Dict[int, downloadThread] = {}
	_timer: wx.Timer
	_syncMode: bool = False
	_shouldStop: bool = False
	"""PRIVATE PROPERTY"""

	def init(self):
		self._timer = wx.Timer()
		self._timer.Notify = lambda: self._tick()
		# schedule ticking every 5 milliseconds
		self._timer.Start(5)

	def startDownload( self, url: str, callback: Callable[ [downloadThread], None], maxSpeed: int = 1024 ) -> int:
		"""
		This method starts a new download
		:param url: the url of the file to download
		:param callback: the callback that will be called every time the download progresses or finishes
		:param maxSpeed: maximum chunk size
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
		self.downloads[ downloadId ] = downloadThread(url, callback, maxSpeed)
		self.downloads[ downloadId ].setName(f'DownloadThread-{downloadId}')
		if not self._syncMode:
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

	def toggleDownload( self, downloadId: int, enable: bool = None ):
		"""
		Pauses or resumes a download.
		if enable is present, True will resume the download if it is not,
		False will pause the download if it is not
		:param downloadId: the download to pause/unpause
		:param enable: should enable or disable
		"""
		if enable is None:
			# here the download pause state is toggled
			if self.downloads[downloadId].paused:
				self.downloads[ downloadId ].pauser.release()
				self.downloads[ downloadId ].paused = False
			else:
				self.downloads[ downloadId ].pauser.acquire(True)
				self.downloads[ downloadId ].paused = True
		else:
			# here will resume/pause the download based on the enable parameter
			if enable:
				# enable is True, if the download isn't resumed, resume it
				if self.downloads[ downloadId ].paused:
					self.toggleDownload( downloadId )
			else:
				# enable is False, if the download isn't paused, pause it
				if not self.downloads[ downloadId ].paused:
					self.toggleDownload( downloadId )

	def getDownloads( self ) -> List[str]:
		"""
		Returns a list with all download urls
		:return: List[str]
		"""
		dl: downloadThread
		return [ dl.url for dl in self.downloads.values() ]

	def waitUtilDone( self, downloadId: int ):
		"""
		Calling this will result in a block until the download finishes
		:param downloadId: the download id to wait for
		"""
		while not self.downloads[ downloadId ].finished:
			pass

	def syncMode( self ):
		"""
		Toggles sync mode, by default the manager works in async mode
		sync mode makes so that only one download is active at time
		"""
		self._syncMode = not self.syncMode
		if self.syncMode:
			# pause all downloads
			for downloadId in self.downloads.keys():
				self.toggleDownload( downloadId )
			# resume the first download
			self._resumeFirst()
		else:
			# resume all downloads
			for downloadId in self.downloads.keys():
				if self.downloads[ downloadId ].paused:
					self.toggleDownload( downloadId )

	def _resumeFirst( self ):
		"""
		Resumes only the first download of the queue
		"""
		# HACK: use the "iterator" to get the first item, then break
		for downloadId in self.downloads.keys():
			self.toggleDownload( downloadId )
			break

	def activeCount( self ) -> int:
		"""
		Counts all the active downloads at this moment
		:return: the active download count
		"""
		active: int = 0
		# count the non-paused downloads
		for download in self.downloads.values():
			if not download.paused:
				active += 1
		return active

	def _tick( self ):
		"""
		Internal method used to check things in sync mode, so that
		a download can resume if one has finished etc, does nothing in async mode
		"""
		if self._syncMode:
			# we're in sync mode
			toBeDeleted: int = None
			# there's no active downloads, if there's one paused, resume it
			if self.activeCount() == 0:
				self._resumeFirst()
			else:
				enableNext: bool = False
				# cycle in all downloads
				#
				# checks all downloads, if the active one finished, enable the next
				# and remove the one that finished
				for downloadId in self.downloads.keys():
					if self.downloads[ downloadId ].finished:
						# enable the next download and remove the current one only if the
						# current download's data has been retrieved
						if self.downloads[downloadId].dataHasBeenRetrieved:
							toBeDeleted = downloadId
							enableNext = True
					elif enableNext:
						self.toggleDownload( downloadId )
						break
			# if there's a download to remove, remove it
			if toBeDeleted:
				del self.downloads[ toBeDeleted ]

	def stop( self ):
		"""
		Stop and cancel all downloads
		"""
		for download in self.downloads.values():
			download.shouldStop = True
		self.downloads.clear()
		self._shouldStop = True
		self._timer.Stop()


manager: downloadManager = downloadManager()

