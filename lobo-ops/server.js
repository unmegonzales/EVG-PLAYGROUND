const express = require('express');
const path = require('path');
const Database = require('better-sqlite3');
const { computeReadiness } = require('./db/event-ready');
const {
  DEPARTMENTS,
  CLASSIFICATIONS,
  SF_STAGES,
  FORM_LINKS,
} = require('./db/constants');
const { buildOnboardingEmail } = require('./templates/onboarding-email');

const app = express();
const PORT = process.env.PORT || 3847;
const dbPath = path.join(__dirname, 'db', 'lobo-ops.db');

if (!require('fs').existsSync(dbPath)) {
  require('./db/init');
}

const db = new Database(dbPath);
db.pragma('journal_mode = WAL');

app.use(express.json({ limit: '2mb' }));
app.use(express.static(path.join(__dirname, 'public')));

function enrich(candidate) {
  const readiness = computeReadiness(candidate);
  const dept = DEPARTMENTS.find((d) => d.code === candidate.department_code);
  const classification = CLASSIFICATIONS.find((c) => c.id === candidate.classification);
  const sf = SF_STAGES.find((s) => s.id === candidate.sf_stage);
  return {
    ...candidate,
    full_name: `${candidate.last_name}, ${candidate.first_name}`,
    department_label: dept ? `${dept.code} - ${dept.name}` : candidate.department_code,
    classification_label: classification?.label || candidate.classification,
    sf_stage_label: sf?.label || candidate.sf_stage,
    waiting_on: sf?.waitingOn || null,
    ...readiness,
    action_flag: candidate.action_override || readiness.actionFlag,
  };
}

function logActivity(candidateId, fieldName, oldValue, newValue, changedBy = 'HR User') {
  db.prepare(`
    INSERT INTO activity_log (candidate_id, field_name, old_value, new_value, changed_by)
    VALUES (?, ?, ?, ?, ?)
  `).run(candidateId, fieldName, String(oldValue ?? ''), String(newValue ?? ''), changedBy);
}

function applyViewFilter(view, rows) {
  switch (view) {
    case 'waiting_candidate':
      return rows.filter((r) =>
        r.sf_stage === 'new_employee' ||
        r.creating_legends_status !== 'complete' ||
        ['missing', 'no_match'].includes(r.alcohol_status) ||
        r.food_handler_status === 'missing' ||
        r.security_photo_status === 'missing'
      );
    case 'waiting_hr':
      return rows.filter((r) => r.sf_stage === 'orientation_step' || r.sf_stage === 'post_hire_verification');
    case 'missing_permits':
      return rows.filter((r) =>
        ['missing', 'no_match', 'expired'].includes(r.alcohol_status) ||
        r.food_handler_status === 'missing' ||
        ['missing', 'uploaded'].includes(r.security_photo_status)
      );
    case 'almost_ready':
      return rows.filter((r) => r.percent >= 70 && !r.eventReady);
    case 'event_ready':
      return rows.filter((r) => r.eventReady);
    case 'inactive':
      return rows.filter((r) => !r.active);
    case 'active':
    default:
      return rows.filter((r) => r.active);
  }
}

app.get('/api/meta', (_req, res) => {
  res.json({ departments: DEPARTMENTS, classifications: CLASSIFICATIONS, sfStages: SF_STAGES, formLinks: FORM_LINKS });
});

app.get('/api/candidates', (req, res) => {
  const { view = 'active', department, classification, q } = req.query;
  let rows = db.prepare('SELECT * FROM candidates ORDER BY last_name, first_name').all().map(enrich);
  rows = applyViewFilter(view, rows);
  if (department) rows = rows.filter((r) => r.department_code === department);
  if (classification) rows = rows.filter((r) => r.classification === classification);
  if (q) {
    const term = q.toLowerCase();
    rows = rows.filter((r) =>
      r.full_name.toLowerCase().includes(term) ||
      (r.email || '').toLowerCase().includes(term) ||
      (r.employee_id || '').includes(term)
    );
  }
  res.json(rows);
});

app.get('/api/candidates/:id', (req, res) => {
  const row = db.prepare('SELECT * FROM candidates WHERE id = ?').get(req.params.id);
  if (!row) return res.status(404).json({ error: 'Not found' });
  const activity = db.prepare('SELECT * FROM activity_log WHERE candidate_id = ? ORDER BY created_at DESC LIMIT 50').all(req.params.id);
  const emails = db.prepare('SELECT * FROM email_log WHERE candidate_id = ? ORDER BY created_at DESC LIMIT 20').all(req.params.id);
  res.json({ ...enrich(row), activity, emails });
});

app.post('/api/candidates', (req, res) => {
  const fields = req.body;
  const stmt = db.prepare(`
    INSERT INTO candidates (
      first_name, last_name, email, phone, employee_id, clock_in_code, position,
      department_code, classification, manager, hourly_rate, hire_date, uniform_size, notes
    ) VALUES (
      @first_name, @last_name, @email, @phone, @employee_id, @clock_in_code, @position,
      @department_code, @classification, @manager, @hourly_rate, @hire_date, @uniform_size, @notes
    )
  `);
  const result = stmt.run({
    first_name: fields.first_name,
    last_name: fields.last_name,
    email: fields.email || null,
    phone: fields.phone || null,
    employee_id: fields.employee_id || null,
    clock_in_code: fields.clock_in_code || null,
    position: fields.position || null,
    department_code: fields.department_code || '36127',
    classification: fields.classification || 'levy_employee',
    manager: fields.manager || null,
    hourly_rate: fields.hourly_rate || null,
    hire_date: fields.hire_date || null,
    uniform_size: fields.uniform_size || null,
    notes: fields.notes || null,
  });
  logActivity(result.lastInsertRowid, 'created', '', `${fields.last_name}, ${fields.first_name}`);
  const created = enrich(db.prepare('SELECT * FROM candidates WHERE id = ?').get(result.lastInsertRowid));
  res.status(201).json(created);
});

