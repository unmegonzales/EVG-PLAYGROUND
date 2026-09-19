-- EMS Access ACE/Jet DDL
-- Preferred path: Table Designer + Relationships window using ems_access_schema.json.
-- SQL is a fallback. If CREATE TABLE fails, create the table visually with the same fields.
-- Number Field Size = Long Integer unless type is Double.
-- Yes/No stored as 0 / -1.

CREATE TABLE tblVendorType (
    [VendorTypeID] COUNTER,
    [VendorTypeName] TEXT(50) NOT NULL,
    [VendorTypeDescription] TEXT(255),
    CONSTRAINT pk_tblVendorType PRIMARY KEY ([VendorTypeID])
);

CREATE UNIQUE INDEX uk_tblVendorType_VendorTypeName ON tblVendorType ([VendorTypeName]);

CREATE TABLE tblEventType (
    [EventTypeID] COUNTER,
    [EventTypeName] TEXT(50) NOT NULL,
    [EventTypeShort] TEXT(10) NOT NULL,
    CONSTRAINT pk_tblEventType PRIMARY KEY ([EventTypeID])
);

CREATE UNIQUE INDEX uk_tblEventType_EventTypeName ON tblEventType ([EventTypeName]);
CREATE UNIQUE INDEX uk_tblEventType_EventTypeShort ON tblEventType ([EventTypeShort]);

CREATE TABLE tblEventStatus (
    [StatusID] COUNTER,
    [StatusName] TEXT(50) NOT NULL,
    [StatusSequence] LONG NOT NULL,
    [IsClosed] YESNO DEFAULT 0,
    CONSTRAINT pk_tblEventStatus PRIMARY KEY ([StatusID])
);

CREATE UNIQUE INDEX uk_tblEventStatus_StatusName ON tblEventStatus ([StatusName]);

CREATE TABLE tblContractClass (
    [ContractClassID] COUNTER,
    [ContractClassName] TEXT(20) NOT NULL,
    [NPOClass] TEXT(20) NOT NULL,
    [DefaultNPORate] DOUBLE NOT NULL DEFAULT 0,
    CONSTRAINT pk_tblContractClass PRIMARY KEY ([ContractClassID])
);

CREATE UNIQUE INDEX uk_tblContractClass_ContractClassName ON tblContractClass ([ContractClassName]);

CREATE TABLE tblAppSetting (
    [SettingID] COUNTER,
    [SettingKey] TEXT(50) NOT NULL,
    [SettingValue] TEXT(255),
    [ValueType] TEXT(20) NOT NULL DEFAULT 'TEXT',
    [Notes] TEXT(255),
    CONSTRAINT pk_tblAppSetting PRIMARY KEY ([SettingID])
);

CREATE UNIQUE INDEX uk_tblAppSetting_SettingKey ON tblAppSetting ([SettingKey]);

CREATE TABLE tblAdjustmentType (
    [AdjustmentTypeID] COUNTER,
    [AdjustmentCode] TEXT(30) NOT NULL,
    [AdjustmentName] TEXT(100) NOT NULL,
    [AppliesTo] TEXT(10) NOT NULL,
    [DefaultIsDeduction] YESNO DEFAULT 0,
    [DefaultGLCode] TEXT(20),
    [SortOrder] LONG DEFAULT 0,
    [Active] YESNO DEFAULT -1,
    CONSTRAINT pk_tblAdjustmentType PRIMARY KEY ([AdjustmentTypeID])
);

CREATE UNIQUE INDEX uk_tblAdjustmentType_AdjustmentCode ON tblAdjustmentType ([AdjustmentCode]);

