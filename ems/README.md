# EMS Access Generation Package

This folder is the **developer handoff** for UNM Athletics Hospitality Event Management System (EMS).

It exists so another tool (or a person sitting in Microsoft Access) can **create the real `.accdb` files**. This Linux environment cannot emit a native Access database.

## What to give the Access-building tool

1. `prompts/ACCESS_GENERATOR_PROMPT.md` — paste this first
2. `EMS_Developer_Build_Binder_Volume_A.md` — build bible
3. `schema/ems_access_schema.json` — canonical field list
4. `schema/create_tables_ace.sql` — fallback DDL
5. `seed/*.csv` — lookup, vendor, location, and category data taken from live workbooks

## Output the other tool must produce

| File | Contents |
|---|---|
| `EMS_BE.accdb` | All tables, relationships, indexes, seed data |
| `EMS_FE.accdb` | Linked tables, dashboard, vendor / event / location / category forms |

Do **not** implement settlement math, PDF, or email in this pass.

## Alpha is done when

1. Open `EMS_FE.accdb`
2. Create an event
3. Create / edit a vendor
4. View seeded locations
5. Manage category map rows
6. Save and reopen records

## Source files this package was built from

- `EMS_Project_Manager_Action_Plan.docx` (Copilot export — architecture only)
- `NPO_Payout_Vendor_Template_final-V4.xlsx` (live NPO engine)
- `09-14-26 - MyVenue Location List - All - UNM.xlsx` (81 locations)
- `09-05-26 RAW Price Level - CATEGORIES - MSR Location Payout.csv`
- `SUB - AP UNM REMIT - NAME - 12-01-25.xlsx`
- `SUB - AP UNM REMIT - SUGAR SHIV - 12-01-25.pdf`
- `NPO - AP UNM REMIT - ARVC - 12-01-25.pdf`
