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

## Email automation

Onboarding emails are generated from your template and logged. Connect Microsoft 365 (Graph API) in a future release for automatic send; until then use the preview to copy/send via Outlook.

## Environment

| Variable | Default | Description        |
|----------|---------|--------------------|
| `PORT`   | `3847`  | Server port        |
