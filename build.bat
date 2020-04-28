@echo off
cls
del dist /Q
del config.cfg /Q
del assets/about.html /Q
del assets/database.json /Q
pyinstaller BEEManipulator.spec --noconfirm
C:\"Program Files"\7-Zip\7z a -r BEEManipulator ./dist/"BEE Manipulator"/*