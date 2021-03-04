import wx


stopwatch = wx.StopWatch()


def start():
	# starts the timer
	stopwatch.Start()


def stop():
	# stops the timer
	global stopwatch
	stopwatch.Pause()
	print(f'time taken to start: { stopwatch.Time() // 1000 }.{stopwatch.Time() % 1000}s')
	del stopwatch

