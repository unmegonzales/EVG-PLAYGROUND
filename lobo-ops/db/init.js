const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const dbPath = path.join(__dirname, 'lobo-ops.db');
if (fs.existsSync(dbPath)) fs.unlinkSync(dbPath);

const db = new Database(dbPath);
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

db.exec(`
  CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    employee_id TEXT,
    clock_in_code TEXT,
    position TEXT,
    department_code TEXT,
    classification TEXT NOT NULL DEFAULT 'levy_employee',
    manager TEXT,
    hr_manager TEXT DEFAULT 'Evan Gonzales',
    hourly_rate REAL,
    hire_date TEXT,
    uniform_size TEXT,
    season TEXT DEFAULT '26/27 UNM Athletic Season',
    active INTEGER NOT NULL DEFAULT 1,

    creating_legends_status TEXT DEFAULT 'missing',
    creating_legends_paid INTEGER DEFAULT 0,
    sf_stage TEXT DEFAULT 'new_employee',
    adobe_sign_status TEXT DEFAULT 'pending',
    i9_status TEXT DEFAULT 'not_started',
    i9_renewal_date TEXT,
    i9_notes TEXT,

    alcohol_status TEXT DEFAULT 'missing',
    alcohol_permit_id TEXT,
    alcohol_expiration TEXT,
    alcohol_temp_permanent TEXT,

    food_handler_status TEXT DEFAULT 'missing',
    security_photo_status TEXT DEFAULT 'missing',
    shirt_status TEXT DEFAULT 'missing',

    levy_license_auth INTEGER DEFAULT 0,
    levy_license_expiration TEXT,
    tip_credit_notice_date TEXT,

    hr_cleared INTEGER DEFAULT 0,
    hr_cleared_date TEXT,
    notes TEXT,
    action_override TEXT,

    onboarding_email_sent_at TEXT,
    cl_reminder_sent_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
  );

  CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER NOT NULL,
    field_name TEXT,
    old_value TEXT,
    new_value TEXT,
    changed_by TEXT DEFAULT 'system',
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
  );

  CREATE TABLE email_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    recipient TEXT NOT NULL,
    template TEXT NOT NULL,
    trigger_reason TEXT,
    status TEXT DEFAULT 'queued',
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE SET NULL
  );
`);

const insert = db.prepare(`
  INSERT INTO candidates (
    first_name, last_name, email, phone, employee_id, position, department_code,
    classification, manager, hourly_rate, hire_date,
    creating_legends_status, sf_stage, i9_status,
    alcohol_status, alcohol_permit_id, alcohol_expiration, alcohol_temp_permanent,
    food_handler_status, security_photo_status, shirt_status,
    hr_cleared, notes
  ) VALUES (
    @first_name, @last_name, @email, @phone, @employee_id, @position, @department_code,
    @classification, @manager, @hourly_rate, @hire_date,
    @creating_legends_status, @sf_stage, @i9_status,
    @alcohol_status, @alcohol_permit_id, @alcohol_expiration, @alcohol_temp_permanent,
    @food_handler_status, @security_photo_status, @shirt_status,
    @hr_cleared, @notes
  )
`);

function row(data) {
  return {
    phone: null,
    employee_id: null,
    alcohol_permit_id: null,
    alcohol_expiration: null,
    alcohol_temp_permanent: null,
    notes: '',
    hr_cleared: 0,
    ...data,
  };
}

