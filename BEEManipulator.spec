# -*- mode: python ; coding: utf-8 -*-

a = Analysis(['BEEManipulator.py'],
             pathex=['./'],
             binaries=[],
             datas=[('assets', 'assets')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[
                'bz2',  # We aren't using this compression format (shutil, zipfile etc handle ImportError)..
                'sqlite3',  # Imported from aenum, but we don't use that enum subclass.
                # Imported by logging handlers which we don't use..
                'win32evtlog',
                'win32evtlogutil',
                'unittest',  # Imported in __name__==__main__..
                'doctest',
                'optparse'],
             win_no_prefer_redirects=True,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='BEE Manipulator',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='assets/icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='BEE Manipulator')