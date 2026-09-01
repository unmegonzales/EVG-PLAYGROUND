#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RosterPath = Join-Path $ScriptDir "roster.csv"

function Get-ReadinessLabel($r) {
  $score = 0
  $total = 7
  if ($r.creating_legends -eq "complete") { $score++ }
  if ($r.sf_stage -in @("signature_step", "post_hire_verification")) { $score++ }
  if ($r.i9_status -eq "complete") { $score++ }
  if ($r.alcohol_status -eq "valid") { $score++ }
  if ($r.food_handler_status -in @("uploaded", "valid")) { $score++ }
  if ($r.security_photo_status -eq "validated") { $score++ }
  if ($r.hr_cleared -match '^(1|yes|true)$') { $score++ }
  $pct = [math]::Round(100 * $score / $total)
  if ($pct -eq 100) { return "READY" }
  return "$pct%"
}

if (-not (Test-Path $RosterPath)) {
  Write-Error "roster.csv not found. Copy roster-template.csv to roster.csv first."
}

$rows = @(Import-Csv $RosterPath | Where-Object { $_.email -and $_.email.Trim() -ne "" })
if ($rows.Count -eq 0) {
  Write-Error "No rows with email addresses in roster.csv"
}

Write-Host ""
Write-Host " Roster - pick someone to email" -ForegroundColor Cyan
Write-Host " ==============================" -ForegroundColor Cyan
Write-Host ""

for ($i = 0; $i -lt $rows.Count; $i++) {
  $r = $rows[$i]
  $name = "$($r.first_name) $($r.last_name)"
  $pct = Get-ReadinessLabel $r
  $num = $i + 1
  Write-Host ("  {0,2}. {1,-25} {2,-30} [{3}]" -f $num, $name, $r.email, $pct)
}

Write-Host ""
Write-Host "  E. Enter email manually"
Write-Host ""
$pick = Read-Host "Enter number (or E)"

if ($pick -eq "E" -or $pick -eq "e") {
  $email = Read-Host "Email"
  $first = Read-Host "First name"
} else {
  $idx = [int]$pick - 1
  if ($idx -lt 0 -or $idx -ge $rows.Count) {
    Write-Error "Invalid selection"
  }
  $r = $rows[$idx]
  $email = $r.email.Trim()
  $first = $r.first_name.Trim()
  Write-Host "Selected: $first ($email)" -ForegroundColor Green
}

Write-Host ""
Write-Host "  1. Onboarding welcome"
Write-Host "  2. Creating Legends reminder"
$tpl = Read-Host "Template (1 or 2, default 1)"
$extra = @()
if ($tpl -eq "2") { $extra += "-ClReminder" }

& (Join-Path $ScriptDir "send-onboarding-email.ps1") -To $email -FirstName $first -Preview @extra
