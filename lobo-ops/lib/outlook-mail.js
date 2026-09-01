/**
 * Microsoft 365 / Outlook mail via Graph API (client credentials).
 * Requires Azure app registration — see docs/OUTLOOK-SETUP.md
 */

const GRAPH = 'https://graph.microsoft.com/v1.0';

function getConfig() {
  return {
    tenantId: process.env.AZURE_TENANT_ID,
    clientId: process.env.AZURE_CLIENT_ID,
    clientSecret: process.env.AZURE_CLIENT_SECRET,
    sendAs: process.env.OUTLOOK_SEND_AS || 'egonzales@levyrestaurants.com',
  };
}

function isConfigured() {
  const c = getConfig();
  return Boolean(c.tenantId && c.clientId && c.clientSecret && c.sendAs);
}

async function getAccessToken() {
  const { tenantId, clientId, clientSecret } = getConfig();
  const res = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: clientId,
      client_secret: clientSecret,
      scope: 'https://graph.microsoft.com/.default',
      grant_type: 'client_credentials',
    }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Azure token failed (${res.status}): ${err}`);
  }
  const data = await res.json();
  return data.access_token;
}

async function sendOutlookEmail({ to, subject, html, text }) {
  if (!to) throw new Error('Recipient email is required');
  if (!isConfigured()) {
    return { sent: false, mode: 'preview_only', reason: 'Graph API not configured — set AZURE_* env vars' };
  }

  const token = await getAccessToken();
  const { sendAs } = getConfig();

  const res = await fetch(`${GRAPH}/users/${encodeURIComponent(sendAs)}/sendMail`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: {
        subject,
        body: { contentType: 'HTML', content: html },
        toRecipients: [{ emailAddress: { address: to } }],
      },
      saveToSentItems: true,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Graph sendMail failed (${res.status}): ${err}`);
  }

  return { sent: true, mode: 'graph_api', from: sendAs, to };
}

module.exports = { isConfigured, sendOutlookEmail, getConfig };
