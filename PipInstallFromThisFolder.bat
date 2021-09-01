rem @echo off
cd /d %~dp0

if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

set currdir=%~dp0
echo %currdir%

call ./dev/DELETE.bat
pip install %currdir%
