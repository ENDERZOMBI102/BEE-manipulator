from datetime import datetime

starTime: datetime


def start():
	# starts the timer
	global starTime
	starTime = datetime.now()


def stop():
	#stops the timer
	global starTime
	print(f'time taken to start: { datetime.now() - starTime }')

