# EMS Developer Build Binder v5.0
## Volume A — Foundation Architecture & Access Generation Spec

**Product:** Event Management System (EMS)  
**Owner:** UNM Athletics Hospitality / Levy  
**Sponsor:** Evan E. Gonzales  
**Binder date:** 2026-09-19  
**Purpose:** Sit beside Microsoft Access and build `EMS_BE.accdb` + `EMS_FE.accdb` without inventing fields.

Canonical machine schema: `schema/ems_access_schema.json`  
Fallback DDL: `schema/create_tables_ace.sql`  
Seed: `seed/*.csv`

If this binder and the JSON disagree on a field size, **JSON wins**.

---

## 0. What this pass is

Build the foundation database and the screens needed to enter masters.

**In scope**

- Split Access app (front end / back end)
- All tables listed in the JSON (Phase A and empty Phase B tables)
- Seed data from live UNM files
- Dashboard + Vendor + Event + Location + Category + Settings forms
- Event status `OPEN` → `FINANCE REVIEW` → `CLOSED`

**Out of scope (do not build yet)**

- Settlement calculations
- PDF generation
- Draft Outlook email
- Reports
- MSR import parser / matching engine UI beyond placeholder buttons

**Alpha pass/fail**

1. Open `EMS_FE.accdb` to the dashboard
2. Create an event and save it
3. Create a vendor and save it
4. Open location list and see seeded MyVenue rows
5. Open category map and see eight product codes
6. Close Access, reopen, records still there (data is in the BE)

---

## 1. Constitution (do not violate)

1. Automate administrative work. Do not change how stands actually operate.
2. EMS stores **paths**, not files. Contracts, W-9, COI, settlements, and imports live in the EMS Repository folders.
3. Access bloat is illegal: no embedded spreadsheets, no copied BE per user, no pictures in the database.
4. NPO and SUB share one vendor table and one location table. They do **not** share settlement math.
5. Location matching is by **full MyVenue name / alias**, never by `LocationCode` alone.
6. `$200` NPO minimum is a **manual statement line** in the current Excel/PDF process. Do not auto-apply it in Alpha or in Phase 2 until Finance confirms.

---

## 2. Files to create

### Back end

`EMS_BE.accdb`

Contains tables, relationships, indexes, seed data only. Store on the approved share (network or SharePoint). One BE for the team.

### Front end

`EMS_FE.accdb`

Contains forms, macros, VBA, queries used by UI. Each user gets a copy. All tables are **linked** to `EMS_BE.accdb`.

On FE startup (AutoExec):

1. Confirm linked tables resolve
2. Open `frmDashboard`

If links are broken, open a simple relink dialog (table `tblAppSetting.RepositoryRoot` is not the BE path; keep BE path in a FE local table `USysBEPath` or a named table `tblLocalLink` with one row `BackEndPath`). Create `tblLocalLink` in the FE only:

| Field | Type | Notes |
|---|---|---|
| LinkID | AutoNumber PK | |
| BackEndPath | Short Text 255 | Full path to EMS_BE.accdb |

### Repository (outside Access)

```
EMS Repository/
  Vendors/
  Contracts/
  W9/
  COI/
  Settlements/
  Imports/
  Archive/
```

Create the folders. Do not put them inside the ACCDB.

---

## 3. Construction order

Do this in order. Do not skip ahead to PDFs.

1. Create `EMS_BE.accdb`
2. Create lookup tables, then core tables, then Phase B tables (empty)
3. Relationships window + unique indexes
4. Seed data (`seed/IMPORT_ORDER.md`)
5. Create `EMS_FE.accdb`, link every BE table
6. `frmDashboard` (buttons only, then wire them)
7. `frmVendor` (production-quality)
8. `frmEvent`
9. `frmLocation` with alias subform
10. `frmCategoryMap`
11. `frmSettings`
12. Placeholder forms for Import Center, Settlement Review, Communications (buttons that open “Not in Alpha” message is acceptable)

---

## 4. Naming standards

