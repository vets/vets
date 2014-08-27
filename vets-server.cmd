@echo off

rem 
rem VETS Server Windows .cmd script
rem
rem Move the App directory from a minimal Portable Python installation to python\
rem
rem If you make a shortcut to this script in 
rem %appdata%\Microsoft\Windows\Start Menu\Programs\Startup
rem you can set the shortcuts "Run" option to "Minimized" for a quieter startup
rem

echo VETS Server - DO NOT CLOSE!
echo.

python\python.exe vets.py
