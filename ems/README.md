# EMS Access Generation Package

This folder is the **developer handoff** for UNM Athletics Hospitality Event Management System (EMS).

It exists so another tool (or a person sitting in Microsoft Access) can **create the real `.accdb` files**. This Linux environment cannot emit a native Access database.

Volume A follows Copilot’s **Developer Build Binder v4.0** chapter map (architecture, lookups, core tables, category map, contracts, forms, build sequence), filled in from live NPO / SUB / MyVenue files. See `COPILOT_V4_CROSSWALK.md`.

## What to give the Access-building tool

1. `prompts/ACCESS_GENERATOR_PROMPT.md` — paste this first
2. `COPILOT_V4_CROSSWALK.md` — Copilot v4.0 vs live corrections
3. `EMS_Developer_Build_Binder_Volume_A.md` — Chapters 1–7 (frozen)
4. `EMS_Developer_Build_Binder_Volume_B.md` — settlement engine (~80% frozen)
5. `schema/ems_access_schema.json` — canonical field list (23 tables)
6. `schema/create_tables_ace.sql` — fallback DDL
7. `seed/*.csv` — lookup, vendor, location, category, and exception types

## Output the other tool must produce

| File | Contents |
|---|---|
| `EMS_BE.accdb` | All tables, relationships, indexes, seed data |
| `EMS_FE.accdb` | Linked tables, dashboard, vendor / event / location / category forms, Import Center shell |

Create **all Volume A + B tables** and named `qry*` objects. Do **not** auto-run settlement math, PDF, or email in the Alpha UI pass. Volume B documents how money moves so the schema does not get redesigned later. Import Center buttons may say Phase 2.

## Alpha is done when

1. Open `EMS_FE.accdb`
2. Create an event
3. Create / edit a vendor
4. View seeded locations
5. Manage category map rows
6. Open Import Center (shell)
7. Save and reopen records

## Source files this package was built from

- Copilot EMS Developer Build Binder v4.0 Volume A (chapter outline pasted 2026-09-19)
- Copilot EMS Developer Build Binder v4.0 Volume B (settlement engine pasted 2026-09-19)
- `EMS_Project_Manager_Action_Plan.docx` (Copilot export — architecture only)
- `NPO_Payout_Vendor_Template_final-V4.xlsx` (live NPO engine)
- `09-14-26 - MyVenue Location List - All - UNM.xlsx` (81 locations)
- `09-05-26 RAW Price Level - CATEGORIES - MSR Location Payout.csv`
- `SUB - AP UNM REMIT - NAME - 12-01-25.xlsx`
- `SUB - AP UNM REMIT - SUGAR SHIV - 12-01-25.pdf`
- `NPO - AP UNM REMIT - ARVC - 12-01-25.pdf`
