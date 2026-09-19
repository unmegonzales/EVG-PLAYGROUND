# EMS Developer Build Binder v5.0
## Volume B — Settlement Engine Technical Specifications

**Product:** Event Management System (EMS)  
**Owner:** UNM Athletics Hospitality / Levy  
**Binder date:** 2026-09-19  
**Depends on:** Volume A (frozen)  
**Canonical schema:** `schema/ems_access_schema.json`

Volume A defines **what exists**.  
Volume B defines **how the money moves**.

This volume freezes the construction baseline for imports, matching, NPO/SUB math, exceptions, queries, and finance-review gates. PDF, email, and Power BI stay in Volume C.

If this binder and the JSON disagree on a field name or size, **JSON wins**. If this binder and Copilot Volume B disagree on math, **live UNM files win** (called out in Chapter 0).

---

## 0. Freeze status

| Area | Status | Notes |
|---|---|---|
| Volume A tables / forms | **Frozen** | Do not redesign |
| Volume B tables listed here | **Frozen (~80%)** | Create in `EMS_BE.accdb` now, even if Alpha UI does not use them |
| NPO/SUB calculation rules | **Frozen** | Use live-file math, not Copilot’s one-rate gross example |
| Exception types | **Frozen** | Add types later via seed, not by inventing tables |
| Query names | **Frozen** | SQL bodies may be refined without renaming |
| $200 NPO minimum | **Open — Finance** | Live Excel is a manual yellow line. Store `MinimumDonation`. Do not code auto-min until Finance confirms |
| PDF / email / Power BI | **Not frozen** | Volume C |

Construction rule: future changes are controlled revisions, not weekly schema rewrites.

---

## 0.1 Copilot Volume B vs live files (do not “simplify” back)

Copilot’s Volume B is the right **shape**. These rules from the live packets override Copilot’s examples:

| Copilot Volume B | Frozen EMS rule |
|---|---|
| NPO = Gross sales × one contract % | NPO donation uses **net** sales, split Food/Non-Alc vs Alcohol, then vendor rates |
| Beer $20,000 × 10% = $2,000 | Alcohol bucket uses **8%** on NPO defaults; food/non-alc uses **10%**. SUB uses four vendor rates |
| Assignment = vendor + location only | Assignment also has **AllocationPct**. Split stands must sum to 1.00 |
| Location match on code (`FB120`) | Match **alias / full MyVenue name**. `PIT 101` is two locations |
| Tips = TipAmount + EmployeeCount | Keep gross vs allocated tips. EmployeeCount is optional |
| Settlement detail class FOOD / NONALC / ALCOHOL | Store **FOOD, NA_BEV, BEER, LIQUOR**. Roll up to NPO classes in queries |
| Import sales never edited | Keep. Matching writes `LocationID` / `ContractClassID` / `MatchStatus` only |

---

## 1. Settlement architecture

### Inputs

| Input | Source | Staging table | Posted / used as |
|---|---|---|---|
| Sales | MyVenue MSR category export | `tblSalesImport` | Mapped net by location + class |
| Assignments | Event assignment sheet / UI | `tblAssignmentImport` | `tblEventAssignment` |
| Tips | Tips sheet | `tblTipsImport` | Header + detail gratuities |
| Contract | Vendor master | `tblVendorContract` | Rates, min, expenses flag |
| Category map | Product codes | `tblCategoryMap` | FOOD / NA_BEV / BEER / LIQUOR |
| Locations | MyVenue list + aliases | `tblLocation` / `tblLocationAlias` | LocationID |

### Outputs

| Output | Grain | Table |
|---|---|---|
| Settlement summary | One per vendor per event | `tblSettlementHeader` |
| Settlement details | Per location (and class amounts on that row) | `tblSettlementDetail` |
| NPO donation | Header `CommissionAmount` for NPO | calculated |
| SUB payment | Header `CommissionAmount` for SUB | calculated |
| Adjustments | Tips already on detail; cook fee, min, card fee, ice | `tblSettlementAdjustment` |
| Finance review | Event-level package | `qryFinanceReview` |
| Audit | Every file drop + every exception | `tblImportBatch` / `tblExceptionLog` |

