@echo off
REM Build the Jarvis installer using Inno Setup
if not exist dist\Jarvis.exe (
    echo Please run build_exe.bat first to create dist\Jarvis.exe
    exit /b 1
)
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" Jarvis.iss
    echo Installer created in installer\JarvisInstaller.exe
    exit /b 0
)
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles%\Inno Setup 6\ISCC.exe" Jarvis.iss
    echo Installer created in installer\JarvisInstaller.exe
    exit /b 0
)
echo Inno Setup compiler not found.
echo Install Inno Setup and re-run this script.
pause
