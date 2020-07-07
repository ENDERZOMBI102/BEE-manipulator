from os import system, chdir
from sys import argv

if '--install' in argv:
  system('pip install pipenv')
  system('pipenv lock')
  system('pipenv sync')
  
if '--start' in argv:
  chdir('./src')
  system('pipenv run py BEEManipulator.py')

if ('--build' in argv) and ('--release' in argv):
  system('pyinstaller src/BEEManipulator_release.spec --noconfirm')
  if '--zip' in argv:
    try:
        os.remove('./BEEManipulator.7z')
    except FileNotFoundError:
        pass
    system('')

if ('--build' in argv) and (not '--debug' in argv):
  system('pyinstaller src/BEEManipulator_debug.spec --noconfirm')
    
