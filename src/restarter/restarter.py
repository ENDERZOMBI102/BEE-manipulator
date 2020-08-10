import os
import sys
import time

time.sleep(5)
if getattr(sys, 'frozen', False):
	os.system('BEEManipulator.exe')
else:
	os.system('../BEEManipulator.py')