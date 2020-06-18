import os
import subprocess
from pathlib import Path
from sys import argv

if Path('./dist').exists():
    subprocess.call(args='"del dist /Q"', executable='build.bat')
if "--release" in argv:
    print('building release version')
    subprocess.call(args='"pyinstaller src/BEEManipulator_release.spec --noconfirm"', executable='build.bat')
    argv.append('--zip')
else:
    print('building debug version')
    subprocess.call(args='"pyinstaller src/BEEManipulator_debug.spec --noconfirm"', executable='build.bat')

if '--zip' in argv:
    try:
        os.remove('./BEEManipulator.7z')
    except FileNotFoundError:
        pass
    subprocess.run(executable='zip.bat', args='')