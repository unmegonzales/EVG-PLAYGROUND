# Outlook / Microsoft 365 Email Setup

You have **three options** — pick what fits your situation.

---

## Option A: PowerShell + Outlook (no Node, no npm) ⭐ Start here

**Best for:** Evan's Windows PC with Outlook already open.

### Steps

1. Open **PowerShell** (not necessarily admin).
2. Go to the scripts folder:
   ```powershell
   cd path\to\EVG-PLAYGROUND\lobo-ops\scripts
   ```
3. **Preview first** (opens draft in Outlook — you click Send):
   ```powershell
   .\send-onboarding-email.ps1 -To "newhire@email.com" -FirstName "Jessie" -Preview
   ```
4. **Send directly**:
   ```powershell
   .\send-onboarding-email.ps1 -To "newhire@email.com" -FirstName "Jessie"
   ```
5. **Multiple recipients**:
   ```powershell
   .\send-onboarding-email.ps1 -To "a@email.com","b@email.com" -FirstName "Team" -Preview
   ```
6. **Creating Legends reminder**:
   ```powershell
   .\send-onboarding-email.ps1 -To "newhire@email.com" -FirstName "Jessie" -ClReminder -Preview
   ```

### If script is blocked

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Requirements

- Microsoft Outlook desktop installed
- Logged into `egonzales@levyrestaurants.com` (or change `-FromAddress`)
- Internet access (email loads Levy/UNM images from GitHub)

---

## Option B: Microsoft Graph API (automated, for hosted Lobo Ops)

**Best for:** When Lobo Ops runs on a server and sends without you clicking Send.

### What IT needs to register (Azure Portal)

1. **Azure AD → App registrations → New registration**
   - Name: `Lobo Ops UNM Onboarding`
   - Supported account types: Single tenant (Levy)

2. **API permissions → Add → Microsoft Graph → Application permissions**
   - `Mail.Send`
   - Click **Grant admin consent** (requires Levy IT admin)

3. **Certificates & secrets → New client secret** — copy the value

4. **Note these values:**
   - Application (client) ID
   - Directory (tenant) ID
   - Client secret value

### Environment variables (`.env` or server config)

```env
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-secret
OUTLOOK_SEND_AS=egonzales@levyrestaurants.com
```

### Test from Lobo Ops app

When env vars are set, clicking **Send Onboarding Email** in Lobo Ops sends via Graph and saves to Sent Items.

Check status: `GET http://localhost:3847/api/email/status`

---

## Option C: Install Node.js (run full Lobo Ops locally)

If you want the full warehouse app on your PC:

1. Install **Node.js LTS**: https://nodejs.org/ (includes npm)
2. Restart PowerShell
3. Verify: `node -v` and `npm -v`
4. Run:
   ```powershell
   cd lobo-ops
   npm install
   npm run init-db
   npm start
   ```
5. Open http://localhost:3847

Combine with Option B env vars for auto-send from the app UI.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `'npm' is not recognized` | Node not installed — use **Option A** (PowerShell) or install Node |
| `ERR_CONNECTION_REFUSED` on localhost:3847 | Server not running on your PC — use Option A or install Node |
| Outlook COM error | Open Outlook first; ensure desktop app (not web-only) |
| Graph 403 Forbidden | IT must grant admin consent for `Mail.Send` |
| Images don't show in email | Recipients need internet; images hosted on GitHub |

---

## Email templates included

| Template | Trigger |
|----------|---------|
| **Onboarding welcome** | New candidate added / manual send |
| **Creating Legends reminder** | `-ClReminder` flag or app button |

Both match your existing `✅ You're Almost Ready!` email content and Smartsheet/Brainshark links.
