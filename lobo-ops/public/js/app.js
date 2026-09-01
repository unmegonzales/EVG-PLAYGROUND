const state = {
  view: 'active',
  department: '',
  classification: '',
  q: '',
  selectedId: null,
  meta: null,
  candidates: [],
};

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function badge(status, type) {
  const map = {
    valid: ['Valid', 'ok'],
    validated: ['Validated', 'ok'],
    complete: ['Complete', 'ok'],
    uploaded: ['Uploaded', 'info'],
    in_progress: ['In Progress', 'info'],
    no_match: ['No Match', 'bad'],
    missing: ['Missing', 'bad'],
    expired: ['Expired', 'bad'],
    temporary: ['Temp', 'warn'],
    not_started: ['Not Started', 'muted'],
    section_1: ['Sec 1', 'info'],
    section_2: ['Sec 2', 'info'],
    renewal_due: ['Renewal', 'warn'],
    new_employee: ['New Emp', 'warn'],
    orientation_step: ['Orient', 'info'],
    signature_step: ['Signature', 'info'],
    post_hire_verification: ['Post Hire', 'ok'],
  };
  const [label, cls] = map[status] || [status, 'muted'];
  return `<span class="badge badge--${cls}">${label}</span>`;
}

function clIcon(status) {
  if (status === 'complete') return '<span class="badge badge--ok">✓</span>';
  if (status === 'in_progress') return '<span class="badge badge--info">…</span>';
  return '<span class="badge badge--bad">○</span>';
}

function actionBadge(flag) {
  if (flag.includes('Event Ready')) return `<span class="badge badge--ok">${flag}</span>`;
  if (flag.includes('Missing')) return `<span class="badge badge--bad">${flag}</span>`;
  if (flag.includes('Waiting on HR')) return `<span class="badge badge--info">${flag}</span>`;
  if (flag.includes('Sent CL')) return `<span class="badge badge--warn">${flag}</span>`;
  return `<span class="badge badge--muted">${flag}</span>`;
}

async function loadMeta() {
  state.meta = await api('/api/meta');
  populateSelects();
}

function populateSelects() {
  const deptOpts = state.meta.departments.map((d) =>
    `<option value="${d.code}">${d.code} - ${d.name}</option>`
  ).join('');
  const classOpts = state.meta.classifications.map((c) =>
    `<option value="${c.id}">${c.label}</option>`
  ).join('');
  const sfOpts = state.meta.sfStages.map((s) =>
    `<option value="${s.id}">${s.label}</option>`
  ).join('');

  $('#filter-dept').innerHTML = '<option value="">All departments</option>' +
    deptOpts +
    '<option value="NPO">Non-Profit Groups (NPO)</option>';

  $('#filter-class').innerHTML = '<option value="">All types</option>' + classOpts;
  ['form-dept', 'add-dept'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.innerHTML = deptOpts + '<option value="NPO">NPO</option>';
  });
  ['form-class', 'add-class'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.innerHTML = classOpts;
  });
  const sfEl = $('#form-sf');
  if (sfEl) sfEl.innerHTML = sfOpts;
}

async function loadStats() {
  const s = await api('/api/stats');
  $('#stat-total').textContent = s.total;
  $('#stat-ready').textContent = s.eventReady;
  $('#stat-permits').textContent = s.missingPermits;
  $('#stat-hr').textContent = s.waitingHr;
}

async function loadCandidates() {
  const params = new URLSearchParams({ view: state.view });
  if (state.department) params.set('department', state.department);
  if (state.classification) params.set('classification', state.classification);
  if (state.q) params.set('q', state.q);

  state.candidates = await api(`/api/candidates?${params}`);
  renderGrid();
  $('#row-count').textContent = `${state.candidates.length} records`;
}

function renderGrid() {
  const tbody = $('#grid-body');
  tbody.innerHTML = state.candidates.map((c) => `
    <tr data-id="${c.id}" class="${c.id === state.selectedId ? 'selected' : ''}">
      <td>${actionBadge(c.action_flag)}</td>
      <td>${clIcon(c.creating_legends_status)}</td>
      <td>${badge(c.alcohol_status)}</td>
      <td>${badge(c.food_handler_status)}</td>
      <td>${badge(c.security_photo_status)}</td>
      <td>${badge(c.sf_stage)}</td>
      <td>${badge(c.i9_status)}</td>
      <td>${c.hr_cleared ? '<span class="badge badge--ok">✓</span>' : '<span class="badge badge--muted">○</span>'}</td>
      <td><span class="pct ${c.eventReady ? 'pct--ready' : ''}">${c.percent}%</span></td>
      <td><strong>${c.full_name}</strong></td>
      <td>${c.email || '—'}</td>
      <td>${c.department_label || c.department_code}</td>
      <td>${c.classification_label}</td>
    </tr>
  `).join('');

  tbody.querySelectorAll('tr').forEach((tr) => {
    tr.addEventListener('click', () => openDetail(Number(tr.dataset.id)));
  });
}

