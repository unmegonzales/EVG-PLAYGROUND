@echo off
echo.
echo  Lobo Ops - Convert Smartsheet Export to roster.csv
echo  ==================================================
echo.
set /p FILE="Path to Smartsheet CSV export: "
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0convert-smartsheet.ps1" -InputFile "%FILE%" -OutputFile "%~dp0roster.csv"
echo.
pause