const seed = [
  {
    first_name: 'Miriam', last_name: 'Alvarado', email: 'Miriamalvarado127@gmail.com',
    phone: '505-810-7188', employee_id: '10743653', position: 'CASHIER, CONCESSION',
    department_code: '36127', classification: 'levy_employee', manager: 'Abigail Tenorio',
    hourly_rate: 15.5, hire_date: '2025-08-08',
    creating_legends_status: 'missing', sf_stage: 'new_employee', i9_status: 'not_started',
    alcohol_status: 'no_match', food_handler_status: 'missing', security_photo_status: 'missing',
    shirt_status: 'missing', hr_cleared: 0, notes: 'Missing Permits — Action Required',
  },
  {
    first_name: 'Desiree', last_name: 'Amaral', email: 'xoxodes@gmail.com',
    phone: '505-737-4009', employee_id: '10352972', position: 'CASHIER, CONCESSION',
    department_code: '36127', classification: 'levy_employee', manager: 'Abigail Tenorio',
    hourly_rate: 16, hire_date: '2023-08-01',
    creating_legends_status: 'complete', sf_stage: 'signature_step', i9_status: 'complete',
    alcohol_status: 'valid', alcohol_permit_id: 'S145747', alcohol_expiration: '2027-08-18',
    alcohol_temp_permanent: 'PERMANENT', food_handler_status: 'uploaded',
    security_photo_status: 'validated', shirt_status: 'uploaded', hr_cleared: 1,
    notes: '',
  },
  {
    first_name: 'LaDonna', last_name: 'Bacca', email: 'la187198@yahoo.com',
    phone: '505-659-9235', employee_id: '10610160', position: 'SUPV, CONCESSIONS',
    department_code: '36127', classification: 'levy_employee', manager: 'Abigail Tenorio',
    hourly_rate: 22, hire_date: '2024-10-21',
    creating_legends_status: 'complete', sf_stage: 'orientation_step', i9_status: 'section_2',
    alcohol_status: 'valid', food_handler_status: 'uploaded', security_photo_status: 'uploaded',
    shirt_status: 'missing', hr_cleared: 0, notes: 'Sent CL',
  },
  {
    first_name: 'Jessie', last_name: 'Johnston', email: 'jjohnston2@comcast.net',
    phone: '', employee_id: '', position: 'EVENT STAFF',
    department_code: '36127', classification: 'levy_employee', manager: 'Abigail Tenorio',
    hourly_rate: 15.5, hire_date: '2026-07-17',
    creating_legends_status: 'in_progress', sf_stage: 'new_employee', i9_status: 'not_started',
    alcohol_status: 'valid', alcohol_permit_id: 'S145747', alcohol_expiration: '2027-08-18',
    alcohol_temp_permanent: 'PERMANENT', food_handler_status: 'missing',
    security_photo_status: 'missing', shirt_status: 'missing', hr_cleared: 0, notes: '',
  },
  {
    first_name: 'Paula', last_name: 'Samora', email: 'samoracc@aol.com',
    phone: '', employee_id: '', position: 'EVENT STAFF',
    department_code: '36127', classification: 'levy_employee', manager: 'Abigail Tenorio',
    hourly_rate: 15.5, hire_date: '2026-07-19',
    creating_legends_status: 'missing', sf_stage: 'new_employee', i9_status: 'not_started',
    alcohol_status: 'valid', alcohol_permit_id: '0', alcohol_expiration: '2028-02-23',
    alcohol_temp_permanent: 'PERMANENT', food_handler_status: 'missing',
    security_photo_status: 'uploaded', shirt_status: 'missing', hr_cleared: 0, notes: '',
  },
  {
    first_name: 'Marina', last_name: 'Gonzales', email: 'mgonzales@example.com',
    phone: '', employee_id: '', position: 'NPO VOLUNTEER',
    department_code: 'NPO', classification: 'npo', manager: 'Evan Gonzales',
    hourly_rate: 0, hire_date: '2026-08-01',
    creating_legends_status: 'in_progress', sf_stage: 'new_employee', i9_status: 'not_started',
    alcohol_status: 'missing', food_handler_status: 'missing',
    security_photo_status: 'missing', shirt_status: 'missing', hr_cleared: 0,
    notes: 'NPO - ARVC affiliated',
  },
  {
    first_name: 'LyoneL', last_name: 'Candelaria', email: 'lcandelaria@example.com',
    phone: '', employee_id: '', position: 'WAREHOUSE',
    department_code: '57039', classification: 'levy_employee', manager: 'Evan Gonzales',
    hourly_rate: 16, hire_date: '2026-06-01',
    creating_legends_status: 'complete', sf_stage: 'post_hire_verification', i9_status: 'complete',
    alcohol_status: 'valid', food_handler_status: 'uploaded',
    security_photo_status: 'validated', shirt_status: 'uploaded', hr_cleared: 1,
    notes: 'VALIDATED security photo',
  },
];

const tx = db.transaction((rows) => {
  for (const r of rows) insert.run(row(r));
});

tx(seed);
console.log(`Initialized database with ${seed.length} sample candidates at ${dbPath}`);
db.close();
