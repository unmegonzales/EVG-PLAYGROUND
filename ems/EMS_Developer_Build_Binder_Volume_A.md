# EMS Developer Build Binder v6.0
## Volume A — Foundation Architecture & User Interface

**Product:** Event Management System (EMS)  
**Owner:** UNM Athletics Hospitality / Levy  
**Sponsor:** Evan E. Gonzales  
**Binder date:** 2026-09-19  
**Chapter map:** Copilot Developer Build Binder v4.0 Volume A  
**Purpose:** Sit beside Microsoft Access and build `EMS_BE.accdb` + `EMS_FE.accdb` without inventing fields.

Canonical machine schema: `schema/ems_access_schema.json`  
Fallback DDL: `schema/create_tables_ace.sql`  
Seed: `seed/*.csv`  
Copilot v4.0 diff: `COPILOT_V4_CROSSWALK.md`

If this binder and the JSON disagree on a field size, **JSON wins**.

---

## How to use this Volume A

1. Paste `prompts/ACCESS_GENERATOR_PROMPT.md` into the Access-building tool.
2. Walk **Chapters 1–7** in order. That is Copilot’s Volume A.
3. Create every table in the JSON (Phase A + empty Phase B). Seed from CSVs.
4. Stop before settlement math. Volume B is the engine.

---

## 0. What this pass is

Build the foundation database and the screens needed to enter masters.

**In scope (Alpha)**

- Split Access app (front end / back end)
- All tables listed in the JSON (Phase A used; Phase B created empty)
- Seed data from live UNM files
- Dashboard + Vendor Master + Event + Location + Category + Settings
- Import Center / Settlement Review / Communications as **shells** (Copilot Ch 6)
- Event status `OPEN` → `FINANCE REVIEW` → `CLOSED`

**Out of scope (do not build yet)**

- Settlement calculations
- PDF generation
- Draft Outlook email
- Reports
- Working Import MyVenue / Import Tips / Import Assignments parsers

**Alpha pass/fail**

1. Open `EMS_FE.accdb` to the dashboard
2. Create an event and save it
3. Create a vendor and save it
4. Open location list and see seeded MyVenue rows
5. Open category map and see eight product codes
6. Open Import Center and see the Copilot buttons (they may say Phase 2)
7. Close Access, reopen, records still there (data is in the BE)

---

## Constitution (do not violate)

1. Automate administrative work. Do not change how stands actually operate.
2. EMS stores **paths**, not files. Contracts, W-9, COI, settlements, and imports live in the EMS Repository folders.
3. Access bloat is illegal: no embedded spreadsheets, no copied BE per user, no pictures in the database.
4. NPO and SUB share one vendor table and one location table. They do **not** share settlement math.
5. Location matching is by **full MyVenue name / alias**, never by `LocationCode` alone.
6. `$200` NPO minimum is a **manual statement line** in the current Excel/PDF process. Store `MinimumDonation` and `MIN_DONATION` adjustment type. Do **not** auto-apply in Alpha or Volume B until Finance confirms.

---

## Naming standards

| Object | Pattern | Example |
|---|---|---|
| Table | `tbl` + noun | `tblVendor` |
| Form | `frm` + noun | `frmVendor` |
| Subform | `sfrm` | `sfrmLocationAlias` |
| Query | `qry` + purpose | `qryVendorActive` |
| Macro | `mcr` | `mcrAutoExec` |
| Module | `mod` | `modApp` |
| Control | `lbl` `txt` `cbo` `cmd` `chk` `sub` | `cboVendorType` |

Copilot v4.0 named the vendor screen `frmVendorMaster`. **Object name is `frmVendor`.** Caption may read Vendor Master. Do not create a second form.

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

# Chapter 1 — System Architecture

Copilot v4.0: Front-End / Back-End Design. EMS stores paths. EMS does NOT store files.

## 1.1 EMS Front-End

**File:** `EMS_FE.accdb`  
**Copy:** one per user.

