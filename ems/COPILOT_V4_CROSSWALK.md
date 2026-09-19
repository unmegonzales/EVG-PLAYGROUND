# Copilot Volume A v4.0 → this package (v6.0)

The user pasted Copilot’s **EMS Developer Build Binder v4.0 Volume A** and asked to start Volume A properly. Copilot’s paste is a chapter outline. This package keeps that chapter map and fills it with live UNM files.

Copilot source: chat paste dated 2026-09-19, titled *Foundation Architecture & User Interface*.  
Canonical build file: `EMS_Developer_Build_Binder_Volume_A.md`.

## Chapter map

| Copilot v4.0 | This binder | Action |
|---|---|---|
| Ch 1 System Architecture (FE/BE/Repository) | Chapter 1 | Adopted. Added `Vendors/` folder, FE-only `tblLocalLink`, AutoExec, Reports empty in Alpha |
| Ch 2 Lookup Tables | Chapter 2 | Adopted. Added Baseball event type, `EventTypeShort`, `StatusSequence`, plus Copilot-omitted lookups `tblContractClass` `tblAppSetting` `tblAdjustmentType` |
| Ch 3 Core tables (`tblEvent` `tblVendor` `tblLocation` `tblLocationAlias`) | Chapter 3 | Adopted and expanded from live files |
| Ch 4 Category Mapping Engine | Chapter 4 | Adopted. `ContractClass` is an FK, not free text |
| Ch 5 Contract Table | Chapter 5 | Adopted. `$200` is stored, **not** auto-applied |
| Ch 6 Form Architecture | Chapter 6 | Adopted. `frmVendorMaster` = object `frmVendor`. Import Center is an Alpha **shell** |
| Ch 7 Build Sequence (1–9) | Chapter 7 | Adopted. Alpha stops at step 7 + Category/Settings. Steps 8–9 are Volume B |
| “Tomorrow Volume B” list | Appendix F | Adopted. Added `tblAssignmentImport` now (empty) so Volume B does not invent a table |

## Field-level: keep Copilot vs correct from live files

| Copilot v4.0 said | Live files / this package |
|---|---|
| `LocationCode` indexed examples `FB106` `PIT104` `FB151` | Official codes are **spaced**: `FB 106`, `PIT 104`. Compact `FB106` is **not** seeded as a unique alias — `PIT101` would collide (`PIT 101` is two stands) |
| `LocationCode` as the location key | `LocationName` + `MyVenueCode` unique. `LocationCode` indexed, **duplicates allowed** |
| Location master = Code + Description + Venue + Department | Also `LocationName`, `Menu`, `POSProfile`, `Family`, `PriceLevel`, `IsWarehouse` from MyVenue 9/14/26 |
| Alias example: `FB 120 - MBP N. SCOREBOARD` vs `…WEST NO.1` | Seeded. Official name is `FB 120 - MBP N. SCOREBOARD WEST NO.1`; NPO template alias kept |
| Event types: Football, MBB, WBB, Concert, Rental, Special Event | Added **Baseball** (`BB`) because MyVenue has `BB 101` |
| `tblEvent` fields: date, name, type, status, notes, created | Also `InternalEventName`, `TaxRate` (0.07625), `Modified*`, `ClosedDate`. Examples: `Football`, `NMAA BBALL 2026`, `MBB - NM HIGHLANDS` |
| Vendor fields: name, short code, type, SAP, BSS, contact, email, CC, phone, active, notes | Also `CheckPayableTo`, `Address1` `City` `State` `PostalCode` (required on SUB statements), W9/COI/Contract **paths** |
| `tblCategoryMap.ContractClass` Short Text `FOOD_NONALC` / `ALCOHOL` | `ContractClassID` → `tblContractClass` with `FOOD` `NA_BEV` `BEER` `LIQUOR` (NPO still rolls to FOOD_NONALC / ALCOHOL) |
| Category examples only “FOOD SALES TAXABLE / LIQUOR SALES TAXABLE” | Eight locked product codes from the 9/5/26 MSR export |
| `MinimumDonation` NPO 200 / SUB NULL | Stored on the contract. **Do not auto-apply.** Current Excel donation formula does not use it; it is a yellow statement line (`tblAdjustmentType` `MIN_DONATION`). Copilot Volume B’s `Max(calc, min)` is an open Finance decision, not a freeze |
| Contract: four rates + min + expenses + dates | Also `CardFeeMaxRate` 0.03, `Active`, `Notes`. LAG 0.70/0.05, SUG 0.80/0.05 |
| FE contains Reports | True as a class of object. **Alpha builds zero reports** |
| FE contains Queries | Alpha may create list queries (`qryVendorActive`, `qryEventList`, …). No settlement queries |
| Build step 8 Imports, step 9 Settlement Engine | In Copilot’s Volume A sequence, then Copilot deferred them to Volume B. This package: create empty import/settlement **tables** now; do not code engines |
| Volume B `tblAssignmentImport` | Created empty in this pass. Posted rows land in `tblEventAssignment` (master, Phase A) |
| Invoice mentioned only via later PDF name | Production invoice number is `UNM-MMDDYY-SHORTCODE` |

## Intentionally not taken from Copilot

- Unique `LocationCode`
- Auto-applied $200 NPO minimum (Excel does not; wait for Finance)
- Single-file `EMS_v1_0.accdb`
- Implementing Import MyVenue / Import Tips in Alpha
- Implementing settlement math, PDF, or email in Alpha
- Treating compact codes (`FB106`) as keys

## Volume B v4.0 paste (2026-09-19)

Copilot’s Volume B chapter map is adopted in `EMS_Developer_Build_Binder_Volume_B.md`. Live-file math overrides Copilot’s simplified examples.

| Copilot Volume B | This package |
|---|---|
| NPO = Gross × one % | Net × 10% food/non-alc + 8% alcohol, × AllocationPct |
| Assignment = vendor + location | Staging `tblAssignmentImport` + posted `tblEventAssignment` with AllocationPct |
| Location match on code | Alias / full MyVenue name |
| Detail ContractClass FOOD/NONALC/ALCOHOL | Four buckets on the detail row; NPO rolls up in queries |
| tblExceptionLog | Adopted, plus `tblExceptionType` seed |
| Query names qrySalesMapped … qryFinanceReview | Frozen names; SQL in Volume B Ch 12 |
| $200 min overrides calc | **Not frozen.** Live Excel is a manual yellow line. Store the field; do not code auto-min until Finance confirms |
| CLOSED gates | Documented; Alpha may still advance status until engine is wired |
| PDF / email / Power BI | Volume C |