Raw import rows are **never typed over**. Corrections happen by: alias, category map, assignment, re-import, or exception resolution.

---

## 2. Pipeline (heart of EMS)

```
OPEN event
  → Import Sales        → tblSalesImport
  → Map categories      → tblCategoryMap
  → Resolve locations   → tblLocationAlias
  → Import / post assignments → tblAssignmentImport → tblEventAssignment
  → Import tips         → tblTipsImport
  → Generate exceptions
  → Resolve exceptions
  → Generate settlements
  → Finance Review
  → Approve
  → CLOSED
```

CLOSED is blocked until Chapter 13 gates pass.

### Step 1 — Import sales

Parse the nested MyVenue CSV (`Location:` then `product Total:` rows). One `tblImportBatch` (`ImportType = SALES`). Product lines only; skip location-total and department-total rows.

`LocationRaw` is Copilot’s `LocationName`. Never edit it.

### Step 2 — Map categories

`ProductCode` → `tblCategoryMap` → `ContractClassID`.  
Unmapped code → exception `MISSING_CATEGORY`. Unmapped but `Active = No` → `IGNORE` (no money).

### Step 3 — Match locations

Trim `LocationRaw`, case-insensitive exact match to `tblLocationAlias.AliasName` → `LocationID`.  
Zero hits → `MISSING_LOCATION`. Do not match on `LocationCode` alone.

### Step 4 — Assign vendor

Join resolved sales location to **posted** `tblEventAssignment` for that `EventID`.  
Apply `AllocationPct`.  
No assignment → `MISSING_VENDOR` (location has sales, nobody owns it).  
Two vendors on one location is legal if allocations sum to 1.00; otherwise `ALLOCATION_NOT_100`.  
Duplicate exact Event+Location+Vendor on import → `DUPLICATE_ASSIGNMENT`.

### Step 5 — Apply contract rates

Active contract where `EffectiveDate <= EventDate` and (`ExpirationDate` is null or `>= EventDate`).  
None → `MISSING_CONTRACT`.

Then run the NPO or SUB engine (Chapters 9–10). Write header, details, adjustments. Do not write if blocking exceptions remain.

---

## 3. tblImportBatch (audit)

Already in Volume A schema. Frozen values:

| Field | Volume B name | Allowed / notes |
|---|---|---|
| BatchID | ImportBatchID | PK |
| EventID | | Required for settlement imports |
| ImportType | | `SALES`, `ASSIGNMENTS`, `TIPS` |
| SourceFileName | FileName | Original file name |
| SourcePath | | Repository path, not the blob |
| ImportedBy | | Short Text 100 |
| ImportedAt | ImportDate | Default Now() |
| RecordCount | | Rows read |
| SuccessCount | | Rows matched |
| ExceptionCount | | Rows or issues logged |
| Status | ImportStatus | `Completed`, `Partial`, `Failed` |
| Notes | | |

`Completed` = no exceptions. `Partial` = some matched, exceptions remain. `Failed` = parser/file failure, do not generate settlements.

---

## 4. tblSalesImport

Raw MyVenue lines. Matching fields may be filled by engine; dollar fields stay as imported.

| Field | Type | Notes |
|---|---|---|
| SalesImportID | AutoNumber PK | |
| EventID | Number FK | |
| BatchID | Number FK | Copilot ImportBatchID |
| LocationRaw | Short Text 255 | Copilot LocationName. Immutable |
| LocationID | Number FK nullable | Filled by alias match |
| ProductCode | Short Text 25 | e.g. 313082, FF-312114 |
| ProductName | Short Text 255 | Copilot ProductDescription |
| ContractClassID | Number FK nullable | Filled by category map |
| GrossAmt | Currency | Copilot GrossSales |
| NetAmt | Currency | **Settlement base for NPO** |
| Quantity | Double | |
| SalesDate | Date/Time | Optional; event date is authoritative |
| ImportTimestamp | Date/Time | Default Now() |
| MatchStatus | Short Text 25 | UNMATCHED / MATCHED / UNMATCHED_LOCATION / UNMATCHED_PRODUCT / IGNORE |
| ExceptionNote | Short Text 255 | |
| RawRow | Number | Source row index |