| Copilot said FE contains | Alpha |
|---|---|
| Forms | Yes — dashboard, masters, shells |
| Reports | **None.** Collection exists; Volume B |
| Queries | List queries only (`qryVendorActive`, `qryEventList`, `qryLocationList`, `qryCategoryMap`) |
| Macros | `mcrAutoExec` |
| VBA | `modApp`, `modRelink` only |
| Navigation | Dashboard buttons |
| UI | Operational Levy/UNM finance look |

All data tables are **linked** to `EMS_BE.accdb`. The only local FE table is `tblLocalLink`:

| Field | Type | Notes |
|---|---|---|
| LinkID | AutoNumber PK | |
| BackEndPath | Short Text 255 | Full path to `EMS_BE.accdb` |

On FE startup (AutoExec):

1. Confirm linked tables resolve
2. Open `frmDashboard`

If links are broken, open a simple relink dialog. `tblAppSetting.RepositoryRoot` is **not** the BE path.

## 1.2 EMS Back-End

**File:** `EMS_BE.accdb`  
**Copy:** one shared file on the approved network / SharePoint location.

| Copilot said BE contains | This package |
|---|---|
| Tables | All 23 tables in the JSON |
| Relationships | `schema/RELATIONSHIPS.md` |
| Import staging data | Empty Phase B: `tblImportBatch` `tblSalesImport` `tblAssignmentImport` `tblTipsImport` |
| Historical data | Empty Phase B: settlement + `tblDocumentRef` |
| Exception staging | Seed `tblExceptionType`; `tblExceptionLog` empty |

No forms in the BE. Seed lookup/vendor/location/category data into the BE.

## 1.3 Repository (outside Access)

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