| Object | Pattern | Example |
|---|---|---|
| Table | `tbl` + noun | `tblVendor` |
| Form | `frm` + noun | `frmVendor` |
| Subform | `sfrm` | `sfrmLocationAlias` |
| Query | `qry` + purpose | `qryVendorActive` |
| Macro | `mcr` | `mcrAutoExec` |
| Module | `mod` | `modApp` |
| Control | `lbl` `txt` `cbo` `cmd` `chk` `sub` | `cboVendorType` |

Invoice number (Phase 2, store the rule now):

```
UNM- & Format([EventDate],"mmddyy") & "-" & [VendorShortCode]
```

Example: `UNM-120125-ARVC`, `UNM-120125-SUG`

PDF file name (Phase 2):

```
Format([EventDate],"mm-dd-yy") & " - " & [EventTypeShort] & " - AP UNM - " & [InvoiceNumber] & ".pdf"
```

Example: `12-01-25 - MBB - AP UNM - UNM-120125-ARVC.pdf`

---

## 5. Locked business facts (from live files, not Copilot chat)

### Vendor types

- **NPO** — nonprofit group. Donation from assigned-location net sales. Tips added. Optional cook fee / min donation / bonus / shortages as manual lines.
- **SUB** — third-party vendor. Vendor-specific rates on food, N/A beverage, beer, liquor. Expenses (card fees, ice) allowed. Gratuities added.

### NPO rates (default)

- Food + non-alcohol net × **10%**
- Alcohol net × **8%**
- Assignment-driven: each Event + Location + Vendor row gets `AllocationPct` of that location’s matched MSR net
- Control: allocations for a location on an event should total **1.00**

NPO donation formula (document only; do not code in Alpha):

```
AllocatedFoodNonAlcNet * FoodRate + AllocatedAlcoholNet * AlcoholRate
```

Food/Non-Alc net = FOOD + NA_BEV  
Alcohol net = BEER + LIQUOR (wine product `313096` is LIQUOR)

### SUB rates (seeded examples from 12/01/25)

| Short | Legal name | Food | N/A Bev | Beer | Liquor | Stand |
|---|---|---|---|---|---|---|
| LAG | Fuego Enterprises LLC | 70% | 5% | 0 | 0 | PIT 107 / 107-LAGUNA |
| SUG | Destiny Marie Maestas | 80% | 5% | 0 | 0 | PIT 103 / 103-SHIVERS |

SUB check formula (document only):

```
net = gross / (1 + TaxRate)
commission = foodNet*FoodRate + naNet*NonAlcoholRate + beerNet*BeerRate + liquorNet*LiquorRate
check = commission - expenses - shortage + gratuities
```

Tax rate in current packets: **7.625%** (`0.07625`).

### Event lifecycle

`OPEN` → `FINANCE REVIEW` → `CLOSED`

Forward only in Alpha. Changing status is a command button on `frmEvent`, not a free combo.

### Category map (locked product codes)

| ProductCode | Description | SUB bucket | NPO class | Default NPO rate |
|---|---|---|---|---|
| 312115 | N/A BEVERAGE SALES - TAXABLE | NA_BEV | FOOD_NONALC | 0.10 |
| 313000 | FOOD SALES - TAXABLE | FOOD | FOOD_NONALC | 0.10 |
| 313004 | LIQUOR SALES - TAXABLE | LIQUOR | ALCOHOL | 0.08 |
| 313082 | BEER PACKAGED SALES | BEER | ALCOHOL | 0.08 |
| 313096 | WINE SALES - TAXABLE | LIQUOR | ALCOHOL | 0.08 |
| FF-312114 | Fan Friendly N/A beverage discount | NA_BEV | FOOD_NONALC | 0.10 |
| FF-313076 | Fan Friendly food discount | FOOD | FOOD_NONALC | 0.10 |
| 353008 | Subcontract income (food%) | FOOD | FOOD_NONALC | 0.10 |

When MyVenue adds a product code, add a row. Never delete; set `Active = No`.

---

## 6. Table catalog

