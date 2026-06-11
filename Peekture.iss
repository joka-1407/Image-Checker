; Peekture Installer Script
; Inno Setup

[Setup]
AppId={{F8E0D4D3-7B4E-4C2A-9A1E-3B5C6D7E8F90}
AppName=Peekture
AppVersion=1.0
AppPublisher=James Orhin Agyin
DefaultDirName={autopf}\Peekture
DefaultGroupName=Peekture
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=C:\Users\jimor\OneDrive\Desktop\Coding Projects\Image Checker\installer
OutputBaseFilename=PeektureSetup
SetupIconFile=C:\Users\jimor\OneDrive\Desktop\Coding Projects\Image Checker\Peaklogo Icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\Peekture.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\Peekture.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Peekture"; Filename: "{app}\Peekture.exe"
Name: "{autodesktop}\Peekture"; Filename: "{app}\Peekture.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Peekture.exe"; Description: "Launch Peekture"; Flags: nowait postinstall skipifsilent