app.patch('/api/candidates/:id', (req, res) => {
  const existing = db.prepare('SELECT * FROM candidates WHERE id = ?').get(req.params.id);
  if (!existing) return res.status(404).json({ error: 'Not found' });

  const allowed = [
    'first_name', 'last_name', 'email', 'phone', 'employee_id', 'clock_in_code', 'position',
    'department_code', 'classification', 'manager', 'hourly_rate', 'hire_date', 'uniform_size',
    'season', 'active', 'creating_legends_status', 'creating_legends_paid', 'sf_stage',
    'adobe_sign_status', 'i9_status', 'i9_renewal_date', 'i9_notes',
    'alcohol_status', 'alcohol_permit_id', 'alcohol_expiration', 'alcohol_temp_permanent',
    'food_handler_status', 'security_photo_status', 'shirt_status',
    'levy_license_auth', 'levy_license_expiration', 'tip_credit_notice_date',
    'hr_cleared', 'hr_cleared_date', 'notes', 'action_override',
  ];

  const updates = [];
  const values = {};
  for (const key of allowed) {
    if (Object.prototype.hasOwnProperty.call(req.body, key)) {
      updates.push(`${key} = @${key}`);
      values[key] = req.body[key];
      if (String(existing[key]) !== String(req.body[key])) {
        logActivity(existing.id, key, existing[key], req.body[key], req.body.changed_by || 'HR User');
      }
    }
  }
  if (!updates.length) return res.status(400).json({ error: 'No valid fields' });

  updates.push("updated_at = datetime('now')");
  db.prepare(`UPDATE candidates SET ${updates.join(', ')} WHERE id = @id`).run({ ...values, id: existing.id });
  res.json(enrich(db.prepare('SELECT * FROM candidates WHERE id = ?').get(existing.id)));
});

app.post('/api/candidates/:id/send-email', (req, res) => {
  const candidate = db.prepare('SELECT * FROM candidates WHERE id = ?').get(req.params.id);
  if (!candidate) return res.status(404).json({ error: 'Not found' });

  const template = req.body.template || 'onboarding';
  const trigger = req.body.trigger || 'manual';
  const email = buildOnboardingEmail(candidate);

  db.prepare(`
    INSERT INTO email_log (candidate_id, recipient, template, trigger_reason, status)
    VALUES (?, ?, ?, ?, ?)
  `).run(candidate.id, candidate.email, template, trigger, 'queued');

  const now = new Date().toISOString();
  if (template === 'onboarding') {
    db.prepare(`UPDATE candidates SET onboarding_email_sent_at = ?, updated_at = datetime('now') WHERE id = ?`).run(now, candidate.id);
  } else if (template === 'cl_reminder') {
    db.prepare(`UPDATE candidates SET cl_reminder_sent_at = ?, updated_at = datetime('now') WHERE id = ?`).run(now, candidate.id);
  }

  logActivity(candidate.id, 'email_sent', '', `${template} → ${candidate.email}`);

  res.json({
    success: true,
    message: `Email queued for ${candidate.email}. Connect Microsoft 365 to send automatically; use preview below for manual send.`,
    preview: email,
  });
});

app.get('/api/stats', (_req, res) => {
  const rows = db.prepare('SELECT * FROM candidates WHERE active = 1').all().map(enrich);
  res.json({
    total: rows.length,
    eventReady: rows.filter((r) => r.eventReady).length,
    missingPermits: rows.filter((r) => r.action_flag.includes('Missing Permits')).length,
    waitingHr: rows.filter((r) => r.sf_stage === 'orientation_step').length,
    waitingCandidate: rows.filter((r) => r.sf_stage === 'new_employee').length,
  });
});

app.get('/api/export/csv', (_req, res) => {
  const rows = db.prepare('SELECT * FROM candidates WHERE active = 1 ORDER BY last_name').all().map(enrich);
  const headers = [
    'Full Name', 'Email', 'Department', 'Classification', 'SF Stage', 'Creating Legends',
    'Alcohol', 'Food Handler', 'Security Photo', 'I-9', 'HR Cleared', 'Readiness %', 'Action Flag',
  ];
  const lines = [headers.join(',')];
  for (const r of rows) {
    lines.push([
      `"${r.full_name}"`, `"${r.email || ''}"`, `"${r.department_label}"`, `"${r.classification_label}"`,
      `"${r.sf_stage_label}"`, r.creating_legends_status, r.alcohol_status, r.food_handler_status,
      r.security_photo_status, r.i9_status, r.hr_cleared ? 'Yes' : 'No', r.percent, `"${r.action_flag}"`,
    ].join(','));
  }
  res.setHeader('Content-Type', 'text/csv');
  res.setHeader('Content-Disposition', 'attachment; filename=lobo-ops-roster.csv');
  res.send(lines.join('\n'));
});

app.get('*', (_req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Lobo Ops running at http://localhost:${PORT}`);
});