Create **all 20 tables** now. Phase B tables stay empty except `tblAdjustmentType` (seeded).

Phase A (used by Alpha UI):  
`tblVendorType` `tblEventType` `tblEventStatus` `tblContractClass` `tblAppSetting` `tblAdjustmentType` `tblVendor` `tblVendorContract` `tblLocation` `tblLocationAlias` `tblCategoryMap` `tblEvent` `tblEventAssignment`

Phase B (create, no forms except placeholders):  
`tblImportBatch` `tblSalesImport` `tblTipsImport` `tblSettlementHeader` `tblSettlementDetail` `tblSettlementAdjustment` `tblDocumentRef`

Field-by-field definitions are in `schema/ems_access_schema.json`. Below is the Access designer translation for every Alpha table. Use Long Integer for Number FKs. Use Double for rates. Use Currency for money.

### 6.1 tblVendorType

| Field | Type | Size | Required | Indexed | Default | Notes |
|---|---|---|---|---|---|---|
| VendorTypeID | AutoNumber | | PK | PK | | |
| VendorTypeName | Short Text | 50 | Yes | Unique | | NPO, SUB |
| VendorTypeDescription | Short Text | 255 | | | | |

Seed: NPO, SUB.

### 6.2 tblEventType

| Field | Type | Size | Required | Indexed | Notes |
|---|---|---|---|---|---|
| EventTypeID | AutoNumber | | PK | PK | |
| EventTypeName | Short Text | 50 | Yes | Unique | Football, MBB, WBB, Concert, Rental, Special Event, Baseball |
| EventTypeShort | Short Text | 10 | Yes | Unique | FB, MBB, WBB, CON, RNT, SPE, BB |

Baseball is included because MyVenue has `BB 101`. Copilot omitted it.

### 6.3 tblEventStatus

| Field | Type | Size | Required | Default | Notes |
|---|---|---|---|---|---|
| StatusID | AutoNumber | | PK | | |
| StatusName | Short Text | 50 | Yes unique | | OPEN, FINANCE REVIEW, CLOSED |
| StatusSequence | Number | Long | Yes | | 1, 2, 3 |
| IsClosed | Yes/No | | | No | Yes only on CLOSED |

### 6.4 tblContractClass

| Field | Type | Size | Required | Notes |
|---|---|---|---|---|
| ContractClassID | AutoNumber | | PK | |
| ContractClassName | Short Text | 20 | Yes unique | FOOD, NA_BEV, BEER, LIQUOR, IGNORE |
| NPOClass | Short Text | 20 | Yes | FOOD_NONALC, ALCOHOL, IGNORE |
| DefaultNPORate | Double | | Yes default 0 | 0.10 or 0.08 |

### 6.5 tblAppSetting

| Field | Type | Size | Required | Notes |
|---|---|---|---|---|
| SettingID | AutoNumber | | PK | |
| SettingKey | Short Text | 50 | Yes unique | |
| SettingValue | Short Text | 255 | | Store numbers as text; typed by ValueType |
| ValueType | Short Text | 20 | Yes default TEXT | TEXT, DOUBLE, CURRENCY, YESNO |
| Notes | Short Text | 255 | | |

Seed includes tax rate, CID 241, GL codes from the 12/01/25 PDFs, default preparer/reviewer/approver names.

### 6.6 tblVendor

