# EMS relationships

Create these in the Access Relationships window after all tables exist. Enforce referential integrity unless noted.

Cascade **delete** only where a child cannot exist without the parent (aliases, assignment rows, import lines, settlement lines).

| From | To | Enforce | Cascade delete |
|---|---|---|---|
| tblVendor.VendorTypeID | tblVendorType.VendorTypeID | Yes | No |
| tblVendorContract.VendorID | tblVendor.VendorID | Yes | No |
| tblLocationAlias.LocationID | tblLocation.LocationID | Yes | Yes |
| tblCategoryMap.ContractClassID | tblContractClass.ContractClassID | Yes | No |
| tblEvent.EventTypeID | tblEventType.EventTypeID | Yes | No |
| tblEvent.StatusID | tblEventStatus.StatusID | Yes | No |
| tblEventAssignment.EventID | tblEvent.EventID | Yes | Yes |
| tblEventAssignment.LocationID | tblLocation.LocationID | Yes | No |
| tblEventAssignment.VendorID | tblVendor.VendorID | Yes | No |
| tblImportBatch.EventID | tblEvent.EventID | Yes | No |
| tblSalesImport.BatchID | tblImportBatch.BatchID | Yes | Yes |
| tblSalesImport.LocationID | tblLocation.LocationID | No (unmatched imports allowed) | No |
| tblSalesImport.ContractClassID | tblContractClass.ContractClassID | No | No |
| tblTipsImport.BatchID | tblImportBatch.BatchID | Yes | Yes |
| tblTipsImport.VendorID | tblVendor.VendorID | No | No |
| tblTipsImport.LocationID | tblLocation.LocationID | No | No |
| tblSettlementHeader.EventID | tblEvent.EventID | Yes | No |
| tblSettlementHeader.VendorID | tblVendor.VendorID | Yes | No |
| tblSettlementDetail.SettlementID | tblSettlementHeader.SettlementID | Yes | Yes |
| tblSettlementDetail.LocationID | tblLocation.LocationID | Yes | No |
| tblSettlementAdjustment.SettlementID | tblSettlementHeader.SettlementID | Yes | Yes |
| tblSettlementAdjustment.AdjustmentTypeID | tblAdjustmentType.AdjustmentTypeID | Yes | No |
| tblDocumentRef.VendorID | tblVendor.VendorID | No | No |
| tblDocumentRef.EventID | tblEvent.EventID | No | No |
| tblDocumentRef.SettlementID | tblSettlementHeader.SettlementID | No | No |

## Extra unique indexes

- `tblEventAssignment (EventID, LocationID, VendorID)`
- `tblSettlementHeader (EventID, VendorID)`
- `tblLocation.LocationCode` is indexed, **not unique**
