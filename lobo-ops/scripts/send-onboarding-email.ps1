#Requires -Version 5.1
<#
.SYNOPSIS
  Send Levy UNM onboarding email via Outlook — NO Node/npm required.

.DESCRIPTION
  Uses the Outlook desktop app already on your machine. Works when logged into
  Outlook as egonzales@levyrestaurants.com (or change -FromAddress below).

.EXAMPLE
  .\send-onboarding-email.ps1 -To "newhire@email.com" -FirstName "Jessie"

.EXAMPLE
  .\send-onboarding-email.ps1 -To "a@x.com","b@y.com" -FirstName "Team" -Preview
    Opens draft in Outlook for review instead of sending immediately.
#>
param(
  [Parameter(Mandatory = $true)]
  [string[]] $To,

  [Parameter(Mandatory = $true)]
  [string] $FirstName,

  [string] $FromAddress = "egonzales@levyrestaurants.com",

  [switch] $Preview,

  [switch] $ClReminder
)

$ErrorActionPreference = "Stop"

$Links = @{
  CreatingLegends = "https://www.brainshark.com/levy/LevyTeamMemberCreatingLegends"
  AdobeSign       = "https://unm-levy.na4.documents.adobe.com/public/esignWidget?wid=CBFCIBAA3AAABLblqZhApEIJQtFaQg-Xe022g-FS947VuAc3TkuD93kf7sIPQg3VN14Kr2khqpvaLZyZPQGk*&hosted=false"
  Alcohol         = "https://app.smartsheet.com/b/form/019f6f7922fc7fd1b5a526a2d01deab4"
  Food            = "https://app.smartsheet.com/b/form/019fad237860724a9f910507aefed202"
  Security        = "https://app.smartsheet.com/b/form/019fad23fc93785e85bef51c0bb5da2b"
  DigitalDen      = "https://app.smartsheet.com/b/publish?EQBCT=9742da38f8dd4f57867e905b1bfd6485"
}

$LevyLogo = "https://unmegonzales.github.io/ZERO-Communications/email/assets/Levy-Logo.png"
$UnmLogo  = "https://unmegonzales.github.io/ZERO-Communications/email/assets/unm-logo.png"
$Hero     = "https://unmegonzales.github.io/ZERO-Communications/email/assets/Hero.png"

if ($ClReminder) {
  $Subject = "Reminder: Complete Creating Legends Training — Levy UNM"
  $HtmlBody = @"
<p>Hi $FirstName,</p>
<p>Please complete your <strong>Creating Legends Virtual Orientation</strong> before your first shift.</p>
<p><a href="$($Links.CreatingLegends)">Start or continue training</a></p>
<p>Download your certificate when finished.</p>
<p>— Evan Gonzales, Levy UNM HR</p>
"@
} else {
  $Subject = "✅ You're Almost Ready! Complete Your Levy UNM Onboarding"
  $HtmlBody = @"
<!DOCTYPE html><html><body style="font-family:Segoe UI,Arial,sans-serif;">
<table width="600" cellpadding="0" cellspacing="0" style="margin:0 auto;background:#fff;">
<tr><td style="padding:24px;text-align:center;">
  <img src="$LevyLogo" height="40" alt="Levy">
  <img src="$UnmLogo" height="40" alt="UNM">
</td></tr>
<tr><td><img src="$Hero" width="600" alt=""></td></tr>
<tr><td style="padding:32px;">
  <p style="color:#ba0c2f;font-size:11px;letter-spacing:0.14em;font-weight:bold;">LEVY × UNM ATHLETICS</p>
  <h1 style="color:#1a1a2e;">Welcome to the Lobo Hospitality Team</h1>
  <p>Hi $FirstName,</p>
  <p>Complete your onboarding checklist to prepare for your first shift. Estimated time: ~2.5 hours (compensated on or near your first paycheck).</p>
  <h2 style="color:#ba0c2f;">🎯 First Shift Readiness Checklist</h2>
  <ol>
    <li><strong>Creating Legends Training</strong> — <a href="$($Links.CreatingLegends)">Start Training</a></li>
    <li><strong>Employment Paperwork</strong> — <a href="$($Links.AdobeSign)">Review &amp; Sign Documents</a></li>
    <li><strong>Required Uploads:</strong>
      <ul>
        <li><a href="$($Links.Alcohol)">NM Alcohol Server Permit</a></li>
        <li><a href="$($Links.Food)">Food Handler Permit</a></li>
        <li><a href="$($Links.Security)">UNM Athletics Photo Upload</a></li>
      </ul>
    </li>
    <li><strong>Resources:</strong> <a href="$($Links.DigitalDen)">Digital Den</a></li>
  </ol>
  <p>Welcome to the team!<br><br>
  <strong>Evan E. Gonzales</strong><br>
  Finance &amp; Human Resources Manager<br>
  Levy at UNM Athletics<br>
  egonzales@levyrestaurants.com</p>
</td></tr>
</table>
</body></html>
"@
}

try {
  $outlook = New-Object -ComObject Outlook.Application
} catch {
  Write-Error @"
Outlook is not available. Make sure Microsoft Outlook desktop is installed and you are logged in.

If Outlook is installed, try running PowerShell as your normal user (not elevated).
Alternative: ask IT to enable Graph API — see lobo-ops/docs/OUTLOOK-SETUP.md
"@
}

foreach ($recipient in $To) {
  $mail = $outlook.CreateItem(0)  # olMailItem
  $mail.To = $recipient
  $mail.Subject = $Subject
  $mail.HTMLBody = $HtmlBody

  # Send from your Levy mailbox if account exists in Outlook profile
  try {
    $account = $outlook.Session.Accounts | Where-Object { $_.SmtpAddress -eq $FromAddress } | Select-Object -First 1
    if ($account) { $mail.SendUsingAccount = $account }
  } catch { /* optional — uses default account */ }

  if ($Preview) {
    $mail.Display($true)
    Write-Host "Draft opened for review: $recipient" -ForegroundColor Cyan
  } else {
    $mail.Send()
    Write-Host "Sent to: $recipient" -ForegroundColor Green
  }
}

Write-Host "Done." -ForegroundColor Green
