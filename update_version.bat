@echo off
REM Update version script
REM Usage: update_version.bat <new_version> [changelog]

if "%~1"=="" (
    echo Usage: update_version.bat ^<new_version^> [changelog]
    echo Example: update_version.bat 1.1.0 "Added new features"
    exit /b 1
)

set NEW_VERSION=%~1
set CHANGELOG=%~2

if "%CHANGELOG%"=="" set CHANGELOG=No changelog provided

REM Update version.json
echo { > version.json
echo   "version": "%NEW_VERSION%", >> version.json
echo   "changelog": "%CHANGELOG%" >> version.json
echo } >> version.json

REM Update Jarvis.py
powershell -Command "(Get-Content Jarvis.py) -replace 'CURRENT_VERSION = \"[^\"]*\"', 'CURRENT_VERSION = \"%NEW_VERSION%\"' | Set-Content Jarvis.py"

echo Version updated to %NEW_VERSION%
echo Changelog: %CHANGELOG%