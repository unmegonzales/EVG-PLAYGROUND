#Requires -Version 5.1
<#
.SYNOPSIS
  Convert a Smartsheet CSV/Excel export into Lobo Ops roster.csv format.

.EXAMPLE
  .\convert-smartsheet.ps1 -InputFile "C:\Downloads\Active-Roster.csv"
.EXAMPLE
  .\convert-smartsheet.ps1 -InputFile ".\export.csv" -OutputFile ".\roster.csv" -Preview
#>
param(
  [Parameter(Mandatory = $true)]
  [string] $InputFile,

  [string] $OutputFile = "",

  [switch] $Preview
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $OutputFile) { $OutputFile = Join-Path $ScriptDir "roster.csv" }

function Find-Col($row, [string[]]$names) {
  $props = $row.PSObject.Properties.Name
  foreach ($n in $names) {
    $hit = $props | Where-Object { $_ -match $n } | Select-Object -First 1
    if ($hit) { return $hit }
  }
  return $null
}

function Map-Alcohol($v) {
  if (-not $v) { return "missing" }
  $v = $v.ToString().ToLower().Trim()
  if ($v -match "valid") { return "valid" }
  if ($v -match "no match") { return "no_match" }
  if ($v -match "expir") { return "expired" }
  return "missing"
}

function Map-CL($v) {
  if (-not $v) { return "missing" }
  $v = $v.ToString().ToLower().Trim()
  if ($v -match "complete|yes|true|check|sent cl") { return "complete" }
  if ($v -match "progress|sent") { return "in_progress" }
  return "missing"
}

function Map-Food($v) {
  if (-not $v) { return "missing" }
  $v = $v.ToString().ToLower().Trim()
  if ($v -match "upload|valid|yes|true|check") { return "uploaded" }
  return "missing"
}

function Map-Security($v) {
  if (-not $v) { return "missing" }
  $v = $v.ToString().ToLower().Trim()
  if ($v -match "valid") { return "validated" }
  if ($v -match "upload|check|yes") { return "uploaded" }
  return "missing"
}

function Map-SF($v) {
  if (-not $v) { return "new_employee" }
  $v = $v.ToString().ToLower().Trim()
  if ($v -match "post hire") { return "post_hire_verification" }
  if ($v -match "signature") { return "signature_step" }
  if ($v -match "orient") { return "orientation_step" }
  return "new_employee"
}

function Map-I9($v) {
  if (-not $v) { return "not_started" }
  $v = $v.ToString().ToLower().Trim()
  if ($v -match "complete|verified|yes") { return "complete" }
  return "not_started"
}

function Map-Dept($v) {
  if (-not $v) { return "36127" }
  $v = $v.ToString().Trim()
  if ($v -match "36127|concession") { return "36127" }
  if ($v -match "36128|group sales") { return "36128" }
  if ($v -match "36129|suites|culinar") { return "36129" }
  if ($v -match "57039|warehouse") { return "57039" }
  if ($v -match "34964|admin") { return "34964" }
  if ($v -match "34963|management") { return "34963" }
  if ($v -match "npo|non.profit") { return "NPO" }
  if ($v -match "^(\d{5})") { return $Matches[1] }
  return "36127"
}

function Map-Class($v) {
  if (-not $v) { return "levy_employee" }
  $v = $v.ToString().ToLower()
  if ($v -match "non.profit|npo") { return "npo" }
  if ($v -match "sub|vendor") { return "sub_vendor" }
  return "levy_employee"
}

if (-not (Test-Path $InputFile)) {
  Write-Error "Input file not found: $InputFile"
}

$rows = @(Import-Csv $InputFile)
if ($rows.Count -eq 0) { Write-Error "No data rows in input file" }

$out = @()
foreach ($r in $rows) {
  $fnCol = Find-Col $r @("^first name$", "first")
  $lnCol = Find-Col $r @("^last name$", "last")
  $emCol = Find-Col $r @("^email", "e-mail")
  if (-not $fnCol -or -not $lnCol) { continue }

  $email = if ($emCol) { $r.$emCol } else { "" }
  if (-not $email -and -not $r.$fnCol) { continue }

  $out += [PSCustomObject]@{
    first_name             = $r.$fnCol
    last_name              = $r.$lnCol
    email                  = $email
    phone                  = if (Find-Col $r @("phone", "telephone")) { $r.$(Find-Col $r @("phone", "telephone")) } else { "" }
    employee_id            = if (Find-Col $r @("employee id")) { $r.$(Find-Col $r @("employee id")) } else { "" }
    department_code        = Map-Dept (if (Find-Col $r @("department", "affiliated")) { $r.$(Find-Col $r @("department", "affiliated")) } else { "" })
    classification         = Map-Class (if (Find-Col $r @("classification")) { $r.$(Find-Col $r @("classification")) } else { "" })
    position               = if (Find-Col $r @("position")) { $r.$(Find-Col $r @("position")) } else { "" }
    manager                = if (Find-Col $r @("manager")) { $r.$(Find-Col $r @("manager")) } else { "" }
    hire_date              = if (Find-Col $r @("hire")) { $r.$(Find-Col $r @("hire")) } else { "" }
    creating_legends       = Map-CL (if (Find-Col $r @("creating legends", "creat")) { $r.$(Find-Col $r @("creating legends", "creat")) } else { "" })
    sf_stage               = Map-SF (if (Find-Col $r @("peoplehub", "onboarding status", "successfactor")) { $r.$(Find-Col $r @("peoplehub", "onboarding status", "successfactor")) } else { "" })
    i9_status              = Map-I9 (if (Find-Col $r @("i9", "e-verify")) { $r.$(Find-Col $r @("i9", "e-verify")) } else { "" })
    alcohol_status         = Map-Alcohol (if (Find-Col $r @("alcohol")) { $r.$(Find-Col $r @("alcohol")) } else { "" })
    food_handler_status    = Map-Food (if (Find-Col $r @("food handler", "food")) { $r.$(Find-Col $r @("food handler", "food")) } else { "" })
    security_photo_status  = Map-Security (if (Find-Col $r @("security", "photo", "status")) { $r.$(Find-Col $r @("security", "photo", "status")) } else { "" })
    hr_cleared             = "0"
    notes                  = if (Find-Col $r @("notes", "action")) { $r.$(Find-Col $r @("notes", "action")) } else { "" }
  }
}

if ($out.Count -eq 0) {
  Write-Error "No rows converted. Check that your CSV has First Name / Last Name columns."
}

if ($Preview) {
  $out | Format-Table -AutoSize
  Write-Host "Preview only. $($out.Count) rows would be written to $OutputFile" -ForegroundColor Cyan
} else {
  $out | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding UTF8
  Write-Host "Wrote $($out.Count) rows to $OutputFile" -ForegroundColor Green
  Write-Host "Open in Excel, review, then run SEND-EMAIL.bat option 3" -ForegroundColor Cyan
}