async function openDetail(id) {
  state.selectedId = id;
  renderGrid();
  const data = await api(`/api/candidates/${id}`);
  $('#detail-panel').hidden = false;
  document.querySelector('.layout').classList.add('has-detail');

  $('#detail-name').textContent = data.full_name;
  $('#detail-readiness').textContent = data.eventReady
    ? '✅ Event Ready — cleared for work'
    : `${data.percent}% complete — missing: ${data.missing.join(', ')}`;

  $('#readiness-bars').innerHTML = data.checks.map((ch) => `
    <div class="check-row">
      <span class="check-dot ${ch.met ? 'check-dot--ok' : 'check-dot--no'}"></span>
      <span>${ch.label}</span>
    </div>
  `).join('');

  const form = $('#detail-form');
  for (const el of form.elements) {
    if (!el.name) continue;
    if (el.type === 'checkbox') {
      el.checked = Boolean(data[el.name]);
    } else if (data[el.name] != null) {
      el.value = data[el.name];
    }
  }

  $('#activity-log').innerHTML = `
    <h4>Activity Log</h4>
    ${(data.activity || []).slice(0, 10).map((a) => `
      <div class="activity-item">
        <strong>${a.field_name}</strong>: ${a.old_value || '—'} → ${a.new_value}
        <br><small>${a.created_at} · ${a.changed_by}</small>
      </div>
    `).join('') || '<p class="activity-item">No activity yet.</p>'}
  `;
}

async function saveDetail(e) {
  e.preventDefault();
  const form = $('#detail-form');
  const body = {};
  for (const el of form.elements) {
    if (!el.name) continue;
    if (el.type === 'checkbox') body[el.name] = el.checked ? 1 : 0;
    else body[el.name] = el.value;
  }
  await api(`/api/candidates/${state.selectedId}`, { method: 'PATCH', body: JSON.stringify(body) });
  await Promise.all([loadCandidates(), loadStats(), openDetail(state.selectedId)]);
}

async function sendEmail(template) {
  if (!state.selectedId) return;
  const result = await api(`/api/candidates/${state.selectedId}/send-email`, {
    method: 'POST',
    body: JSON.stringify({ template, trigger: 'manual' }),
  });
  $('#email-status').textContent = result.message;
  if (!result.success && result.message.includes('PowerShell')) {
    $('#email-status').innerHTML = `${result.message}<br><br><strong>No npm needed:</strong> Run <code>lobo-ops/scripts/send-onboarding-email.ps1</code> on your Windows PC with Outlook open. See docs/OUTLOOK-SETUP.md`;
  }
  const iframe = $('#email-preview');
  iframe.srcdoc = result.preview.html;
  $('#modal-email').showModal();
  await openDetail(state.selectedId);
}

async function addCandidate(e) {
  e.preventDefault();
  const form = $('#add-form');
  const body = Object.fromEntries(new FormData(form));
  delete body.send_email;
  const created = await api('/api/candidates', { method: 'POST', body: JSON.stringify(body) });
  $('#modal-add').close();
  form.reset();
  if (form.send_email?.checked) {
    state.selectedId = created.id;
    await sendEmail('onboarding');
  }
  await Promise.all([loadCandidates(), loadStats()]);
  openDetail(created.id);
}

function bindEvents() {
  $$('.nav-item').forEach((btn) => {
    btn.addEventListener('click', () => {
      $$('.nav-item').forEach((b) => b.classList.remove('nav-item--active'));
      btn.classList.add('nav-item--active');
      state.view = btn.dataset.view;
      loadCandidates();
    });
  });

  $('#filter-dept').addEventListener('change', (e) => {
    state.department = e.target.value;
    loadCandidates();
  });

  $('#filter-class').addEventListener('change', (e) => {
    state.classification = e.target.value;
    loadCandidates();
  });

  let searchTimer;
  $('#search').addEventListener('input', (e) => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      state.q = e.target.value.trim();
      loadCandidates();
    }, 250);
  });

  $('#btn-add').addEventListener('click', () => $('#modal-add').showModal());
  $('#btn-cancel-add').addEventListener('click', () => $('#modal-add').close());
  $('#add-form').addEventListener('submit', addCandidate);

  $('#btn-close-detail').addEventListener('click', () => {
    $('#detail-panel').hidden = true;
    state.selectedId = null;
    renderGrid();
  });

  $('#detail-form').addEventListener('submit', saveDetail);
  $('#btn-send-onboarding').addEventListener('click', () => sendEmail('onboarding'));
  $('#btn-send-cl').addEventListener('click', () => sendEmail('cl_reminder'));
  $('#btn-close-email').addEventListener('click', () => $('#modal-email').close());

  $('#btn-export').addEventListener('click', () => {
    window.location.href = '/api/export/csv';
  });
}

async function init() {
  bindEvents();
  await loadMeta();
  await Promise.all([loadCandidates(), loadStats()]);
}

init();
