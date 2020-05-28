@echo off
cls
del dist /Q
if %~1 == "release" (
	del BEEManipulator.7z
    pyinstaller src/BEEManipulator_release.spec --noconfirm
    C:\"Program Files"\7-Zip\7z a -r BEEManipulator ./dist/"BEE Manipulator"/*
) else (
    pyinstaller src/BEEManipulator_debug.spec --noconfirm
)