---

## 5. tblAssignmentImport (staging) vs tblEventAssignment (posted)

Copilot put assignments in one table. EMS keeps two so a bad import cannot smash posted ownership.

**tblAssignmentImport** (new, staging, never the calc source)

| Field | Type | Notes |
|---|---|---|
| AssignmentImportID | AutoNumber PK | |
| BatchID | Number FK | |
| EventID | Number FK | |
| VendorShortCodeRaw | Short Text 25 | |
| VendorID | Number FK nullable | |
| LocationRaw | Short Text 255 | |
| LocationID | Number FK nullable | |
| AllocationPct | Double default 1 | 0–1 |
| Headcount | Number | Optional |
| PayeeSeq | Number | |
| Notes | Long Text | |
| MatchStatus | Short Text 25 | |

Posting copies matched rows into `tblEventAssignment` (Volume A). Calc always reads **posted** assignments.

Add optional `Headcount` and `SourceBatchID` on `tblEventAssignment`.

---

## 6. tblTipsImport

| Field | Type | Notes |
|---|---|---|
| TipsImportID | AutoNumber PK | Copilot TipImportID |
| EventID | Number FK | |
| BatchID | Number FK | |
| VendorShortCodeRaw | Short Text 25 | |
| VendorID | Number FK nullable | |
| LocationRaw | Short Text 255 | |
| LocationID | Number FK nullable | |
| GrossTips | Currency | |
| AllocationPct | Double default 1 | |
| AllocatedTips | Currency | Copilot TipAmount. This is what pays |
| EmployeeCount | Number | Optional |
| MatchStatus | Short Text 25 | |
| Notes | Short Text 255 | |

If location match fails, try vendor+location description (same rule as NPO V4). Else `UNMATCHED_TIPS`.

---

## 7. tblExceptionLog (critical)

Finance will hate EMS without this.

**tblExceptionType** (seeded lookup)

| Code | Meaning |
|---|---|
| MISSING_LOCATION | Sales/assignment/tips location string not in aliases |
| MISSING_VENDOR | Sales at a location with no posted assignment |
| MISSING_CATEGORY | ProductCode not in category map |
| DUPLICATE_ASSIGNMENT | Same event+location+vendor twice |
| MISSING_CONTRACT | No active contract for vendor/event date |
| ALLOCATION_NOT_100 | Posted allocations for event+location not within 0.0001 of 1.00 |
| NO_MSR_SALES | Assignment exists, mapped net = 0 |
| UNMATCHED_TIPS | Tips row could not match vendor/location |
| MISSING_ALLOCATION | Assignment row has blank allocation |

`NO_MSR_SALES` is **non-blocking** ( Copilot Excel status OK-equivalent warning). All others except IGNORE are **blocking** until `Resolved = Yes`.

**tblExceptionLog**

| Field | Type | Notes |
|---|---|---|
| ExceptionID | AutoNumber PK | |
| EventID | Number FK | |
| BatchID | Number FK nullable | |
| ExceptionTypeID | Number FK | |
| SourceTable | Short Text 50 | tblSalesImport, etc. |
| SourcePK | Number | |
| VendorID | Number nullable | |
| LocationID | Number nullable | |
| ProductCode | Short Text 25 | |
| Description | Long Text | Human readable |
| Resolved | Yes/No default No | |
| ResolvedBy | Short Text 50 | |
| ResolvedDate | Date/Time | |
| CreatedDate | Date/Time default Now() | |

Do not delete exceptions. Resolve them.

---

## 8. tblSettlementHeader

One row per vendor per event. Unique `(EventID, VendorID)`.

Copilot names mapped onto the richer Volume A header:

