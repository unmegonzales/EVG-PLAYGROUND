# Levy Banquets — Reserve email signature

Paste-ready HTML for **Reserve by Infor** electronic signatures, styled for Levy banquet event correspondence.

## Files

| File | Use |
| --- | --- |
| `paste-into-reserve.html` | Copy this markup into the signature HTML source editor |
| `preview.html` | Open in a browser to review the design in a mock email |

## Design

- Forest green left rail aligned with Levy branding in Reserve
- Clear name → title → **Levy Banquets** hierarchy
- Contact row + plan-an-event CTA
- Table-based, inline CSS for Outlook / Gmail / Reserve compatibility
- No hosted images required (survives restricted email clients)

## Customize

Edit these strings in `paste-into-reserve.html` before pasting:

- Name / title / department
- Phone (`tel:`) and email (`mailto:`)
- Venue line under the Levy wordmark (optional)

## Install in Reserve

1. Settings → Edit User → Email Signature  
2. HTML tab → Source (`<>`)  
3. Paste `paste-into-reserve.html`  
4. Enable **Include Signature in New Emails** → Save  
