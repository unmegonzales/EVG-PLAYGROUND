/**
 * Event-ready = all required items complete EXCEPT shirt/uniform (item #7 excluded per spec).
 */
function computeReadiness(candidate) {
  const checks = [
    {
      key: 'creating_legends',
      label: 'Creating Legends',
      met: candidate.creating_legends_status === 'complete',
    },
    {
      key: 'success_factors',
      label: 'SuccessFactors',
      met: ['signature_step', 'post_hire_verification'].includes(candidate.sf_stage),
    },
    {
      key: 'i9',
      label: 'I-9 / e-Verify',
      met: candidate.i9_status === 'complete',
    },
    {
      key: 'alcohol',
      label: 'Alcohol Permit',
      met: candidate.alcohol_status === 'valid',
    },
    {
      key: 'food',
      label: 'Food Handler',
      met: ['uploaded', 'valid'].includes(candidate.food_handler_status),
    },
    {
      key: 'security',
      label: 'Security Photo',
      met: candidate.security_photo_status === 'validated',
    },
    {
      key: 'hr_cleared',
      label: 'HR Clearance',
      met: Boolean(candidate.hr_cleared),
    },
  ];

  const completed = checks.filter((c) => c.met).length;
  const total = checks.length;
  const percent = Math.round((completed / total) * 100);
  const missing = checks.filter((c) => !c.met).map((c) => c.label);
  const eventReady = completed === total;

  let actionFlag = '';
  if (eventReady) {
    actionFlag = 'Event Ready';
  } else if (missing.includes('Alcohol Permit') || missing.includes('Food Handler') || missing.includes('Security Photo')) {
    actionFlag = 'Missing Permits — Action Required';
  } else if (candidate.sf_stage === 'orientation_step') {
    actionFlag = 'Waiting on HR — Orientation Step';
  } else if (candidate.sf_stage === 'new_employee') {
    actionFlag = 'Waiting on Candidate — New Employee';
  } else if (missing.includes('Creating Legends')) {
    actionFlag = 'Sent CL';
  } else {
    actionFlag = 'In Progress';
  }

  return { checks, completed, total, percent, missing, eventReady, actionFlag };
}

module.exports = { computeReadiness };