| Field | Type | Size | Required | Indexed | Default | Notes |
|---|---|---|---|---|---|---|
| VendorID | AutoNumber | | PK | PK | | |
| VendorName | Short Text | 255 | Yes | Yes | | Legal name |
| VendorShortCode | Short Text | 25 | Yes | Unique | | ARVC, LAG, SUG. Join key to Excel. |
| VendorTypeID | Number | Long | Yes | FK | | |
| SAPID | Short Text | 50 | | | | |
| BSSID | Short Text | 50 | | | | |
| CheckPayableTo | Short Text | 255 | | | | Statement payee |
| PrimaryContact | Short Text | 255 | | | | |
| Phone | Short Text | 50 | | | | |
| EmailAddress | Short Text | 255 | | | | |
| CCEmailAddress | Short Text | 255 | | | | |
| Address1 | Short Text | 255 | | | | Required for SUB statements |
| City | Short Text | 100 | | | | |
| State | Short Text | 2 | | | | |
| PostalCode | Short Text | 10 | | | | |
| Active | Yes/No | | Yes | | Yes | |
| W9Path | Short Text | 255 | | | | Path only |
| COIPath | Short Text | 255 | | | | |
| ContractPath | Short Text | 255 | | | | |
| Notes | Long Text | | | | | Standing notes |
| CreatedDate | Date/Time | | | | Now() | |
| CreatedBy | Short Text | 50 | | | | |
| ModifiedDate | Date/Time | | | | | |
| ModifiedBy | Short Text | 50 | | | | |

Combo on VendorTypeID: display `VendorTypeName`, store `VendorTypeID`.

### 6.7 tblVendorContract

| Field | Type | Required | Default | Validation | Notes |
|---|---|---|---|---|---|
| ContractID | AutoNumber PK | | | | |
| VendorID | Number FK | Yes | | | |
| FoodRate | Double | Yes | 0 | 0–1 | 70% = 0.7 |
| NonAlcoholRate | Double | Yes | 0 | 0–1 | |
| BeerRate | Double | Yes | 0 | 0–1 | |
| LiquorRate | Double | Yes | 0 | 0–1 | |
| MinimumDonation | Currency | | | | NPO 200; SUB Null |
| AllowExpenses | Yes/No | | No | | SUB Yes |
| CardFeeMaxRate | Double | | 0 | | SUB 0.03 |
| EffectiveDate | Date/Time | | Date() | | |
| ExpirationDate | Date/Time | | | | |
| Active | Yes/No | | Yes | | |
| Notes | Long Text | | | | |

One active contract per vendor is enough for Alpha. Seed one row per vendor.

### 6.8 tblLocation — read this twice

`LocationCode` is **not unique**.

MyVenue 9/14/26 has two rows that both start with `PIT 101`:

- `PIT 101 - A - POP & POUR (Q)` (MyVenueCode 31)
- `PIT 101 - B - NACHOMAMA (R)` (MyVenueCode 32)

If you unique-index `LocationCode`, the database is wrong.

| Field | Type | Size | Required | Indexed | Notes |
|---|---|---|---|---|---|
| LocationID | AutoNumber | | PK | PK | |
| MyVenueCode | Number | Long | Yes | Unique | Numeric Code from MyVenue export |
| LocationName | Short Text | 255 | Yes | Unique | Full name `FB 106 - RED RALLY NORTH EAST` |
| LocationCode | Short Text | 50 | Yes | Duplicates OK | `FB 106`, `PIT 101` |
| LocationDescription | Short Text | 255 | | | After first ` - ` |
| Venue | Short Text | 100 | | Yes | Football Stadium, The Pit, Baseball, Other |
| Department | Short Text | 100 | | | e.g. 36127 - CONCESSIONS |
| Menu | Short Text | 255 | | | |
| POSProfile | Short Text | 100 | | | |
| Family | Short Text | 255 | | | |
| PriceLevel | Short Text | 50 | | | |
| IsWarehouse | Yes/No | | | | Default No |
| Active | Yes/No | | | | No for ZZZ, warehouse, AA |
| Notes | Long Text | | | | |

81 seed rows. 68 active.

### 6.9 tblLocationAlias

| Field | Type | Size | Required | Indexed | Notes |
|---|---|---|---|---|---|
| AliasID | AutoNumber | | PK | | |
| LocationID | Number FK | | Yes | Yes | Cascade delete |
| AliasName | Short Text | 255 | Yes | Unique | Exact match string for MSR / Excel |
| AliasType | Short Text | 25 | | | OFFICIAL, CODE, MSR, NPO_TEMPLATE, LEGACY_NPO |
| Notes | Short Text | 255 | | | |

