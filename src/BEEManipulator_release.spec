# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

from PyInstaller.building.build_main import Analysis

blacklist: list = ['cache']
resources: list = []
DISTPATH: str


for file in Path('../resources').glob('*'):
	if file.name in blacklist:
		continue
	if file.is_dir():
		for file2 in file.glob('*'):
			resources.append( ( '/'.join(file2.parts), '/'.join(file2.parts[1:-1]) ) )
	else:
		resources.append( ( '/'.join(file.parts), '/'.join(file.parts[1:-1]) ) )


a = Analysis(
	['BEEManipulator.pyw'],
	pathex=['./'],
	binaries=[],
	datas=resources,
	hiddenimports=['wx._xml'],
	hookspath=['.'],
	runtime_hooks=[],
	excludes=[
		'bz2',  # We aren't using this compression format (shutil, zipfile etc handle ImportError)..
		'sqlite3',  # Imported from aenum, but we don't use that enum subclass.
		'win32evtlog',  # Imported by logging handlers which we don't use..
		'win32evtlogutil',
		'unittest',  # Imported in __name__==__main__..
		'doctest',
		'tkinter'
	],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=None,
	noarchive=False
)
pyz = PYZ(
	a.pure,
	a.zipped_data,
	cipher=None
)
exe = EXE(
	pyz,
	a.scripts,
	[],
	exclude_binaries=True,
	name='BEE Manipulator',
	debug=False,
	bootloader_ignore_signals=False,
	strip=True,
	upx=False,
	console=False,
	windowed=True,
	icon='../resources/icons/icon.ico'
)
coll = COLLECT(
	exe,
	a.binaries,
	a.zipfiles,
	a.datas,
	strip=False,
	upx=False,
	upx_exclude=[],
	name='BEE Manipulator'
)

for dll in Path(f'{DISTPATH}/BEE Manipulator').glob('api-ms-win-*.dll'):
	os.remove( dll )

Path(f'{DISTPATH}/BEE Manipulator/BEE Manipulator.exe')\
	.rename(f'{DISTPATH}/BEE Manipulator/BEEManipulator.exe')

Path(f'{DISTPATH}/BEE Manipulator/BEE Manipulator.exe.manifest')\
	.rename(f'{DISTPATH}/BEE Manipulator/BEEManipulator.exe.manifest')
