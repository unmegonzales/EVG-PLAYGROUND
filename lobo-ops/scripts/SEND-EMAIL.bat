@echo off
chcp 65001 >nul 2>&1
echo.
echo  Lobo Ops - Send Onboarding Email via Outlook
echo  =============================================
echo.

set /p EMAIL="Candidate email: "
set /p FIRST="First name: "

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0send-onboarding-email.ps1" -To "%EMAIL%" -FirstName "%FIRST%" -Preview

if errorlevel 1 (
  echo.
  echo ERROR - see messages above.
  pause
  exit /b 1
)

echo.
pause