Import matching rule (Phase 2): `AliasName` equals the incoming location string, trimmed, case-insensitive. If zero hits → `UNMATCHED_LOCATION`. If you ever get two hits, the unique index already prevented it.

**Required alias corrections** (already in seed):

| Legacy (NPO V4) | Official 9/14/26 |
|---|---|
| `FB 113 - MBP - MINI MELTS (NW)` | `FB 114 - MBP - MINI MELTS (NW)` |
| `FB 113B - MBP - MINI MELTS (NE)` | `FB 115 - MBP - MINI MELTS (NE)` |

Official `FB 113` is Student Zone, not Mini Melts. Do not “fix” this by changing LocationCode on the official row.

### 6.10 tblCategoryMap

| Field | Type | Size | Required | Notes |
|---|---|---|---|---|
| CategoryMapID | AutoNumber PK | | | |
| ProductCode | Short Text 25 | | Yes unique | |
| ProductDescription | Short Text 255 | | Yes | |
| ContractClassID | Number FK | | Yes | |
| DefaultRate | Double | | Yes | |
| Active | Yes/No | | | Default Yes |
| Notes | Short Text 255 | | | |

### 6.11 tblEvent

| Field | Type | Size | Required | Default | Notes |
|---|---|---|---|---|---|
| EventID | AutoNumber PK | | | | |
| EventDate | Date/Time | | Yes indexed | | |
| EventName | Short Text | 255 | Yes | | Football, MBB - NM HIGHLANDS |
| InternalEventName | Short Text | 255 | | | MEN'S BASKETBALL |
| EventTypeID | Number FK | | Yes | | |
| StatusID | Number FK | | Yes | 1 (OPEN) | |
| TaxRate | Double | | Yes | 0.07625 | |
| Notes | Long Text | | | | |
| CreatedDate | Date/Time | | | Now() | |
| CreatedBy | Short Text | 50 | | | |
| ModifiedDate | Date/Time | | | | |
| ModifiedBy | Short Text | 50 | | | |
| ClosedDate | Date/Time | | | | Set when status becomes CLOSED |

Do not unique-index date+name yet. Same-day football + concert is possible.

### 6.12 tblEventAssignment

Create the table. A full assignment UI can be a datasheet subform on `frmEvent` if time allows; otherwise leave it for the next pass, but **the table must exist**.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| AssignmentID | AutoNumber PK | | | |
| EventID | Number FK | Yes | | Cascade delete with event |
| LocationID | Number FK | Yes | | |
| VendorID | Number FK | Yes | | |
| AllocationPct | Double | Yes | 1 | 0 through 1 |
| PayeeSeq | Number | | | Statement line order per vendor |
| AssignmentStatus | Short Text 50 | | PROOF / INITIAL LOAD | |
| Notes | Long Text | | | |

Unique: EventID + LocationID + VendorID.

### 6.13 Phase B tables

Create with JSON field lists. No calc, no UI except placeholder buttons.

`tblSettlementHeader.InvoiceNumber` unique. Also unique EventID+VendorID.

`tblSalesImport.LocationID` and `ContractClassID` FKs are **not enforced**, so unmatched import rows can be stored.

---

## 7. Forms

Access theme: keep it operational (Levy/UNM finance), not a marketing site. White/light gray, navy headers are fine. No giant hero images.

### frmDashboard

Unbound. Seven buttons, two columns.

| Button | Opens |
|---|---|
| Events | `frmEventList` then `frmEvent` |
| Vendors | `frmVendorList` then `frmVendor` |
| Locations | `frmLocationList` then `frmLocation` |
| Import Center | Placeholder |
| Settlement Review | Placeholder |
| Communications | Placeholder |
| Settings | `frmSettings` |

Optional header labels (from settings): company name, “EMS v1.0”, BE path.

### frmVendor / frmVendorList

`frmVendorList`: continuous or datasheet of active+inactive with search box on name/short code, New / Open / Close.

`frmVendor`: single form, Record Source `tblVendor`.

**Tab 1 General**

- VendorName, VendorShortCode, VendorTypeID, Active
- SAPID, BSSID, CheckPayableTo
- Notes