| Copilot field | EMS field |
|---|---|
| TotalGrossSales | `TotalGrossSales` (added) |
| TotalTips | `TipsAmount` |
| TotalSettlement | `AmountDue` |
| SettlementStatus | `Status` |
| GeneratedDate | `CreatedDate` |

**Frozen Status values:** `Draft` → `Reviewed` → `Approved` → `Paid`

Keep Volume A money fields: FoodNet, NonAlcNet, BeerNet, LiquorNet, GroupNet, CommissionAmount, TipsAmount, AdjustmentAmount, AmountDue, InvoiceNumber, PreparedBy / ReviewedBy / ApprovedBy.

Invoice number:

```
UNM- & Format([EventDate],"mmddyy") & "-" & [VendorShortCode]
```

---

## 9. tblSettlementDetail

One row per settlement + location (assignment line). Class dollars live **on the row**, not as separate rows per FOOD/ALCOHOL (Copilot’s ContractClass column is replaced by four net + four commission columns already on the table).

| Field | Role |
|---|---|
| LocationID | Assigned stand |
| AllocationPct | Share of that location |
| FoodNet, NonAlcNet, BeerNet, LiquorNet | Allocated nets |
| LocationNet | Sum of four nets |
| FoodCommission … LiquorCommission | Rate applied |
| TotalCommission | NPO donation or SUB commission for the stand |
| Gratuities | Allocated tips |
| RateFood / RateNonAlc / RateBeer / RateLiquor | Snapshot of rates used (added so audit does not drift) |

NPO rollup for display:

- FOOD_NONALC net = FoodNet + NonAlcNet  
- ALCOHOL net = BeerNet + LiquorNet

---

## 10. NPO calculation engine (frozen)

Per posted assignment row:

```
Matched sales at LocationID
  FoodNet     = Sum(NetAmt) where class = FOOD
  NonAlcNet   = Sum(NetAmt) where class = NA_BEV
  BeerNet     = Sum(NetAmt) where class = BEER
  LiquorNet   = Sum(NetAmt) where class = LIQUOR

Allocated* = classNet * AllocationPct

FoodNonAlcNet = AllocatedFood + AllocatedNonAlc
AlcoholNet    = AllocatedBeer + AllocatedLiquor

Donation = FoodNonAlcNet * FoodRate + AlcoholNet * AlcoholRate
         + AllocatedBeer * BeerRate + AllocatedLiquor * LiquorRate
```

For standard NPO contracts FoodRate = NonAlcoholRate = 0.10 and BeerRate = LiquorRate = 0.08, so:

```
Donation = FoodNonAlcNet * 0.10 + AlcoholNet * 0.08
```

That is the 9/5/26 workbook formula (`CONTRACT CALC!K`).

Tips: `AllocatedTips` for same Event+Vendor+Location.

**Minimum donation (not coded until Finance confirms):**

Live Excel does **not** put `$200` in the donation formula. It is a yellow statement cell (`MIN_DONATION` adjustment). Copilot Volume B proposed header-level `Max(calc, min)`. That is **not** frozen.

Volume B generate-settlement must:

```
Donation = Sum(detail Food/Non-Alc and Alcohol commissions using live rates)
AmountDue = Donation + Tips + manual adjustments (cook fee, min donation, bonus, shortages)
```

If Finance later approves auto-min, add `MIN_DONATION = MinimumDonation - CalcDonation` only when CalcDonation < MinimumDonation, **header level**, never per location.

Cook fees, bonus, shortages stay **manual adjustments** (yellow cells today).

9/5/26 proof (do not seed): assignment net $54,718.50, donation $5,129.94, tips $3,421.74. ARVC also had $25 cook fee.

---

## 11. SUB calculation engine (frozen)

Different from NPO. No minimum donation. Expenses allowed.

Per vendor/event (12/01/25 workbook is one stand per vendor; still write one detail row with LocationID when known):

