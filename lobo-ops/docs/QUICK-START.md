# 10-Minute Quick Start (No Node Required)

## Your toolkit - 3 files on Desktop

Copy this whole `scripts` folder to your Desktop (or OneDrive):

| File | What it does |
|------|----------------|
| **SEND-EMAIL.bat** | Send onboarding or CL reminder (menu) |
| **roster-template.csv** | Copy to `roster.csv` and fill in Excel |
| **send-onboarding-email.ps1** | Called by the .bat (don't run alone unless you want) |

## Workflow

### 1. Track your team (Excel or offline roster)
- Copy `roster-template.csv` to `roster.csv`
- Edit in Excel: names, emails, status columns
- OR double-click `../roster-offline.html` for in-browser tracking (Export CSV when done)

### 2. Send emails
Double-click **SEND-EMAIL.bat**:
- **1** = Onboarding welcome
- **2** = Creating Legends reminder  
- **3** = Pick someone from roster.csv (shows readiness %)

### 3. Status column cheat sheet

| Column | Values |
|--------|--------|
| creating_legends | missing, in_progress, complete |
| sf_stage | new_employee, orientation_step, signature_step, post_hire_verification |
| i9_status | not_started, complete |
| alcohol_status | missing, no_match, valid |
| food_handler_status | missing, uploaded |
| security_photo_status | missing, uploaded, validated |
| hr_cleared | 0 or 1 |

**Event Ready** = all 7 complete (shirt NOT required)

## Next session (when you have time)
- Install Node.js for full Lobo Ops web app
- Microsoft Graph API for auto-send without Preview
- Smartsheet sync for auto Valid/No Match
