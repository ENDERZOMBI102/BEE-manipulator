from requests import *
from subprocess import *
from zipfile import *
from sys import platform
import json
import io

os=platform

r = get('https://api.github.com/repos/BEEmod/BEE2.4/releases/latest')
j = r.json()
mac_url = j['assets'][0]['browser_download_url']
win_url = j['assets'][1]['browser_download_url']
if os == "win32":
    r =get(win_url)
else:
    r =get(mac_url)
z =ZipFile(io.BytesIO(r.content))
z.extractall("BEE2")
r = get('https://api.github.com/repos/BEEmod/BEE2-items/releases/latest')
j = r.json()
d_url = j['assets'][0]['browser_download_url']
r =get(d_url)
z =ZipFile(io.BytesIO(r.content))
z.extractall("BEE2")
if os == "win32":
    call(['.\BEE2.exe', ''])
else:
    call(['.\BEE2', ''])