**Tab 2 Contacts**

- PrimaryContact, Phone, EmailAddress, CCEmailAddress
- Address1, City, State, PostalCode

**Tab 3 Contract**

- Subform `sfrmVendorContract` bound to `tblVendorContract` (Link Child/Master VendorID)
- Show FoodRate, NonAlcoholRate, BeerRate, LiquorRate as percent format
- MinimumDonation, AllowExpenses, CardFeeMaxRate, EffectiveDate, ExpirationDate, Active
- W9Path, COIPath, ContractPath on the parent (or this tab) with a button that does `Application.FollowHyperlink` if path is not blank. No file attach.

Before update: VendorShortCode required, no spaces-only. Duplicate short code must fail on unique index with a readable message.

Deactivate = `Active = No`. Do not delete vendors that have assignments.

### frmEvent / frmEventList

List: date desc, name, type, status.

`frmEvent` fields: EventDate, EventName, InternalEventName, EventTypeID, TaxRate, Notes. Status is displayed read-only plus:

- `cmdAdvanceStatus` — OPEN to FINANCE REVIEW, or FINANCE REVIEW to CLOSED
- Confirm on CLOSED; set ClosedDate = Date()

Optional subform `sfrmEventAssignment` (datasheet): Location (combo on LocationName, only Active), Vendor (combo on ShortCode + Name), AllocationPct, PayeeSeq, Notes.

Location combo Row Source:

```sql
SELECT LocationID, LocationName, LocationCode, Venue
FROM tblLocation
WHERE Active = True
ORDER BY Venue, LocationCode, LocationName;
```

Column widths: 0"; 2.8"; 0.8"; 1.2"

### frmLocation / frmLocationList

List filterable by Venue and Active. Show LocationCode, LocationName, Venue, Department, Active.

`frmLocation`: all tblLocation fields except Autonumber displayed as locked. Subform `sfrmLocationAlias` (AliasName, AliasType, Notes).

Button `cmdAddAlias` focuses the subform new record.

Do not allow LocationCode-only uniqueness checks.

### frmCategoryMap

Datasheet or continuous form on `tblCategoryMap` joined to `tblContractClass` for class name. Allow add/edit. Deactivate instead of delete.

### frmSettings

Continuous or single form over `tblAppSetting`. Key read-only, value editable. Include RepositoryRoot.

---

## 8. Light VBA (Alpha only)

Module `modApp`:

```vb
Public Function NextEventStatus(ByVal currentStatusID As Long) As Long
    ' 1 -> 2, 2 -> 3, 3 -> 0 (already closed)
End Function

Public Function FormatInvoiceNumber(ByVal eventDate As Date, ByVal shortCode As String) As String
    FormatInvoiceNumber = "UNM-" & Format(eventDate, "mmddyy") & "-" & shortCode
End Function
```

Do not call invoice formatting from Alpha UI except maybe a disabled preview label.

`modRelink` (FE): if any linked table is broken, prompt for `EMS_BE.accdb` and relink all.

No settlement modules.

---

## 9. Seed expectations after import

| Table | Rows |
|---|---|
| tblVendorType | 2 |
| tblEventType | 7 |
| tblEventStatus | 3 |
| tblContractClass | 5 |
| tblAppSetting | 22 |
| tblAdjustmentType | 22 |
| tblCategoryMap | 8 |
| tblVendor | 10 (8 NPO, 2 SUB; DOJ inactive) |
| tblVendorContract | 10 |
| tblLocation | 81 |
| tblLocationAlias | 228 (skip dupes if unique index hits) |

ARVC SAP `1013051` BSS `5487` came from the 12/01/25 NPO PDF, not from NPO MASTER (those cells were blank).

LAG / SUG addresses and rates came from the SUB 12/01/25 workbook.

---

## 10. Known traps (the reason Copilot’s Access design would have failed)

