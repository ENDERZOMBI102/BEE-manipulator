@echo off
cls
del dist /Q
pyinstaller BEEManipulator.py --add-data assets;assets -i ./assets/icon.ico -noconfirm
C:\"Program Files"\7-Zip\7z a -r BEEManipulator ./dist/BEEManipulator/*