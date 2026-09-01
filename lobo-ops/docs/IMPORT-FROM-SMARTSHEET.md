# Import from Smartsheet → roster.csv

Step-by-step guide to move your existing Smartsheet rosters into Lobo Ops.

---

## Before you start

You need these files in the **same folder**:

```
scripts/
├── roster-template.csv    ← column headers (reference)
├── roster.csv             ← YOUR live file (create this)
├── SEND-EMAIL.bat
└── send-onboarding-email.ps1
```

If `roster.csv` doesn't exist yet:

```powershell
Copy-Item roster-template.csv roster.csv
```

---

## Step 1 — Export from Smartsheet

Do this for each sheet you use (Active Roster, Alcohol Permits, Security Photos, etc.).

1. Open the Smartsheet
2. **File → Export → Export to Microsoft Excel** (or CSV)
3. Save to your Desktop, e.g. `Active-Roster-Export.xlsx`

**Tip:** Export the **Active Team Member Roster** first — it has the most columns.

---

## Step 2 — Open both files in Excel

1. Open your Smartsheet export (`Active-Roster-Export.xlsx`)
2. Open `roster.csv` (from your Lobo Ops scripts folder)

Keep them side by side.

---

## Step 3 — Column mapping

Copy data from Smartsheet into `roster.csv` using this map:

| roster.csv column | Smartsheet source | How to fill |
|-------------------|-------------------|-------------|
| `first_name` | First Name | Direct copy |
| `last_name` | Last Name | Direct copy |
| `email` | Email | Direct copy |
| `phone` | Telephone | Direct copy |
| `employee_id` | Employee ID | Direct copy |
| `department_code` | Department / Affiliated Org | See dept table below |
| `classification` | CLASSIFICATION column | `LEVY EMPLOYEE` → `levy_employee`, `NON-PROFIT ORG` → `npo` |
| `position` | Position | Direct copy |
| `manager` | Manager | Direct copy |
| `hire_date` | Hire Date | Format: `YYYY-MM-DD` (e.g. `2025-08-08`) |
| `creating_legends` | Status for Creating Legends (✓) | ✓ or complete → `complete`, Sent CL → `in_progress`, blank → `missing` |
| `sf_stage` | PeopleHub Onboarding Status | See SF map below |
| `i9_status` | i9 e-Verify Status | Complete → `complete`, blank → `not_started` |
| `alcohol_status` | Alcohol Server Permit Match? | Valid → `valid`, No Match → `no_match`, blank → `missing` |
| `food_handler_status` | Food Handler Permit Uploaded? | ✓ or Yes → `uploaded`, blank → `missing` |
| `security_photo_status` | Photo Uploaded / STATUS | VALIDATED → `validated`, ✓ uploaded → `uploaded`, blank → `missing` |
| `hr_cleared` | (manual) | `1` when YOU have cleared them, else `0` |
| `notes` | Action flags / Notes | e.g. "Missing Permits — Action Required" |

### Department code map

| Smartsheet text | roster.csv `department_code` |
|-----------------|------------------------------|
| 36127 - CONCESSIONS / 36127 UNM General | `36127` |
| 36128 - GROUP SALES | `36128` |
| 36129 - SUITES | `36129` |
| 57039 - WAREHOUSE | `57039` |
| 34964 - ADMIN | `34964` |
| 34963 - MANAGEMENT | `34963` |
| NPO - ARVC / Non-Profit | `NPO` |

### SuccessFactors stage map

| PeopleHub / Smartsheet text | roster.csv `sf_stage` |
|----------------------------|------------------------|
| New Employee | `new_employee` |
| Orientation Step | `orientation_step` |
| Signature Step | `signature_step` |
| Post Hire Verification | `post_hire_verification` |

---

## Step 4 — Merge multiple Smartsheet sheets

You often have **separate sheets** for alcohol, food, and security. Match by **email** or **last name + first name**.

### Example workflow

1. **Main roster export** → copy identity columns (name, email, dept, SF stage)
2. **Alcohol sheet export** → VLOOKUP email → fill `alcohol_status`, `alcohol_permit_id`, expiration in notes
3. **Security photos export** → VLOOKUP email → fill `security_photo_status`
4. **Food handler sheet** → VLOOKUP email → fill `food_handler_status`

### Excel VLOOKUP example

In `roster.csv`, if alcohol data is on a sheet named `Alcohol`:

```
=IFERROR(VLOOKUP(B2,Alcohol!D:F,3,FALSE),"missing")
```

Adjust column letters to match your export. Simpler: sort both sheets by email and copy-paste the status column.

---

## Step 5 — Save and verify

1. Save `roster.csv` as **CSV UTF-8** (Excel: Save As → CSV UTF-8)
2. Close Excel (don't leave the file locked)
3. Test:

```powershell
cd path\to\scripts
.\SEND-EMAIL.bat
# Choose option 3 — you should see your team with readiness %
```

Readiness % is calculated automatically:
- **100% / READY** = all 7 event-ready checks pass
- Lower % = missing items listed in the picker

---

## Step 6 — Ongoing updates (weekly rhythm)

You don't re-import everything each time. Pick one:

| Approach | When |
|----------|------|
| **Edit roster.csv directly** | After checking Smartsheet/SF — change status cells |
| **Re-export + merge** | Start of season or big batch of new hires |
| **roster-offline.html** | Double-click → edit → Export CSV → replace roster.csv |

---

## Optional: auto-convert script

If your Smartsheet export is a CSV with familiar column names:

```powershell
cd lobo-ops\scripts
.\convert-smartsheet.ps1 -InputFile "C:\Users\You\Downloads\Active-Roster.csv" -OutputFile "roster.csv"
```

Review the output in Excel before using. The script handles common column name variations.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Option 3 shows no one | `roster.csv` must have an `email` column filled in |
| Readiness always 0% | Check status values match exactly (lowercase, underscores) |
| Excel mangled hire dates | Format column as Text before paste, or use `YYYY-MM-DD` |
| Special characters broke .bat | Save CSV as UTF-8; avoid smart quotes in names |
| Duplicate people | Sort by email, remove dupes before save |

---

## Print reference

Open **`docs/DESK-REFERENCE.html`** in a browser → Print → keep at your desk.
