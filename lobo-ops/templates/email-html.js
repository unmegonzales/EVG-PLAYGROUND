const { FORM_LINKS } = require('../db/constants');

const ASSETS = {
  levyLogo: 'https://unmegonzales.github.io/ZERO-Communications/email/assets/Levy-Logo.png',
  unmLogo: 'https://unmegonzales.github.io/ZERO-Communications/email/assets/unm-logo.png',
  hero: 'https://unmegonzales.github.io/ZERO-Communications/email/assets/Hero.png',
};

const ADOBE_SIGN = process.env.ADOBE_SIGN_URL ||
  'https://unm-levy.na4.documents.adobe.com/public/esignWidget?wid=CBFCIBAA3AAABLblqZhApEIJQtFaQg-Xe022g-FS947VuAc3TkuD93kf7sIPQg3VN14Kr2khqpvaLZyZPQGk*&hosted=false';

function buildOnboardingEmail(candidate) {
  const name = candidate.first_name || 'Team Member';
  const subject = "✅ You're Almost Ready! Complete Your Levy UNM Onboarding";

  const html = `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f0f0f0;font-family:'Segoe UI',Arial,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f0f0f0;padding:24px 0;">
    <tr><td align="center">
      <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;max-width:600px;">
        <tr><td style="padding:24px 32px;text-align:center;">
          <img src="${ASSETS.levyLogo}" alt="Levy" height="40" style="margin-right:16px;">
          <img src="${ASSETS.unmLogo}" alt="UNM Athletics" height="40">
        </td></tr>
        <tr><td><img src="${ASSETS.hero}" alt="" width="600" style="display:block;width:100%;max-width:600px;"></td></tr>
        <tr><td style="padding:32px;">
          <p style="margin:0 0 8px;font-size:11px;letter-spacing:0.14em;color:#ba0c2f;font-weight:700;">LEVY × UNM ATHLETICS</p>
          <h1 style="margin:0 0 16px;font-size:26px;color:#1a1a2e;">Welcome to the Lobo Hospitality Team</h1>
          <p style="color:#444;line-height:1.6;">Hi ${name},</p>
          <p style="color:#444;line-height:1.6;">We're excited to have you join the Levy Lobos Family. Complete the onboarding checklist below to prepare for your first shift and become event-ready.</p>
          <p style="color:#666;font-size:14px;"><strong>⏱ Estimated time:</strong> ~2.5 hours (compensated on or near your first paycheck)</p>

          <h2 style="color:#ba0c2f;font-size:18px;margin-top:32px;">🎯 First Shift Readiness Checklist</h2>
          <table role="presentation" width="100%" cellpadding="8" cellspacing="0" style="margin:16px 0;">
            <tr style="background:#f8f8f8;"><td width="28">1</td><td><strong>Creating Legends Training</strong><br><a href="${FORM_LINKS.creatingLegends}" style="color:#ba0c2f;">Start Training →</a><br><small>Download your certificate — you'll need it for paperwork.</small></td></tr>
            <tr><td>2</td><td><strong>Employment Paperwork</strong><br><a href="${ADOBE_SIGN}" style="color:#ba0c2f;">Review &amp; Sign Documents →</a></td></tr>
            <tr style="background:#f8f8f8;"><td>3</td><td><strong>Required Uploads</strong><br>
              <a href="${FORM_LINKS.alcohol}">🍷 NM Alcohol Server Permit</a><br>
              <a href="${FORM_LINKS.food}">🍴 Food Handler Permit</a><br>
              <a href="${FORM_LINKS.security}">📷 UNM Athletics Photo Upload</a>
            </td></tr>
            <tr><td>4</td><td><strong>Resources</strong><br><a href="${FORM_LINKS.digitalDen}">Digital Den →</a></td></tr>
          </table>

          <p style="color:#444;line-height:1.6;margin-top:24px;">Once all requirements are verified, you'll be cleared to work events.</p>
          <p style="color:#444;line-height:1.6;">Welcome to the team!<br><br>
            <strong>Evan E. Gonzales</strong><br>
            Finance &amp; Human Resources Manager<br>
            Levy at UNM Athletics<br>
            <a href="mailto:egonzales@levyrestaurants.com">egonzales@levyrestaurants.com</a><br>
            Office: 505.925.1576 · Cell: 505.549.6545
          </p>
        </td></tr>
        <tr><td style="background:#1a1a2e;color:#aaa;padding:16px 32px;font-size:11px;text-align:center;">
          Creating Legendary Experiences. © 2026 Compass Group USA, Inc.
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>`;

  const text = `Welcome ${name}!

Complete your Levy UNM onboarding (~2.5 hrs, compensated):

1. Creating Legends: ${FORM_LINKS.creatingLegends}
2. Employment Paperwork: ${ADOBE_SIGN}
3. Alcohol Permit: ${FORM_LINKS.alcohol}
4. Food Handler: ${FORM_LINKS.food}
5. Security Photo: ${FORM_LINKS.security}
6. Digital Den: ${FORM_LINKS.digitalDen}

— Evan Gonzales, Levy UNM HR
egonzales@levyrestaurants.com | 505.925.1576`;

  return { subject, html, text, to: candidate.email };
}

function buildClReminderEmail(candidate) {
  const name = candidate.first_name || 'Team Member';
  const subject = 'Reminder: Complete Creating Legends Training — Levy UNM';
  const html = `<p>Hi ${name},</p>
<p>This is a friendly reminder to complete your <strong>Creating Legends Virtual Orientation</strong> before your first shift.</p>
<p><a href="${FORM_LINKS.creatingLegends}">Start or continue training →</a></p>
<p>Download your certificate when finished — you'll upload it during employment paperwork.</p>
<p>— Evan Gonzales, Levy UNM HR</p>`;
  const text = `Hi ${name}, please complete Creating Legends: ${FORM_LINKS.creatingLegends}`;
  return { subject, html, text, to: candidate.email };
}

function buildEmail(template, candidate) {
  if (template === 'cl_reminder') return buildClReminderEmail(candidate);
  return buildOnboardingEmail(candidate);
}

module.exports = { buildEmail, buildOnboardingEmail, buildClReminderEmail, ASSETS };
