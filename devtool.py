from os import system, chdir, remove
from pathlib import Path
from sys import argv
from os import getenv

upxpath = 'C:/Users/Flavia/AppData/Local/Programs/UPX/upx-3.96-win64/upx.exe' if getenv('upxpath') is None else getenv('upxpath')
distpath = str( Path('./dist/BEE Manipulator').resolve() ).replace('\\', '/')
sevenzippath = 'C:\"Program Files"\7-Zip\7z' if getenv('7zpath') is None else getenv('7zpath')

if '--help' in argv:
    print('BEE Manipulator development tool v2.3')
    print('Made By ENDERZOMBI102')
    print('Possible parameters:')
    print('--install    installs BM dependencies from requirements.txt')
    print('--start      start BM from source')
    print('--build      use pyinstaller to compile BM to an exe')
    print('--release --debug necessary for --build to work')
    print('--zip        compress the compiled exe+resources to a 7z file')
    print('--startexe   start the exe compiled by pyinstaller')
    print('--deldist    delete the dist folder')
    print('--delbuild   delete the build folder')
    print('--clean      clean up the folder (includes --deldist and --delbuild)')
    print('--pass "ARG" passes the "ARG" string to the exe')

if '--install' in argv:
    system('pip install virtualenv')
    system('py -m venv %userprofile%/.virtualenvs/BEE-manipulator')
    system('%userprofile%/.virtualenvs/BEE-manipulator/scripts/activate && pip install -r requirements.txt')

if '--start' in argv:
    chdir('./src')
    system('pipenv run py BEEManipulator.py')

if ('--build' in argv) and ('--release' in argv):
    system('pyinstaller src/BEEManipulator_release.spec --noconfirm')
    system(f'pyinstaller src/urlhandler/urlhandler.spec --noconfirm --upx-dir="{upxpath}" --distpath="{distpath}"')

if ('--build' in argv) and ('--debug' in argv):
    system('pyinstaller src/BEEManipulator_debug.spec --noconfirm')
    system(f'pyinstaller src/urlhandler/urlhandler.spec --noconfirm --upx-dir="{upxpath}" --distpath="{distpath}"')

if ('--build' in argv) and not ('--debug' or '--release' in argv):
    print('--build needs --debug or --release parameters')

if '--zip' in argv:
    try:
        remove('./BEEManipulator.7z')
    except FileNotFoundError:
        pass
    system(f'{sevenzippath} a -r BEEManipulator ./dist/"BEE Manipulator"/*')
    print('finished step: zip')

if '--startexe' in argv:
    try:
        chdir('./dist/BEE Manipulator')
    except FileNotFoundError:
        print('No dist folder found! BM was not compiled first?')
    else:
        if Path('./BEE Manipulator.exe').exists():
            if '--pass' in argv:
                args = argv[ argv.index('--pass')+1 ]
                system('"BEE Manipulator.exe" ' + args )
            else:
                system('"BEE Manipulator.exe"')
        else:
            print('No exe found! BM was not compiled first or the compile failed?')

if '--deldist' in argv:
    system('rmdir dist /S /Q')
    print('finished step: deldist')

if '--delbuild' in argv:
    system('rmdir build /S /Q')
    print('finished step: delbuild')

if '--clean' in argv:
    print('removing "dist"')
    if Path('./dist').exists():
        system('rmdir dist /S /Q')
    print('removing "build"')
    if Path('./build').exists():
        system('rmdir build /S /Q')
    print('removing "logs"')
    if Path('./logs').exists():
        system('rmdir logs /S /Q')
    print('removing "assets/packages"')
    if Path('./assets/packages').exists():
        system('rmdir assets/packages /S /Q')
    print('removing "assets/about.html"')
    if Path('./assets/about.html').exists():
        remove('assets/about.html')
    print('removing "assets/database.json"')
    if Path('./assets/database.json').exists():
        remove('assets/database.json')
    print('removing "config.cfg"')
    if Path('./config.cfg').exists():
        remove('config.cfg')
    print('finished step: clean')

if len(argv) < 2:
    print('No parameter given! use --help to get help')