```
Net = Gross / (1 + Event.TaxRate)     ' 0.07625 in current packets
Commission = FoodNet * FoodRate
           + NonAlcNet * NonAlcoholRate
           + BeerNet * BeerRate
           + LiquorNet * LiquorRate

AmountDue = Commission
          - expenses (card fee 3% max, ice $3/bag, COS, shortage)
          + gratuities
```

Proof: LAG `UNM-120125-LAG` $1,639.33 (food 70%, N/A 5%). SUG `UNM-120125-SUG` $1,293.64 (food 80%, N/A 5%).

GL split is in `tblAdjustmentType` / `tblAppSetting`. Do not invent new GLs.

---

## 12. Query architecture (frozen names)

Create these as Access queries in the FE (or BE if the generator prefers; FE is enough). They **are** the engine’s readable layer. VBA may call them; do not replace them with undocumented query names.

### qrySalesMapped

SalesImport joined to category map. Resolves ProductCode → ContractClass.

```sql
SELECT
  s.SalesImportID, s.EventID, s.BatchID,
  s.LocationRaw, s.LocationID,
  s.ProductCode, s.ProductName,
  s.GrossAmt, s.NetAmt, s.Quantity,
  c.ContractClassName, c.NPOClass,
  s.MatchStatus
FROM tblSalesImport AS s
LEFT JOIN tblContractClass AS c
  ON s.ContractClassID = c.ContractClassID;
```

### qryLocationResolved

Alias match helper (engine also does this in VBA on import). Documents the join:

```sql
SELECT
  s.SalesImportID, s.EventID, s.LocationRaw,
  a.AliasName, a.LocationID, loc.LocationName, loc.LocationCode
FROM (tblSalesImport AS s
LEFT JOIN tblLocationAlias AS a
  ON StrComp(Trim(s.LocationRaw), Trim(a.AliasName), 1) = 0)
LEFT JOIN tblLocation AS loc
  ON a.LocationID = loc.LocationID;
```

Access `StrComp` with `1` = text (case-insensitive). If the generator cannot build that join, keep the query as LocationRaw = AliasName and document the limitation.

### qryVendorAssigned

Posted assignments:

```sql
SELECT
  ea.EventID, ea.LocationID, ea.VendorID, ea.AllocationPct,
  ea.PayeeSeq, ea.Headcount,
  v.VendorShortCode, v.VendorName, vt.VendorTypeName,
  loc.LocationName
FROM ((tblEventAssignment AS ea
INNER JOIN tblVendor AS v ON ea.VendorID = v.VendorID)
INNER JOIN tblVendorType AS vt ON v.VendorTypeID = vt.VendorTypeID)
INNER JOIN tblLocation AS loc ON ea.LocationID = loc.LocationID;
```

### qrySettlementCalculation

Allocated nets by event, vendor, location, class (feed the generate routine):

```sql
SELECT
  ea.EventID,
  ea.VendorID,
  ea.LocationID,
  ea.AllocationPct,
  cc.ContractClassName,
  Sum(s.NetAmt * ea.AllocationPct) AS AllocatedNet,
  Sum(s.GrossAmt * ea.AllocationPct) AS AllocatedGross
FROM (tblEventAssignment AS ea
INNER JOIN tblSalesImport AS s
  ON ea.EventID = s.EventID AND ea.LocationID = s.LocationID)
INNER JOIN tblContractClass AS cc
  ON s.ContractClassID = cc.ContractClassID
WHERE s.MatchStatus = 'MATCHED'
GROUP BY ea.EventID, ea.VendorID, ea.LocationID, ea.AllocationPct, cc.ContractClassName;
```

### qrySettlementSummary

```sql
SELECT
  h.SettlementID, h.EventID, h.VendorID, h.InvoiceNumber,
  h.SettlementType, h.Status,
  h.GroupNet, h.CommissionAmount, h.TipsAmount,
  h.AdjustmentAmount, h.AmountDue,
  v.VendorShortCode, v.VendorName
FROM tblSettlementHeader AS h
INNER JOIN tblVendor AS v ON h.VendorID = v.VendorID;
```

### qryFinanceReview

