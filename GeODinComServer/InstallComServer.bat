@ECHO OFF
Set _path="%~dp0GeODin.exe"
IF EXIST %_path% (
 goto REGSERVER
) else (
goto ERROR
)

:REGSERVER
ECHO Try to install GeODin Com-Server
"%~dp0GeODin.exe" -regserver
ECHO Server installed
PAUSE
goto end

:ERROR
ECHO Could not find GeODin
PAUSE
goto end