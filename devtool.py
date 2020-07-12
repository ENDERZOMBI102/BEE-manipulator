from os import system, chdir, remove
from pathlib import Path
from sys import argv

if '--help' in argv:
    print('BEE Manipulator development tool v2.1')
    print('Made By ENDERZOMBI102')
    print('Possible parameters:')
    print('--install    installs BM dependencies from pipfile')
    print('--start      start BM from source')
    print('--build      use pyinstaller to compile BM to an exe')
    print('--release --debug necessary for --build to work')
    print('--zip        compress the compiled exe+resources to a 7z file')
    print('--startexe   start the exe compiled by pyinstaller')
    print('--deldist    delete the dist folder')
    print('--delbuild   delete the build folder [new in 2.1]')
    print('--clean      clean up the folder (includes --deldist and --delbuild) [new in 2.1]')

if '--install' in argv:
    system('pip install pipenv')
    system('pipenv lock')
    system('pipenv sync')

if '--start' in argv:
    chdir('./src')
    system('pipenv run py BEEManipulator.py')

if ('--build' in argv) and ('--release' in argv):
    system('pyinstaller src/BEEManipulator_release.spec --noconfirm')

if ('--build' in argv) and ('--debug' in argv):
    system('pyinstaller src/BEEManipulator_debug.spec --noconfirm')

if ('--build' in argv) and not ('--debug' or '--release' in argv):
    print('--build needs --debug or --release parameters')

if '--zip' in argv:
    try:
        remove('./BEEManipulator.7z')
    except FileNotFoundError:
        pass
    system(r'C:\"Program Files"\7-Zip\7z a -r BEEManipulator ./dist/"BEE Manipulator"/*')

if '--startexe' in argv:
    chdir('./dist/BEE Manipulator')
    if Path('./BEE Manipulator.exe').exists():
        system('"BEE Manipulator.exe --dev"')
    else:
        print('No exe found! BM was not compiled first or the compile failed.')

if '--deldist' in argv:
    system('rmdir dist /S /Q')

if '--delbuild' in argv:
    system('rmdir build /S /Q')

if '--clean' in argv:
    if Path('./dist').exists():
        system('rmdir dist /S /Q')
    if Path('./build').exists():
        system('rmdir build /S /Q')
    if Path('./logs').exists():
        system('rmdir logs /S /Q')
    if Path('./config.cfg').exists():
        remove('config.cfg')

if len(argv) < 2:
    print('No parameter given! use --help to get help')
