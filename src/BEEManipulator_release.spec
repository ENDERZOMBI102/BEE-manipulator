# -*- mode: python ; coding: utf-8 -*-


a = Analysis(['BEEManipulator.py'],
             pathex=['./'],
             binaries=[],
             datas=[('../assets/about.md', 'assets'),
                    ('../assets/icons/*', 'assets/icons')],
             hiddenimports=['wx._xml'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[
                'bz2', # We aren't using this compression format (shutil, zipfile etc handle ImportError)..
                'sqlite3', # Imported from aenum, but we don't use that enum subclass.
                'win32evtlog', # Imported by logging handlers which we don't use..
                'win32evtlogutil',
                'unittest',  # Imported in __name__==__main__..
                'doctest',
                'tkinter',
                'numpy'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=False,
          name='BEE Manipulator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,
          upx=True,
          console=False,
          windowed=True,
		  icon='../assets/icons/icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='BEE Manipulator')