CREATE TABLE tblVendor (
    [VendorID] COUNTER,
    [VendorName] TEXT(255) NOT NULL,
    [VendorShortCode] TEXT(25) NOT NULL,
    [VendorTypeID] LONG NOT NULL,
    [SAPID] TEXT(50),
    [BSSID] TEXT(50),
    [CheckPayableTo] TEXT(255),
    [PrimaryContact] TEXT(255),
    [Phone] TEXT(50),
    [EmailAddress] TEXT(255),
    [CCEmailAddress] TEXT(255),
    [Address1] TEXT(255),
    [City] TEXT(100),
    [State] TEXT(2),
    [PostalCode] TEXT(10),
    [Active] YESNO NOT NULL DEFAULT -1,
    [W9Path] TEXT(255),
    [COIPath] TEXT(255),
    [ContractPath] TEXT(255),
    [Notes] MEMO,
    [CreatedDate] DATETIME DEFAULT Now(),
    [CreatedBy] TEXT(50),
    [ModifiedDate] DATETIME,
    [ModifiedBy] TEXT(50),
    CONSTRAINT pk_tblVendor PRIMARY KEY ([VendorID])
);

CREATE INDEX ix_tblVendor_VendorName ON tblVendor ([VendorName]);
CREATE UNIQUE INDEX uk_tblVendor_VendorShortCode ON tblVendor ([VendorShortCode]);

CREATE TABLE tblVendorContract (
    [ContractID] COUNTER,
    [VendorID] LONG NOT NULL,
    [FoodRate] DOUBLE NOT NULL DEFAULT 0,
    [NonAlcoholRate] DOUBLE NOT NULL DEFAULT 0,
    [BeerRate] DOUBLE NOT NULL DEFAULT 0,
    [LiquorRate] DOUBLE NOT NULL DEFAULT 0,
    [MinimumDonation] CURRENCY,
    [AllowExpenses] YESNO DEFAULT 0,
    [CardFeeMaxRate] DOUBLE DEFAULT 0,
    [EffectiveDate] DATETIME DEFAULT Date(),
    [ExpirationDate] DATETIME,
    [Active] YESNO DEFAULT -1,
    [Notes] MEMO,
    CONSTRAINT pk_tblVendorContract PRIMARY KEY ([ContractID])
);


CREATE TABLE tblLocation (
    [LocationID] COUNTER,
    [MyVenueCode] LONG NOT NULL,
    [LocationName] TEXT(255) NOT NULL,
    [LocationCode] TEXT(50) NOT NULL,
    [LocationDescription] TEXT(255),
    [Venue] TEXT(100),
    [Department] TEXT(100),
    [Menu] TEXT(255),
    [POSProfile] TEXT(100),
    [Family] TEXT(255),
    [PriceLevel] TEXT(50),
    [IsWarehouse] YESNO DEFAULT 0,
    [Active] YESNO DEFAULT -1,
    [Notes] MEMO,
    CONSTRAINT pk_tblLocation PRIMARY KEY ([LocationID])
);

CREATE UNIQUE INDEX uk_tblLocation_MyVenueCode ON tblLocation ([MyVenueCode]);
CREATE UNIQUE INDEX uk_tblLocation_LocationName ON tblLocation ([LocationName]);
CREATE INDEX ix_tblLocation_LocationCode ON tblLocation ([LocationCode]);
CREATE INDEX ix_tblLocation_Venue ON tblLocation ([Venue]);

CREATE TABLE tblLocationAlias (
    [AliasID] COUNTER,
    [LocationID] LONG NOT NULL,
    [AliasName] TEXT(255) NOT NULL,
    [AliasType] TEXT(25),
    [Notes] TEXT(255),
    CONSTRAINT pk_tblLocationAlias PRIMARY KEY ([AliasID])
);

CREATE UNIQUE INDEX uk_tblLocationAlias_AliasName ON tblLocationAlias ([AliasName]);

CREATE TABLE tblCategoryMap (
    [CategoryMapID] COUNTER,
    [ProductCode] TEXT(25) NOT NULL,
    [ProductDescription] TEXT(255) NOT NULL,
    [ContractClassID] LONG NOT NULL,
    [DefaultRate] DOUBLE NOT NULL,
    [Active] YESNO DEFAULT -1,
    [Notes] TEXT(255),
    CONSTRAINT pk_tblCategoryMap PRIMARY KEY ([CategoryMapID])
);