Copilot v4.0 listed Contracts, COI, W9, Settlements, Imports, Archive. **Vendors/** is also required (Action Plan Directive 2). Create the folders. Do not put them inside the ACCDB.

---

# Chapter 2 — Lookup Tables

Copilot v4.0: create these first. Seed `NPO`/`SUB`, six event types, three statuses.

Create **all lookup tables below** before core tables. Copilot listed three; Access also needs contract class, settings, and adjustment types.

## 2.1 tblVendorType

Purpose: vendor classifications.

| Field | Type | Size | Required | Indexed | Notes |
|---|---|---|---|---|---|
| VendorTypeID | AutoNumber | | PK | PK | |
| VendorTypeName | Short Text | 50 | Yes | Unique | NPO, SUB |
| VendorTypeDescription | Short Text | 255 | | | |

Seed:

| VendorTypeName | Description |
|---|---|
| NPO | Nonprofit group settlement (donation + tips) |
| SUB | Subcontractor / third-party vendor commission |

## 2.2 tblEventType

| Field | Type | Size | Required | Indexed | Notes |
|---|---|---|---|---|---|
| EventTypeID | AutoNumber | | PK | PK | |
| EventTypeName | Short Text | 50 | Yes | Unique | Football, MBB, WBB, Concert, Rental, Special Event, Baseball |
| EventTypeShort | Short Text | 10 | Yes | Unique | FB, MBB, WBB, CON, RNT, SPE, BB |

Copilot v4.0 omitted Baseball. MyVenue has `BB 101`. Include it.

## 2.3 tblEventStatus

| Field | Type | Size | Required | Default | Notes |
|---|---|---|---|---|---|
| StatusID | AutoNumber | | PK | | |
| StatusName | Short Text | 50 | Yes unique | | OPEN, FINANCE REVIEW, CLOSED |
| StatusSequence | Number | Long | Yes | | 1, 2, 3 |
| IsClosed | Yes/No | | | No | Yes only on CLOSED |

Workflow (forward only in Alpha):

```
OPEN
  ↓
FINANCE REVIEW
  ↓
CLOSED
```

## 2.4 tblContractClass (Copilot omitted; required)

Category map and SUB buckets need a real lookup. Do **not** store `FOOD_NONALC` as the only class on `tblCategoryMap`.

| Field | Type | Size | Required | Notes |
|---|---|---|---|---|
| ContractClassID | AutoNumber | | PK | |
| ContractClassName | Short Text | 20 | Yes unique | FOOD, NA_BEV, BEER, LIQUOR, IGNORE |
| NPOClass | Short Text | 20 | Yes | FOOD_NONALC, ALCOHOL, IGNORE |
| DefaultNPORate | Double | | Yes default 0 | 0.10 or 0.08 |

NPO still rolls FOOD + NA_BEV → FOOD_NONALC @ 10% and BEER + LIQUOR → ALCOHOL @ 8%. Wine product `313096` is LIQUOR.

## 2.5 tblAppSetting

| Field | Type | Size | Required | Notes |
|---|---|---|---|---|
| SettingID | AutoNumber | | PK | |
| SettingKey | Short Text | 50 | Yes unique | |
| SettingValue | Short Text | 255 | | Store numbers as text; typed by ValueType |
| ValueType | Short Text | 20 | Yes default TEXT | TEXT, DOUBLE, CURRENCY, YESNO |
| Notes | Short Text | 255 | | |

Seed includes tax rate 0.07625, CID 241, GL codes from the 12/01/25 PDFs, default preparer/reviewer/approver names, `NPOMinimumDonation=200` with note **do not auto-apply**.

## 2.6 tblAdjustmentType

Seeded now so Volume B does not invent GL lines. Alpha has no adjustment UI.

---

# Chapter 3 — Core Table Specifications

Copilot v4.0: `tblEvent`, `tblVendor`, `tblLocation`, `tblLocationAlias`.

## 3.1 tblEvent

Purpose: one event. Copilot examples: EventDate `09/05/2026`, EventName `Football` / `NMAA BBALL 2026`. Live SUB packet used `MBB - NM HIGHLANDS`.

| Field | Type | Size | Required | Default | Notes |
|---|---|---|---|---|---|
| EventID | AutoNumber PK | | | | Indexed |
| EventDate | Date/Time | | Yes indexed | | |
| EventName | Short Text | 255 | Yes | | Football, NMAA BBALL 2026 |
| InternalEventName | Short Text | 255 | | | MEN'S BASKETBALL |
| EventTypeID | Number FK | | Yes | | |
| StatusID | Number FK | | Yes | 1 (OPEN) | |
| TaxRate | Double | | Yes | 0.07625 | Live packets |
| Notes | Long Text | | | | |
| CreatedDate | Date/Time | | | Now() | |
| CreatedBy | Short Text | 50 | | | |
| ModifiedDate | Date/Time | | | | |
| ModifiedBy | Short Text | 50 | | | |
| ClosedDate | Date/Time | | | | Set when status becomes CLOSED |

Do not unique-index date+name yet. Same-day football + concert is possible.

## 3.2 tblVendor

Purpose: master vendor repository for NPOs and subcontractors.

Copilot examples: Albuquerque Rebels Volleyball Club / Fuego Enterprises LLC; short codes ARVC, DCVA, LAG, SUG.

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

## 3.3 tblLocation — read this twice

Purpose: master inventory of locations.

`LocationCode` is **not unique**.

MyVenue 9/14/26 has two rows that both start with `PIT 101`:

- `PIT 101 - A - POP & POUR (Q)` (MyVenueCode 31)
- `PIT 101 - B - NACHOMAMA (R)` (MyVenueCode 32)

If you unique-index `LocationCode`, the database is wrong.

Copilot v4.0 examples `FB106` `PIT104` `FB151` are compact. Official values are spaced (`FB 106`). Do **not** seed compact codes as unique aliases — `PIT101` would hit two stands.

| Field | Type | Size | Required | Indexed | Notes |
|---|---|---|---|---|---|
| LocationID | AutoNumber | | PK | PK | |
| MyVenueCode | Number | Long | Yes | Unique | Numeric Code from MyVenue export |
| LocationName | Short Text | 255 | Yes | Unique | Full name `FB 106 - RED RALLY NORTH EAST` |
| LocationCode | Short Text | 50 | Yes | Duplicates OK | `FB 106`, `PIT 101` |
| LocationDescription | Short Text | 255 | | | After first ` - ` (Copilot: RED RALLY NORTH EAST, BURQUE BREWS) |
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

## 3.4 tblLocationAlias

Purpose: protect imports from naming changes.

Copilot v4.0 example (already in seed):

- `FB 120 - MBP N. SCOREBOARD` (NPO template)
- `FB 120 - MBP N. SCOREBOARD WEST NO.1` (official)  
same `LocationID`.

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

## 3.5 tblEventAssignment (not in Copilot Ch 3; table must exist)

Create the table. A full assignment UI can be a datasheet subform on `frmEvent` if time allows; otherwise leave it for the next pass, but **the table must exist**. Copilot’s Volume B `tblAssignmentImport` is the *staging* table (empty, Chapter 7 / Appendix A). Posted rows belong here.

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

---

# Chapter 4 — Category Mapping Engine

Copilot v4.0: maps MyVenue product codes. Allowed Copilot classes were `FOOD_NONALC` / `ALCOHOL`. Live MSR needs four SUB buckets; NPO still rolls to those two classes via `tblContractClass.NPOClass`.

## 4.1 tblCategoryMap

| Field | Type | Size | Required | Notes |
|---|---|---|---|---|
| CategoryMapID | AutoNumber PK | | | |
| ProductCode | Short Text 25 | | Yes unique | Indexed |
| ProductDescription | Short Text 255 | | Yes | FOOD SALES - TAXABLE, LIQUOR SALES - TAXABLE |
| ContractClassID | Number FK | | Yes | Not a free-text ContractClass column |
| DefaultRate | Double | | Yes | 0.10 or 0.08 |
| Active | Yes/No | | | Default Yes |
| Notes | Short Text 255 | | | |

When MyVenue adds a product code, add a row. Never delete; set `Active = No`.

## 4.2 Locked product codes

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

---

# Chapter 5 — Contract Table

Copilot v4.0: holds settlement logic. Create the table and seed rates. **Do not code settlement in Alpha.**

## 5.1 tblVendorContract

| Field | Type | Required | Default | Validation | Notes |
|---|---|---|---|---|---|
| ContractID | AutoNumber PK | | | | |
| VendorID | Number FK | Yes | | | |
| FoodRate | Double | Yes | 0 | 0–1 | 70% = 0.7 |
| NonAlcoholRate | Double | Yes | 0 | 0–1 | |
| BeerRate | Double | Yes | 0 | 0–1 | |
| LiquorRate | Double | Yes | 0 | 0–1 | |
| MinimumDonation | Currency | | | | Copilot: NPO 200, SUB NULL. Store it. Do **not** auto-apply |
| AllowExpenses | Yes/No | | No | | SUB Yes |
| CardFeeMaxRate | Double | | 0 | | SUB 0.03 |
| EffectiveDate | Date/Time | | Date() | | |
| ExpirationDate | Date/Time | | | | |
| Active | Yes/No | | Yes | | |
| Notes | Long Text | | | | |

One active contract per vendor is enough for Alpha. Seed one row per vendor.

## 5.2 Locked business facts (from live files)

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

---

# Chapter 6 — Form Architecture

Copilot v4.0 screens: Dashboard, Vendor Master, Event, Location, Import Center.

Access theme: operational (Levy/UNM finance), not a marketing site. White/light gray, navy headers are fine. No giant hero images.

## 6.1 frmDashboard

Unbound. Seven buttons, two columns.

| Button | Opens |
|---|---|
| Events | `frmEventList` then `frmEvent` |
| Vendors | `frmVendorList` then `frmVendor` (caption Vendor Master) |
| Locations | `frmLocationList` then `frmLocation` |
| Import Center | `frmImportCenter` (Alpha shell) |
| Settlement Review | Placeholder |
| Communications | Placeholder |
| Settings | `frmSettings` |

Optional header labels (from settings): company name, “EMS v1.0”, BE path.

## 6.2 frmVendor / frmVendorList (Copilot: frmVendorMaster)

Functions Copilot listed: Add Vendor, Edit Vendor, Deactivate Vendor.

`frmVendorList`: continuous or datasheet of active+inactive with search box on name/short code, New / Open / Close.

`frmVendor`: single form, Record Source `tblVendor`. Caption **Vendor Master**.

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

## 6.3 frmEvent / frmEventList

Functions Copilot listed: Create Event, Edit Event, Move Status.

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

## 6.4 frmLocation / frmLocationList

Functions Copilot listed: Add, Modify, Add Alias.

List filterable by Venue and Active. Show LocationCode, LocationName, Venue, Department, Active.

`frmLocation`: all tblLocation fields except Autonumber displayed as locked. Subform `sfrmLocationAlias` (AliasName, AliasType, Notes).

Button `cmdAddAlias` focuses the subform new record.

Do not allow LocationCode-only uniqueness checks.

## 6.5 frmImportCenter (Copilot Ch 6 — Alpha shell only)

Copilot v4.0 put this in Volume A with:

- Button **Import MyVenue**
- Button **Import Tips**
- Displays: Import Status, Record Count, Exceptions

Build the form. **Do not parse files.**

Unbound form. Caption: Import Center.

| Control | Type | Alpha behavior |
|---|---|---|
| cboEvent | Combo of tblEvent | Optional; user can pick an event |
| cmdImportMyVenue | Button | MsgBox "Phase 2 — MyVenue / MSR import is Volume B" |
| cmdImportTips | Button | MsgBox "Phase 2 — Tips import is Volume B" |
| cmdImportAssignments | Button | MsgBox "Phase 2 — Assignment import is Volume B" (Copilot Volume B table; NPO EVENT ASSIGNMENT sheet) |
| txtImportStatus | Locked text | "Not in Alpha" |
| txtRecordCount | Locked text | 0 |
| txtExceptionCount | Locked text | 0 |
| sfrmImportBatch | Datasheet on tblImportBatch | Empty; shows RecordCount / ExceptionCount / Status later |
| cmdClose | Button | Close |

## 6.6 frmCategoryMap

Datasheet or continuous form on `tblCategoryMap` joined to `tblContractClass` for class name. Allow add/edit. Deactivate instead of delete.

## 6.7 frmSettings

Continuous or single form over `tblAppSetting`. Key read-only, value editable. Include RepositoryRoot.

## 6.8 Placeholder screens

Settlement Review, Communications:

Unbound form, title, one sentence (“Phase 2 — not in Alpha”), Close button. Dashboard buttons may open these so navigation can be validated.

---

# Chapter 7 — Build Sequence

Copilot v4.0 order (do not skip ahead to PDFs):

| Step | Copilot | This pass |
|---|---|---|
| 1 | Lookup Tables | Create + seed |
| 2 | Core Tables | Create + seed vendors/locations/categories; create empty assignment/import/settlement tables |
| 3 | Relationships | Relationships window + unique indexes |
| 4 | Vendor Master | `frmVendor` / list |
| 5 | Event Form | `frmEvent` / list + status button |
| 6 | Location Form | `frmLocation` + alias subform |
| 7 | Dashboard | `frmDashboard` + AutoExec. Also Category Map + Settings |
| 8 | Imports | **Stop.** Shell `frmImportCenter` only |
| 9 | Settlement Engine | **Stop.** Volume B |

Detailed Alpha order:

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
12. `frmImportCenter` shell + Settlement Review + Communications placeholders

---

# Appendix A — Phase B tables (create empty now)

Create with JSON field lists. No calc, no working import UI.

`tblImportBatch` `tblSalesImport` `tblAssignmentImport` `tblTipsImport` `tblSettlementHeader` `tblSettlementDetail` `tblSettlementAdjustment` `tblExceptionType` `tblExceptionLog` `tblDocumentRef`

`tblSettlementHeader.InvoiceNumber` unique. Also unique EventID+VendorID.

`tblSalesImport.LocationID` and `ContractClassID` FKs are **not enforced**, so unmatched import rows can be stored.

### tblAssignmentImport (Copilot Volume B, created empty in Volume A)

Staging for the NPO `EVENT ASSIGNMENT` sheet. Posted/cleaned rows live in `tblEventAssignment`.

| Field | Type | Notes |
|---|---|---|
| AssignmentImportID | AutoNumber PK | |
| BatchID | Number FK → tblImportBatch | Cascade delete with batch. ImportType = ASSIGNMENT |
| EventID | Number FK optional | Not enforced if event missing |
| RawRow | Number | Excel row |
| LocationRaw | Short Text 255 | MSR / template location string |
| LocationCodeRaw | Short Text 50 | Spaced or compact code as imported |
| LocationID | Number | Matched; **not enforced** |
| VendorShortCodeRaw | Short Text 25 | ARVC, … |
| VendorNameRaw | Short Text 255 | |
| VendorID | Number | Matched; **not enforced** |
| AllocationPct | Double default 1 | |
| PayeeSeq | Number | |
| Headcount | Number | Optional Copilot Volume B staffing count; not used in Alpha |
| AssignmentStatusRaw | Short Text 50 | |
| MatchStatus | Short Text 25 default UNMATCHED | MATCHED, UNMATCHED_LOCATION, UNMATCHED_VENDOR |
| ExceptionNote | Short Text 255 | |
| PostedYN | Yes/No default No | Volume B sets Yes after writing tblEventAssignment |
| Notes | Long Text | |

---

# Appendix B — Light VBA (Alpha only)

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

No settlement modules. Import Center buttons only `MsgBox` Phase 2.

---

# Appendix C — Seed expectations after import

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
| tblExceptionType | 9 (lookup only; log stays empty) |
| tblAssignmentImport | 0 |

ARVC SAP `1013051` BSS `5487` came from the 12/01/25 NPO PDF, not from NPO MASTER (those cells were blank).

LAG / SUG addresses and rates came from the SUB 12/01/25 workbook.

---

# Appendix D — Known traps (the reason Copilot’s Access design would have failed)

1. **PIT 101 is two locations.** Unique `LocationCode` is a defect.
2. **Mini Melts codes drifted** between NPO V4 and the 9/14/26 MyVenue list. Aliases are mandatory on day one.
3. **NPO math ≠ SUB math.** One vendor table, two later engines.
4. **$200 minimum is not in the Excel donation formula.** It is a yellow statement cell.
5. **MSR location strings must match aliases exactly.** `FB 107 - NE SPECIALTY - DAWG HOUSE` vs `NE SPECIALTY DAWG O.G.` are different strings; both need aliases.
6. **Invoice live pattern is `UNM-MMDDYY-SHORTCODE`**, not the Copilot PDF-only naming line. Store both rules.
7. **PIT 107 Laguna** has POS Profile `UNM FOOTBALL STADIUM` in MyVenue. Store as exported; Venue can still be The Pit if LocationCode starts with PIT. Seed script used POS Profile first, then code prefix. If Venue looks wrong on a SUB stand, prefer LocationCode prefix in a later data fix — do not block Alpha.
8. Ray’s last name appears as Velasquez and Valasquez on source PDFs. Settings use **Velasquez**.
9. **Compact Copilot codes (`FB106`) are not keys.** Official `LocationCode` is `FB 106`. Do not unique-index a space-stripped code.

---

# Appendix E — Acceptance checklist (print this)

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
- [ ] Import Center opens with Import MyVenue / Import Tips (Phase 2 messages OK)
- [ ] No settlement, PDF, or email code

---

# Appendix F — Volume B

Written: `EMS_Developer_Build_Binder_Volume_B.md`.

Volume A Alpha still does **not** run settlement math. The Access generator **does** create Volume B tables, `tblExceptionType` seed, and named `qry*` objects now so the schema stays frozen.

PDF, email, and Power BI remain Volume C.
