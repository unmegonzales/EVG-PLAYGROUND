const { FORM_LINKS } = require('../db/constants');

function buildOnboardingEmail(candidate) {
  const name = candidate.first_name || 'Team Member';
  const subject = "✅ You're Almost Ready! Complete Your Levy UNM Onboarding";

  const html = `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>${subject}</title></head>
<body style="font-family:Segoe UI,Arial,sans-serif;background:#f4f4f4;margin:0;padding:24px;">
  <div style="max-width:640px;margin:0 auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08);">
    <div style="background:#1a1a2e;color:#fff;padding:24px 32px;">
      <p style="margin:0;font-size:12px;letter-spacing:.12em;opacity:.8;">LEVY × UNM ATHLETICS</p>
      <h1 style="margin:8px 0 0;font-size:28px;">Welcome, ${name}!</h1>
      <p style="margin:12px 0 0;opacity:.9;">Complete your onboarding checklist to prepare for your first shift.</p>
    </div>
    <div style="padding:32px;">
      <p style="color:#555;">Hi ${name},</p>
      <p style="color:#333;line-height:1.6;">We're excited to have you join the Levy Lobos Family. Complete the steps below — estimated time ~2.5 hours (compensated on or near your first paycheck).</p>

      <h2 style="color:#ba0c2f;margin-top:32px;">🎯 First Shift Readiness Checklist</h2>
      <ol style="line-height:2;color:#333;">
        <li><strong>Creating Legends Training</strong> — <a href="${FORM_LINKS.creatingLegends}">Start Training</a></li>
        <li><strong>Employment Paperwork</strong> — Complete via Adobe Sign / SuccessFactors</li>
        <li><strong>Required Uploads:</strong>
          <ul>
            <li><a href="${FORM_LINKS.alcohol}">NM Alcohol Server Permit</a></li>
            <li><a href="${FORM_LINKS.food}">Food Handler Permit</a></li>
            <li><a href="${FORM_LINKS.security}">UNM Athletics Photo Upload</a></li>
          </ul>
        </li>
        <li><strong>Resources:</strong> <a href="${FORM_LINKS.digitalDen}">Digital Den</a></li>
      </ol>

      <p style="margin-top:32px;color:#333;">Once all requirements are verified, you'll be cleared to work events.</p>
      <p style="color:#333;">Welcome to the team!<br><strong>Evan E. Gonzales</strong><br>Finance & Human Resources Manager<br>Levy at UNM Athletics</p>
    </div>
    <div style="background:#f0f0f0;padding:16px 32px;font-size:12px;color:#666;">
      Creating Legendary Experiences. © 2026 Compass Group USA, Inc.
    </div>
  </div>
</body>
</html>`;

  const text = `Welcome ${name}! Complete your Levy UNM onboarding:
1. Creating Legends: ${FORM_LINKS.creatingLegends}
2. Alcohol Permit: ${FORM_LINKS.alcohol}
3. Food Handler: ${FORM_LINKS.food}
4. Security Photo: ${FORM_LINKS.security}
— Evan Gonzales, Levy UNM HR`;

  return { subject, html, text, to: candidate.email };
}

module.exports = { buildOnboardingEmail };