CREATE UNIQUE INDEX uk_tblCategoryMap_ProductCode ON tblCategoryMap ([ProductCode]);

CREATE TABLE tblEvent (
    [EventID] COUNTER,
    [EventDate] DATETIME NOT NULL,
    [EventName] TEXT(255) NOT NULL,
    [InternalEventName] TEXT(255),
    [EventTypeID] LONG NOT NULL,
    [StatusID] LONG NOT NULL DEFAULT 1,
    [TaxRate] DOUBLE NOT NULL DEFAULT 0.07625,
    [Notes] MEMO,
    [CreatedDate] DATETIME DEFAULT Now(),
    [CreatedBy] TEXT(50),
    [ModifiedDate] DATETIME,
    [ModifiedBy] TEXT(50),
    [ClosedDate] DATETIME,
    CONSTRAINT pk_tblEvent PRIMARY KEY ([EventID])
);

CREATE INDEX ix_tblEvent_EventDate ON tblEvent ([EventDate]);

CREATE TABLE tblEventAssignment (
    [AssignmentID] COUNTER,
    [EventID] LONG NOT NULL,
    [LocationID] LONG NOT NULL,
    [VendorID] LONG NOT NULL,
    [AllocationPct] DOUBLE NOT NULL DEFAULT 1,
    [PayeeSeq] LONG,
    [AssignmentStatus] TEXT(50) DEFAULT 'PROOF / INITIAL LOAD',
    [Notes] MEMO,
    CONSTRAINT pk_tblEventAssignment PRIMARY KEY ([AssignmentID])
);


CREATE TABLE tblImportBatch (
    [BatchID] COUNTER,
    [EventID] LONG,
    [ImportType] TEXT(20) NOT NULL,
    [SourceFileName] TEXT(255) NOT NULL,
    [SourcePath] TEXT(255),
    [ImportedAt] DATETIME DEFAULT Now(),
    [ImportedBy] TEXT(50),
    [RecordCount] LONG DEFAULT 0,
    [ExceptionCount] LONG DEFAULT 0,
    [Status] TEXT(25) DEFAULT 'IMPORTED',
    [Notes] MEMO,
    CONSTRAINT pk_tblImportBatch PRIMARY KEY ([BatchID])
);


CREATE TABLE tblSalesImport (
    [SalesImportID] COUNTER,
    [BatchID] LONG NOT NULL,
    [EventID] LONG,
    [RawRow] LONG,
    [DepartmentRaw] TEXT(255),
    [LocationRaw] TEXT(255),
    [LocationID] LONG,
    [ProductCode] TEXT(25),
    [ProductName] TEXT(255),
    [ContractClassID] LONG,
    [Quantity] DOUBLE,
    [GrossAmt] CURRENCY,
    [NetAmt] CURRENCY,
    [MatchStatus] TEXT(25) DEFAULT 'UNMATCHED',
    [ExceptionNote] TEXT(255),
    CONSTRAINT pk_tblSalesImport PRIMARY KEY ([SalesImportID])
);

CREATE INDEX ix_tblSalesImport_LocationRaw ON tblSalesImport ([LocationRaw]);
CREATE INDEX ix_tblSalesImport_ProductCode ON tblSalesImport ([ProductCode]);

CREATE TABLE tblTipsImport (
    [TipsImportID] COUNTER,
    [BatchID] LONG NOT NULL,
    [EventID] LONG,
    [VendorID] LONG,
    [VendorShortCodeRaw] TEXT(25),
    [LocationID] LONG,
    [LocationRaw] TEXT(255),
    [GrossTips] CURRENCY,
    [AllocationPct] DOUBLE DEFAULT 1,
    [AllocatedTips] CURRENCY,
    [Notes] TEXT(255),
    [MatchStatus] TEXT(25) DEFAULT 'UNMATCHED',
    CONSTRAINT pk_tblTipsImport PRIMARY KEY ([TipsImportID])
);