Event package: imports, exception counts, settlement totals, unpaid blocking exceptions.

```sql
SELECT
  e.EventID, e.EventDate, e.EventName, st.StatusName,
  Count of batches, sum RecordCount,
  Count of unresolved blocking exceptions,
  Count of settlements, Sum(AmountDue)
FROM tblEvent e ...
```

Exact SQL may use subqueries; keep the name and the columns Finance needs: event, status, import completeness, open exceptions, settlement count, amount due.

### qryExceptionOpen

```sql
SELECT x.*, t.ExceptionCode
FROM tblExceptionLog AS x
INNER JOIN tblExceptionType AS t ON x.ExceptionTypeID = t.ExceptionTypeID
WHERE x.Resolved = False;
```

---

## 13. Finance review workflow

```
OPEN
 → Import Data
 → Generate Settlement
 → Resolve Exceptions
 → FINANCE REVIEW
 → Approve
 → CLOSED
```

**No event moves to CLOSED unless all of these are true:**

1. At least one `SALES` batch Status `Completed` or `Partial` with `SuccessCount > 0`
2. Zero unresolved **blocking** exceptions for the EventID
3. Every posted assignment vendor has a `tblSettlementHeader` row
4. Every settlement Status is `Reviewed` or `Approved` or `Paid` (not `Draft`)
5. Event Status is `FINANCE REVIEW` before the Closed click

`cmdAdvanceStatus` on `frmEvent` must enforce this once Volume B code is wired. Until then, Volume A may still advance status (Alpha). Volume B implementation replaces that with the gates.

Settlement Review form (`frmSettlementReview`) in Volume B implementation:

- Event combo
- Exception list (unresolved first)
- Generate Settlements button
- Vendor settlement list → open statement preview (layout later; data now)
- Mark Reviewed / Approved

Import Center (`frmImportCenter`) in Volume B implementation:

- Import MyVenue
- Import Assignments
- Import Tips
- Show last batch: Status, RecordCount, SuccessCount, ExceptionCount

---

## 14. Forms added or upgraded in Volume B (not Alpha)

Alpha may keep placeholders. Volume B wiring:

| Form | Purpose |
|---|---|
| frmImportCenter | Three import buttons + batch stats + exception peek |
| frmSettlementReview | Generate, review, approve |
| frmExceptionLog | Filter Event, Resolved, Type |
| sfrmEventAssignment | Already specified in Volume A; used as posted assignment UI |

Still **do not** build PDF, Outlook draft, or Power BI in this volume.

---

## 15. Volume C candidates (not this build)

- Automated email generation
- Vendor settlement PDF packages (NPO ARVC layout + SUB Sugar Shivers layout)
- Approval routing beyond on-form Reviewed/Approved
- Employee tip distribution engine
- Power BI integration
- Microsoft Copilot integration
- Electronic document retention rules

---

## 16. Access generator instructions for Volume B objects

When generating the ACCDB (same pass as Volume A or immediately after):

1. Create all Volume B tables from JSON (`tblAssignmentImport`, `tblExceptionType`, `tblExceptionLog`, plus extra fields on existing B tables)
2. Seed `tblExceptionType`
3. Create the six `qry*` objects (plus `qryExceptionOpen`)
4. Do **not** auto-run settlement math on Alpha
5. Placeholder Import/Settlement forms may stay until Volume A Alpha is accepted, then replace with Chapter 14

---

## 17. Acceptance (Volume B schema freeze)

- [ ] `tblAssignmentImport` exists and is not the calc source
- [ ] `tblExceptionLog` + `tblExceptionType` seeded
- [ ] Sales import has immutable `LocationRaw` + `NetAmt`
- [ ] Settlement Status allows Draft / Reviewed / Approved / Paid
- [ ] Named queries exist
- [ ] CLOSED gates documented on frmEvent (code may wait until after Alpha UI)
- [ ] NPO formula uses net × 10/8 with allocation
- [ ] SUB formula uses four rates, tax strip, expenses
- [ ] Header-level NPO minimum documented as EMS rule
