# Paste this into the Access-building tool

You are generating a **Microsoft Access** application for UNM Athletics Hospitality / Levy.

This environment can create `.accdb` files. Follow the attached EMS package. Do not invent tables, fields, or rates.

## Attached / required files

Read in this order:

1. `ems/EMS_Developer_Build_Binder_Volume_A.md`
2. `ems/schema/ems_access_schema.json`
3. `ems/schema/RELATIONSHIPS.md`
4. `ems/seed/IMPORT_ORDER.md`
5. Every CSV in `ems/seed/` except `location_alias_conflicts.csv` (docs only)
6. `ems/schema/create_tables_ace.sql` only if you can run ACE SQL; otherwise use Table Designer from the JSON

JSON is the canonical field list. If you would like to “improve” the schema, **don’t**. File a note instead.

## Create these two files

- `EMS_BE.accdb` — tables, relationships, indexes, seed data
- `EMS_FE.accdb` — linked tables + forms + AutoExec to `frmDashboard`

Put them wherever the user asks. Default: a folder named `EMS` next to an `EMS Repository` folder with `Vendors`, `Contracts`, `W9`, `COI`, `Settlements`, `Imports`, `Archive`.

## Hard rules

1. Split FE/BE. No data tables local to the FE except `tblLocalLink` (BackEndPath).
2. Store document **paths**, never embed files.
3. `tblLocation.LocationCode` is **not unique**. `PIT 101` is two locations.
4. Unique: `LocationName`, `MyVenueCode`, `VendorShortCode`, `AliasName`, `ProductCode`.
5. Rates are decimals (`0.10` = 10%, `0.7` = 70%).
6. Do **not** implement settlement math, PDF, email, or reports.
7. Do **not** auto-apply the $200 NPO minimum.
8. Event status is forward-only: OPEN → FINANCE REVIEW → CLOSED.
9. NPO and SUB are two `VendorType` values in one `tblVendor`.
10. Seed from the CSVs. Do not type demo vendors like “Test NPO 1”.

## Tables to create (all of them)

Lookups: `tblVendorType` `tblEventType` `tblEventStatus` `tblContractClass` `tblAppSetting` `tblAdjustmentType`

Core: `tblVendor` `tblVendorContract` `tblLocation` `tblLocationAlias` `tblCategoryMap` `tblEvent` `tblEventAssignment`

Phase B empty (except adjustment types seeded): `tblImportBatch` `tblSalesImport` `tblTipsImport` `tblSettlementHeader` `tblSettlementDetail` `tblSettlementAdjustment` `tblDocumentRef`

Number FKs = Long Integer. Money = Currency. Rates = Double.

## Forms to create

- `frmDashboard` — Events, Vendors, Locations, Import Center, Settlement Review, Communications, Settings
- `frmVendorList` + `frmVendor` (tabs: General, Contacts, Contract + `sfrmVendorContract`)
- `frmEventList` + `frmEvent` with status advance button; assignment subform if straightforward
- `frmLocationList` + `frmLocation` + `sfrmLocationAlias`
- `frmCategoryMap`
- `frmSettings`
- Placeholder forms for Import / Settlement / Communications

## Seed mapping

CSV columns use names (`VendorType` = NPO/SUB, `MyVenueCode`, `ContractClass`). After import, populate FKs:

- VendorType name → `VendorTypeID`
- MyVenueCode → `LocationID` for aliases
- VendorShortCode → `VendorID` for contracts
- ContractClass name → `ContractClassID` for category map

Yes/No: `1` = Yes, `0` = No.

Expected counts: 81 locations, 228 aliases (skip alias dupes), 10 vendors (DOJ inactive), 8 category codes, LAG contract 0.70/0.05, SUG 0.80/0.05, ARVC SAP 1013051 BSS 5487.

## Done when

A user can open the FE, land on the dashboard, create an event, create a vendor, view locations, manage categories, save, and reopen. Settlement buttons may say Phase 2.

## Do not

- Unique-index `LocationCode`
- Collapse PIT 101 A/B into one row
- Recode official FB 113 Mini Melts (official FB 113 is Student Zone; Mini Melts NW is FB 114 via alias)
- Build Copilot’s single-file `EMS_v1_0.accdb` unless the user explicitly overrides the FE/BE split
- Add sample settlement numbers
- Change GL codes or tax rate 0.07625

When finished, list the objects you created and the seed row counts.
