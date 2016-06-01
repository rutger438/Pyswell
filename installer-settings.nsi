# define name of installer
OutFile "oilswell-installer.exe"
 
# define installation directory
InstallDir $PROGRAMFILES\Oilswell
 
# For removing Start Menu shortcut in Windows 7
RequestExecutionLevel user
 
# start default section
Section
 
    # set the installation directory as the destination for the following actions
    SetOutPath $INSTDIR
 
    # create the uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"

    # copy files
    File /r "dist\"
 
    # create a new shortcut to the program uninstaller
    CreateShortCut "$SMPROGRAMS\uninstall-oilswell.lnk" "$INSTDIR\uninstall.exe"
    # create a new shortcuts to the program
    CreateShortCut "$SMPROGRAMS\oilswell.lnk" "$INSTDIR\oilswell.exe"
    CreateShortCut "$DESKTOP\oilswell.lnk" "$INSTDIR\oilswell.exe"
SectionEnd
 
# uninstaller section start
Section "uninstall"
 
    # first, delete the uninstaller
    Delete "$INSTDIR\uninstall.exe"

    # second, remove files and folders
    Delete "$INSTDIR\*.*"
    RmDir /r "$INSTDIR"
 
    # third, remove the links from the start menu
    Delete "$SMPROGRAMS\uninstall-oilswell.lnk"
    Delete "$SMPROGRAMS\oilswell.lnk"
    Delete "$DESKTOP\oilswell.lnk"
 
# uninstaller section end
SectionEnd