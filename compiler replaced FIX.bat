@echo off
title Compiler Fixer
rem EAF: boolean, Exit After Finish, exit the app after finished fixing
rem FPATH: string, fix path, the path to portal 2 directory
rem WEB: boolean, web, if the computer is connected to the web
rem ALP2: boolean, Auto Launch Portal 2, launch portal 2 after the fix
rem FIXED: boolean, rappresents if the bug was fixed
rem TPATH: boolean, True PATH, is true if the path is correct

rem echo %errorlevel%
set fpath=C:\"Program Files (x86)"\Steam\steamapps\common\"Portal 2"\
set alp2=true
set fixed=false
set vbsp=false
set vrad=false
set tpath=false
set eaf=false
ping -n 1 www.google.com | find "TTL=" >nul
if "%errorlevel%"=="1" (
	set web=offline
) else (
	set web=online
)
if exist %fpath%"portal2" set tpath=true
:menu
	cls
	set %errorlevel%=0
	echo Wecome to the "Original compiler replaced." fixer!
	echo the problem is simple, bee overwrite the original compiler with the bee one.
	echo.
	echo already fixed: %fixed%
	echo path is correct: %tpath%
	echo internet status: %web%
	echo auto launch Portal 2 after fix: %alp2%
	echo current path: %fpath%
	echo. press a option (1/2/3/4/5)
	echo. 1) Fix!
	echo. 2) Launch Portal 2
	echo. 3) Options
	echo. 4) Credits
	echo. 5) Replace compiler to non-BEE state
	echo. 5) Exit
	choice /N /C 12345
	if "%errorlevel%"=="1" goto fixstate
	if "%errorlevel%"=="2" start steam://rungameid/620
	if "%errorlevel%"=="3" goto options
	if "%errorlevel%"=="4" (
		cls
		echo These are the credits!
		echo.
		echo Application By ENDERZOMBI102
		echo BEE2.4 By Teamspen210 and others
		echo.
		pause
	)
	if "%errorlevel%"=="4" (
		ren %fpath%bin\vrad_original.exe vrad.exe
		ren %fpath%bin\vbsp_original.exe vbsp.exe
	)
	if "%errorlevel%"=="6" exit
goto menu

:options
	cls
	set %errorlevel%=0
	echo options for the fixer
	echo. press a option (1/2/3/4/5)
	echo. 1) Insert path to Portal 2
	echo. 2) Auto launch Portal 2: %alp2%
	echo. 3) Redo internet test, status: %web%
	echo. 4) Exit after finish: %eaf%
	echo. 5) Back
	if "%fixed%"=="true" echo 6) Overwrite "alredy fixed"
	choice /N /C 123456
	cls
	if "%errorlevel%"=="1" goto options_setpath
	if "%errorlevel%"=="2" (
		if "%alp2%"=="true" (
			set alp2=false
		) else (
			set alp2=true
		)
	)
	if "%errorlevel%"=="4" (
		if "%eaf%"=="true" (
			set eaf=false
		) else (
			set eaf=true
		)
	)
	if "%errorlevel%"=="5" goto menu
	if "%fixed%"=="true" (
		if "%errorlevel%"=="6" set fixed=false
	)
	if "%errorlevel%"=="3" (
		ping -n 1 www.google.com | find "TTL=" >nul
		if "%errorlevel%"=="1" (
			set web=offline
		) else (
			set web=online
		)
	)
goto options

:options_setpath
	if "%errorlevel%"=="1" (
		cls
		echo imput the path. (if no path is given, use the default)
		echo IF THE PATH CONTAIS SPACES, NEED TO BE FORMATTED LIKE THIS: path\to\"portal 2"
		echo inside " " when contais spaces
		echo current path: %fpath%
		set /p var=
		if "%var%"=="" goto options
		if "%var%"==" " goto options
		set fpath=%var%
		if exist %fpath%"portal2" set tpath=true
	)
goto options

:fixstate
	cls
	set %errorlevel%=0
	if "%web%"=="offline" (
		echo sorry but internet access is required for the fix.
		echo if you have internet access but here don't work please
		echo go to redo a webtest on options
		echo. Press any key to go to options
		pause>nul
		goto options
	)
	if "%fixed%"=="true" (
		echo you have already fixed the error, why retry?
		echo if you really want to refix go to options and select overwrite.
		echo.
		echo Press any key to retun to the menu'
		pause>nul
		goto menu
	)
	set finish=%time%
	certutil.exe -urlcache -split -f "https://github.com/ENDERZOMBI102/updaBEEr/blob/master/vrad_original.exe" %tmp%\vrad_original.exe
	certutil.exe -urlcache -split -f "https://github.com/ENDERZOMBI102/updaBEEr/blob/master/vbsp_original.exe" %tmp%\vbsp_original.exe
	cls
	if exist %tmp%\vbsp.exe set vbsp=true
	if exist %tmp%\vrad.exe set vrad=true
	echo. vrad.exe is downloaded? %vrad%
	echo. vbsp.exe is downloaded? %vbsp%
	if "%vrad%"=="true" (
		echo moving vrad_original to p2 folder...
		move /Y %tmp%\vrad_original.exe %fpath%\bin
	)
	if "%vbsp%"=="true" (
		echo moving vbsp_original to p2 folder...
		move /Y %tmp%\vbsp_original.exe %fpath%\bin
	)
	if "%vbsp%"=="false" (
		del %~dp0\*.key
		echo can't download file vbsp.exe from github.
		echo certutil is abilitated to access internet?
		echo certutil is blocked by an antivirus?
		echo.
		echo permit certutil from the anti virus, is abilitated
		echo false-positive! is a official microsoft software!
		echo.
		echo Press any key to return to the menu'
		pause>nul
		goto menu
	)
	if "%vrad%"=="false" (
		del %~dp0\*.key
		echo can't download file vrad.exe from github.
		echo certutil is abilitated to access internet?
		echo certutil is blocked by an antivirus?
		echo.
		echo permit certutil from the anti virus, is abilitated
		echo false-positive! is a official microsoft software!
		echo.
		echo Press any key to return to the menu'
		pause>nul
		goto menu
	)
	del %~dp0\*.key
	echo.
	echo Done!
	if "%alp2%"=="true" start steam://rungameid/620
	if "%eaf%"=="true" exit
	echo.
	echo Press any key to return to the menu'
	pause>nul
	
goto menu
	
	