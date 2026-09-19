# Seed import order

Natural keys are used in the CSV files (`VendorShortCode`, `MyVenueCode`, `ProductCode`, `SettingKey`). Access AutoNumbers are assigned at import. Do not expect CSV ID columns for core tables.

## Order

1. `tblVendorType.csv`
2. `tblEventType.csv`
3. `tblEventStatus.csv`
4. `tblContractClass.csv`
5. `tblAppSetting.csv`
6. `tblAdjustmentType.csv`
7. `tblLocation.csv` (match `MyVenueCode`, `LocationName`, `LocationCode`, …)
8. `tblLocationAlias.csv` — after locations exist, look up `LocationID` from `MyVenueCode`
9. `tblVendor.csv` — look up `VendorTypeID` from `VendorType` name (`NPO` / `SUB`)
10. `tblVendorContract.csv` — look up `VendorID` from `VendorShortCode`
11. `tblCategoryMap.csv` — look up `ContractClassID` from `ContractClass` name (`FOOD`, `NA_BEV`, `BEER`, `LIQUOR`)

`location_alias_conflicts.csv` is documentation only. Do not import it as a table.

## Rules

- `Active` / Yes-No columns: `1` = Yes, `0` = No.
- Rates are decimals: `0.10` = 10%, `0.7` = 70%.
- Blank `MinimumDonation` on SUB contracts = Null, not zero, if Access import allows it. If the importer writes 0, that is acceptable for Alpha.
- Alias import must skip duplicates on `AliasName` (unique index).
- Official `LocationName` is also stored as an `OFFICIAL` alias. If a unique-index collision occurs, keep the alias row and ignore the duplicate.
