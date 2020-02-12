# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ui.py'],
             pathex=['C:\\Users\\Flavia\\Documents\\GitHub\\BEE-manipulator'],
             binaries=[],
             datas=[("./assets/icon.ico", "./assets/"),("./assets/icon.png", "./assets/")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='BEE Manipulator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,
          upx=True,
          console=False,
          windowed=True,
          icon="./assets/icon.ico")
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='BEE Manipulator')