1. **PIT 101 is two locations.** Unique `LocationCode` is a defect.
2. **Mini Melts codes drifted** between NPO V4 and the 9/14/26 MyVenue list. Aliases are mandatory on day one.
3. **NPO math ≠ SUB math.** One vendor table, two later engines.
4. **$200 minimum is not in the Excel donation formula.** It is a yellow statement cell.
5. **MSR location strings must match aliases exactly.** `FB 107 - NE SPECIALTY - DAWG HOUSE` vs `NE SPECIALTY DAWG O.G.` are different strings; both need aliases.
6. **Invoice live pattern is `UNM-MMDDYY-SHORTCODE`**, not the Copilot PDF-only naming line. Store both rules.
7. **PIT 107 Laguna** has POS Profile `UNM FOOTBALL STADIUM` in MyVenue. Store as exported; Venue can still be The Pit if LocationCode starts with PIT. Seed script used POS Profile first, then code prefix. If Venue looks wrong on a SUB stand, prefer LocationCode prefix in a later data fix — do not block Alpha.
8. Ray’s last name appears as Velasquez and Valasquez on source PDFs. Settings use **Velasquez**.

---

## 11. Placeholder screens

Import Center, Settlement Review, Communications:

Unbound form, title, one sentence (“Phase 2 — not in Alpha”), Close button. Dashboard buttons may open these so navigation can be validated.

---

## 12. Phase 2 math (reference only — do not implement)

### NPO, per assignment row

Match MSR `LocationRaw` to `tblLocationAlias.AliasName` → `LocationID`.  
Sum `NetAmt` by ContractClass.  
`FoodNonAlcNet = FOOD + NA_BEV`  
`AlcoholNet = BEER + LIQUOR`  
Apply `AllocationPct`.  
`Donation = FoodNonAlcNet * FoodRate + AlcoholNet * AlcoholRate`  
Add tips from `tblTipsImport` for same event+vendor+location.  
Add `tblSettlementAdjustment` rows (cook fee, min donation, bonus, shortages).

Status flags copied from Excel:

- Missing allocation
- `Abs(Sum(AllocationPct for Event+Location) - 1) > 0.0001` → REVIEW LOCATION ALLOCATION
- No MSR sales → NO MSR SALES
- Else OK

### SUB, per vendor/event

Not assignment-split in the 12/01/25 workbook: one stand code per vendor tab. Still store LocationID on the header or a single detail row.  
Gross from inventory/MyVenue, strip tax at event TaxRate, apply four contract rates, subtract expenses, add gratuities.

GL split already seeded in `tblAppSetting` and `tblAdjustmentType`.

---

## 13. Acceptance checklist (print this)

- [ ] `EMS_BE.accdb` exists and is the only copy of tables
- [ ] `EMS_FE.accdb` has no local copies of data tables
- [ ] Relationships match `schema/RELATIONSHIPS.md`
- [ ] `LocationCode` is **not** unique
- [ ] `LocationName` and `MyVenueCode` are unique
- [ ] `AliasName` is unique
- [ ] 81 locations loaded; ZZZ/warehouse/AA inactive
- [ ] Alias exists mapping Mini Melts NW legacy FB 113 → official FB 114
- [ ] 10 vendors loaded; DOJ inactive; ARVC has SAP/BSS
- [ ] LAG 0.70 / 0.05 and SUG 0.80 / 0.05 contracts loaded
- [ ] Dashboard opens on FE start
- [ ] Can create event in OPEN, advance to FINANCE REVIEW, then CLOSED
- [ ] Can create vendor NPO and SUB
- [ ] Can add a location alias
- [ ] Can add a category map row
- [ ] No settlement, PDF, or email code

---

## 14. What the next binder (Volume B) will add

Do not do this now:

- MSR CSV parser for the nested “Location: / product Total:” export
- Assignment import
- Tips import
- NPO engine + exception statuses
- SUB engine + expense lines
- Statement forms matching the ARVC NPO PDF and SUG SUB PDF
- PDF export to `EMS Repository/Settlements/`
- Draft email with PDF path in body
- Finance Review / Close event guards (“all settlements APPROVED”)
