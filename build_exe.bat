@echo off
REM Build Jarvis.exe from Jarvis.py using PyInstaller
C:\Users\cjtha\AppData\Local\Python\pythoncore-3.14-64\python.exe -m PyInstaller --onefile --windowed --icon Jarvis.ico --add-data "version.json;." Jarvis.py
echo Build complete. See dist\Jarvis.exe