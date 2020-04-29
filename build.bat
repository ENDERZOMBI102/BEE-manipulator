@echo off
cls
del dist /Q
pyinstaller BEEManipulator.spec --noconfirm
C:\"Program Files"\7-Zip\7z a -r BEEManipulator ./dist/"BEE Manipulator"/*