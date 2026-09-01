@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo.
echo  Lobo Ops - Send Email
echo  =====================
echo.
echo  1. Onboarding welcome email
echo  2. Creating Legends reminder
echo  3. Send from roster.csv (pick a name)
echo  4. Exit
echo.
set /p CHOICE="Choose 1-4: "

if "%CHOICE%"=="4" exit /b 0
if "%CHOICE%"=="3" goto fromroster
if "%CHOICE%"=="2" set EXTRA=-ClReminder
if not "%CHOICE%"=="1" if not "%CHOICE%"=="2" (
  echo Invalid choice.
  pause
  exit /b 1
)

set /p EMAIL="Candidate email: "
set /p FIRST="First name: "
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0send-onboarding-email.ps1" -To "%EMAIL%" -FirstName "%FIRST%" %EXTRA% -Preview
goto done

:fromroster
if not exist "%~dp0roster.csv" (
  echo.
  echo roster.csv not found in this folder.
  echo Copy roster-template.csv to roster.csv and fill in your team.
  pause
  exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0send-from-roster.ps1"
goto done

:done
echo.
pause
