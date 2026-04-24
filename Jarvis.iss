[Setup]
AppName=Jarvis
AppVersion=1.0
DefaultDirName={pf}\Jarvis
DefaultGroupName=Jarvis
OutputBaseFilename=JarvisInstaller
Compression=lzma
SolidCompression=yes
DisableStartupPrompt=yes
OutputDir=installer
SetupIconFile=Jarvis.ico

[Files]
Source: "dist\\Jarvis.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "version.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Jarvis"; Filename: "{app}\Jarvis.exe"
Name: "{userdesktop}\Jarvis"; Filename: "{app}\Jarvis.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
