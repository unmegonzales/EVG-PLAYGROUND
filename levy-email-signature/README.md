# Levy at UNM — Reserve email signature

Paste-ready HTML for **Reserve by Infor**, matched to Evan E. Gonzales’s Levy signature.

## Cognito / save error

Reserve sits behind AWS Cognito + WAF. Pasting modern HTML (`style=...`, comments, rich CSS) often gets blocked as XSS and surfaces as a **Cognito** error.

Use the **safe** markup below (classic `<font>` / `bgcolor`, no CSS comments).

## Files

| File | Use |
| --- | --- |
| `paste-into-reserve.html` | **Try this first** — logo + contact + notices |
| `paste-into-reserve-no-image.html` | If Cognito still errors — text only, then insert logo with the Image toolbar button |
| `preview.html` | Browser preview |

## Install in Reserve

1. Settings → Edit User → Email Signature → **HTML** tab  
2. Open source (`<>`)  
3. Delete any existing content  
4. Paste **only** the contents of `paste-into-reserve.html` (no markdown fences)  
5. Save with **Include Signature in New Emails** checked  

### If Cognito still appears

1. Refresh / re-login (expired token can also show as Cognito)  
2. Paste `paste-into-reserve-no-image.html` instead  
3. In Design/HTML view, use **Insert Image** and point to:  
   `https://unmegonzales.github.io/ZERO-Communications/email/assets/Levy-Logo.png`  
4. Set image width to about **110px**

## Links

- Non-Profit Groups: https://new.express.adobe.com/webpage/m2nlJXIvP4xV8  
- Careers: Compass Group careers (Albuquerque / Levy)  
- GoLobos.com: https://golobos.com/  
