from dataclasses import dataclass
from time import time

import wx
from pypresence import Presence, InvalidPipe

import config
from api.manager import Manager
from srctools.logger import get_logger

logger = get_logger()


@dataclass
class RpcData:
	# images
	large_image: str
	large_text: str
	small_image: str
	small_text: str
	# text
	state: str
	details: str
	start: float = time()


class RichPresence(Manager):

	lastData: RpcData = None
	data: RpcData
	presence: Presence
	_timer: wx.Timer
	_retryConnectTimer: wx.Timer
	retryTime: int
	wasConnected: bool = False

	def init( self ) -> None:
		self.presence = Presence( client_id=655075172767760384 )
		self.retryTime = config.load('rpcReconnectTime')
		# timers
		self._timer = wx.Timer()
		self._timer.Notify = lambda: self._update()
		self._retryConnectTimer = wx.Timer()
		self._retryConnectTimer.Notify = lambda: self.tryConnect()
		# dummy data
		self.data = RpcData(
			# images
			large_image=None,
			large_text=None,
			small_image=None,
			small_text=None,
			# text
			state='dummy',
			details='dummy'
		)
		# connect to discord
		self.tryConnect()

	def stop( self ) -> None:
		self._timer.Stop()
		self._retryConnectTimer.Stop()
		self.presence.close()

	def update( self, **kwargs ):
		for key, value in kwargs.items():
			if key in self.data.__dict__:
				setattr(self.data, key, value)
			else:
				logger.warning(f'Got unknown key for RichPresence.update()! key: {key}, value: {value}')

	def _update( self ) -> None:
		if self.data != self.lastData:
			self.presence.update( **self.data.__dict__ )
			self.lastData = RpcData( **self.data.__dict__ )

	def tryConnect( self ) -> None:
		try:
			self.presence.connect()
			self.wasConnected = True
			self._timer.Start(1500)  # every 15 seconds, _update the presence data
		except InvalidPipe:
			logger.info(f'Cannot connect to discord RPC server, retrying in {self.retryTime}s')
			self.wasConnected = False
			self._retryConnectTimer.StartOnce( self.retryTime * 1000 )


manager: RichPresence = RichPresence()


if __name__ == '__main__':
	from random import Random

	def update(evt):
		manager.update(
			state=Random().choice( ['State 1', 'State 2', 'State 3'] ),
			details=Random().choice( [ 'Detail 1', 'Detail 2', 'Detail 3' ] )
		)

	app = wx.App()
	manager.init()
	win = wx.Frame(None)
	btn = wx.Button(
		parent=win,
		label='Change presence'
	)
	btn.Bind(wx.EVT_BUTTON, update)
	win.Show()
	app.MainLoop()
	manager.stop()

