from datetime import datetime

starTime: datetime


def start():
	global starTime
	starTime = datetime.now()


def stop():
	global starTime
	print(f'time taken to start: { datetime.now() - starTime }')

