; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)

AppId={{C9181EC3-F379-44C9-8070-FCAB3E22A02C}
AppName=Descargar de El Trece
AppVersion=1.1
;AppVerName=Descargar de El Trece 1.1
AppPublisher=Televisión a la carta
AppPublisherURL=http://blog.tvalacarta.info/
AppSupportURL=http://blog.tvalacarta.info/
AppUpdatesURL=http://blog.tvalacarta.info/
DefaultDirName={pf}\Televisión a la carta\Descargar de El Trece
DefaultGroupName=Televisión a la carta
LicenseFile=C:\py2exe\eltrece\LICENSE.txt
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "C:\py2exe\eltrece\dist\descargar.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\py2exe\eltrece\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Descargar de El Trece"; Filename: "{app}\descargar.exe"
Name: "{group}\{cm:ProgramOnTheWeb,Televisión a la carta}"; Filename: "http://blog.tvalacarta.info/"
Name: "{commondesktop}\Descargar de El Trece"; Filename: "{app}\descargar.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Descargar de El Trece"; Filename: "{app}\descargar.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\descargar.exe"; Description: "{cm:LaunchProgram,Descargar de El Trece}"; Flags: nowait postinstall skipifsilent

