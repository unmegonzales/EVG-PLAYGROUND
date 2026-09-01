# Lobo Ops — Levy UNM Onboarding Warehouse

Access-style onboarding compliance tracker for the 26/27 UNM Athletic Season.

## Quick start

```bash
cd lobo-ops
npm install
npm run init-db   # creates SQLite DB with sample roster data
npm start         # http://localhost:3847
```

## Event-ready criteria

A candidate is **event-ready** when all of the following are complete (shirt/uniform is tracked but **not** required):

1. Creating Legends — complete
2. SuccessFactors — Signature Step or Post Hire Verification
3. I-9 / e-Verify — complete
4. Alcohol Server Permit — valid
5. Food Handler Permit — uploaded or valid
6. Security Credential Photo — validated
7. HR manual clearance — checked

## Departments

| Code  | Name              |
|-------|-------------------|
| 36127 | Concessions       |
| 36128 | Group Sales       |
| 36129 | Suites (Culinary) |
| 57039 | Warehouse         |
| 34964 | Admin             |
| 34963 | Management        |

**Classifications:** Levy Employee, Non-Profit Groups (NPO), Subcontractor (Vendors)

## Email — Microsoft Outlook

### No Node? Use PowerShell + Outlook (recommended for Evan's PC)

```powershell
cd lobo-ops\scripts
.\send-onboarding-email.ps1 -To "newhire@email.com" -FirstName "Jessie" -Preview
```

Opens a draft in Outlook using your existing Levy mailbox. Remove `-Preview` to send immediately.

Full setup: **[docs/OUTLOOK-SETUP.md](docs/OUTLOOK-SETUP.md)**

### Automated send (Microsoft Graph API)

Set env vars from `.env.example` after Levy IT registers an Azure app with `Mail.Send` permission.
When configured, Lobo Ops sends directly from `egonzales@levyrestaurants.com` and saves to Sent Items.

## Environment

| Variable | Default | Description        |
|----------|---------|--------------------|
| `PORT`   | `3847`  | Server port        |
