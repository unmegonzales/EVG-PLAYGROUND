@echo off
REM Double-click helper — opens PowerShell to send onboarding email via Outlook
echo.
echo  Lobo Ops - Send Onboarding Email via Outlook
echo  =============================================
echo.

set /p EMAIL="Candidate email: "
set /p FIRST="First name: "

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0send-onboarding-email.ps1" -To "%EMAIL%" -FirstName "%FIRST%" -Preview

pause