CREATE TABLE tblSettlementHeader (
    [SettlementID] COUNTER,
    [EventID] LONG NOT NULL,
    [VendorID] LONG NOT NULL,
    [InvoiceNumber] TEXT(50),
    [SettlementType] TEXT(10) NOT NULL,
    [Status] TEXT(25) DEFAULT 'DRAFT',
    [FoodNet] CURRENCY DEFAULT 0,
    [NonAlcNet] CURRENCY DEFAULT 0,
    [BeerNet] CURRENCY DEFAULT 0,
    [LiquorNet] CURRENCY DEFAULT 0,
    [GroupNet] CURRENCY DEFAULT 0,
    [CommissionAmount] CURRENCY DEFAULT 0,
    [TipsAmount] CURRENCY DEFAULT 0,
    [AdjustmentAmount] CURRENCY DEFAULT 0,
    [AmountDue] CURRENCY DEFAULT 0,
    [StatementNotes] MEMO,
    [PreparedBy] TEXT(50),
    [PreparedDate] DATETIME,
    [ReviewedBy] TEXT(50),
    [ReviewedDate] DATETIME,
    [ApprovedBy] TEXT(50),
    [ApprovedDate] DATETIME,
    [PdfPath] TEXT(255),
    [CreatedDate] DATETIME DEFAULT Now(),
    CONSTRAINT pk_tblSettlementHeader PRIMARY KEY ([SettlementID])
);

CREATE UNIQUE INDEX uk_tblSettlementHeader_InvoiceNumber ON tblSettlementHeader ([InvoiceNumber]);

CREATE TABLE tblSettlementDetail (
    [SettlementDetailID] COUNTER,
    [SettlementID] LONG NOT NULL,
    [LocationID] LONG NOT NULL,
    [AllocationPct] DOUBLE DEFAULT 1,
    [FoodNet] CURRENCY DEFAULT 0,
    [NonAlcNet] CURRENCY DEFAULT 0,
    [BeerNet] CURRENCY DEFAULT 0,
    [LiquorNet] CURRENCY DEFAULT 0,
    [LocationNet] CURRENCY DEFAULT 0,
    [FoodCommission] CURRENCY DEFAULT 0,
    [NonAlcCommission] CURRENCY DEFAULT 0,
    [BeerCommission] CURRENCY DEFAULT 0,
    [LiquorCommission] CURRENCY DEFAULT 0,
    [TotalCommission] CURRENCY DEFAULT 0,
    [Gratuities] CURRENCY DEFAULT 0,
    CONSTRAINT pk_tblSettlementDetail PRIMARY KEY ([SettlementDetailID])
);


CREATE TABLE tblSettlementAdjustment (
    [AdjustmentID] COUNTER,
    [SettlementID] LONG NOT NULL,
    [AdjustmentTypeID] LONG NOT NULL,
    [Amount] CURRENCY NOT NULL DEFAULT 0,
    [GLCode] TEXT(20),
    [Notes] TEXT(255),
    CONSTRAINT pk_tblSettlementAdjustment PRIMARY KEY ([AdjustmentID])
);


CREATE TABLE tblDocumentRef (
    [DocumentID] COUNTER,
    [VendorID] LONG,
    [EventID] LONG,
    [SettlementID] LONG,
    [DocumentType] TEXT(25) NOT NULL,
    [DocumentPath] TEXT(255) NOT NULL,
    [OriginalFileName] TEXT(255),
    [Notes] TEXT(255),
    [CreatedDate] DATETIME DEFAULT Now(),
    CONSTRAINT pk_tblDocumentRef PRIMARY KEY ([DocumentID])
);


-- Composite unique indexes
CREATE UNIQUE INDEX uk_assignment ON tblEventAssignment ([EventID], [LocationID], [VendorID]);
CREATE UNIQUE INDEX uk_settlement_event_vendor ON tblSettlementHeader ([EventID], [VendorID]);
CREATE INDEX ix_location_code ON tblLocation ([LocationCode]);

