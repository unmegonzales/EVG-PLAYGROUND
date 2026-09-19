# Paste this into the Access-building tool

You are generating a **Microsoft Access** application for UNM Athletics Hospitality / Levy.

This environment can create `.accdb` files. Follow the attached EMS package. Do not invent tables, fields, or rates.

Walk **Volume A Chapters 1–7** in `ems/EMS_Developer_Build_Binder_Volume_A.md` (Copilot v4.0 chapter map). Live-file corrections in that binder and `ems/COPILOT_V4_CROSSWALK.md` override Copilot chat.

## Attached / required files

Read in this order:

1. `ems/prompts/ACCESS_GENERATOR_PROMPT.md` (this file)
2. `ems/COPILOT_V4_CROSSWALK.md` — Copilot v4.0 vs live files
3. `ems/EMS_Developer_Build_Binder_Volume_A.md`
4. `ems/EMS_Developer_Build_Binder_Volume_B.md` — how the money moves; create tables/queries now, do not run the engine in Alpha
5. `ems/schema/ems_access_schema.json`
6. `ems/schema/RELATIONSHIPS.md`
7. `ems/seed/IMPORT_ORDER.md`
8. Every CSV in `ems/seed/` except `location_alias_conflicts.csv` (docs only)
9. `ems/schema/create_tables_ace.sql` only if you can run ACE SQL; otherwise use Table Designer from the JSON

JSON is the canonical field list. If you would like to “improve” the schema, **don’t**. File a note instead.

## Create these two files

- `EMS_BE.accdb` — tables, relationships, indexes, seed data
- `EMS_FE.accdb` — linked tables + forms + AutoExec to `frmDashboard`

Put them wherever the user asks. Default: a folder named `EMS` next to an `EMS Repository` folder with `Vendors`, `Contracts`, `W9`, `COI`, `Settlements`, `Imports`, `Archive`.

## Hard rules

1. Split FE/BE. No data tables local to the FE except `tblLocalLink` (BackEndPath).
2. Store document **paths**, never embed files.
3. `tblLocation.LocationCode` is **not unique**. `PIT 101` is two locations. Official codes are spaced (`FB 106`), not Copilot compact (`FB106`).
4. Unique: `LocationName`, `MyVenueCode`, `VendorShortCode`, `AliasName`, `ProductCode`.
5. Rates are decimals (`0.10` = 10%, `0.7` = 70%).
6. Do **not** implement settlement math, PDF, email, or reports in Alpha. Create Volume B tables and named `qry*` objects so the schema stays frozen.
7. Do **not** auto-apply the $200 NPO minimum. Store the contract field and `MIN_DONATION` adjustment type. Copilot’s `Max(calc, min)` idea is not approved.
8. Event status is forward-only: OPEN → FINANCE REVIEW → CLOSED.
9. NPO and SUB are two `VendorType` values in one `tblVendor`.
10. Seed from the CSVs. Do not type demo vendors like “Test NPO 1”.
11. Import Center is an Alpha **shell**. Buttons may MsgBox “Phase 2”. Do not parse MyVenue/tips/assignments.

## Tables to create (all 23)

Lookups: `tblVendorType` `tblEventType` `tblEventStatus` `tblContractClass` `tblAppSetting` `tblAdjustmentType` `tblExceptionType`

Core: `tblVendor` `tblVendorContract` `tblLocation` `tblLocationAlias` `tblCategoryMap` `tblEvent` `tblEventAssignment`

Phase B empty (except adjustment types and exception types seeded): `tblImportBatch` `tblSalesImport` `tblAssignmentImport` `tblTipsImport` `tblSettlementHeader` `tblSettlementDetail` `tblSettlementAdjustment` `tblExceptionLog` `tblDocumentRef`

Number FKs = Long Integer. Money = Currency. Rates = Double.

## Forms to create (Copilot Ch 6)

- `frmDashboard` — Events, Vendors, Locations, Import Center, Settlement Review, Communications, Settings
- `frmVendorList` + `frmVendor` (caption **Vendor Master**; Copilot called this frmVendorMaster — do not create a second form). Tabs: General, Contacts, Contract + `sfrmVendorContract`
- `frmEventList` + `frmEvent` with status advance button; assignment subform if straightforward
- `frmLocationList` + `frmLocation` + `sfrmLocationAlias`
- `frmCategoryMap`
- `frmSettings`
- `frmImportCenter` — Import MyVenue, Import Tips, Import Assignments, Status / Record Count / Exceptions (Phase 2 messages)
- Placeholder forms for Settlement Review / Communications

Queries allowed in Alpha: `qryVendorActive` `qryEventList` `qryLocationList` `qryCategoryMap`.

Also create Volume B named queries (empty-safe SQL from Volume B Ch 12): `qrySalesMapped` `qryLocationResolved` `qryVendorAssigned` `qrySettlementCalculation` `qrySettlementSummary` `qryFinanceReview` `qryExceptionOpen`. Do not wire them to a Generate button in Alpha.

## Seed mapping

CSV columns use names (`VendorType` = NPO/SUB, `MyVenueCode`, `ContractClass`). After import, populate FKs:

- VendorType name → `VendorTypeID`
- MyVenueCode → `LocationID` for aliases
- VendorShortCode → `VendorID` for contracts
- ContractClass name → `ContractClassID` for category map

Yes/No: `1` = Yes, `0` = No.

Expected counts: 81 locations, 228 aliases (skip alias dupes), 10 vendors (DOJ inactive), 8 category codes, 9 exception types, LAG contract 0.70/0.05, SUG 0.80/0.05, ARVC SAP 1013051 BSS 5487, 0 import/settlement rows.

## Done when

A user can open the FE, land on the dashboard, create an event, create a vendor, view locations, manage categories, open Import Center, save, and reopen. Settlement and import buttons may say Phase 2.

## Do not

- Unique-index `LocationCode`
- Collapse PIT 101 A/B into one row
- Recode official FB 113 Mini Melts (official FB 113 is Student Zone; Mini Melts NW is FB 114 via alias)
- Seed compact aliases like `FB106` / `PIT101` (PIT 101 would collide)
- Build Copilot’s single-file `EMS_v1_0.accdb` unless the user explicitly overrides the FE/BE split
- Add sample settlement numbers
- Change GL codes or tax rate 0.07625
- Implement Copilot build steps 8 (Imports) or 9 (Settlement Engine) **logic**. Tables and query objects for those steps **must** exist.

When finished, list the objects you created and the seed row counts.
