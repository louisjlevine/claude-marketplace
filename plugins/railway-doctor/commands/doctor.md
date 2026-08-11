---
description: Run full health check on a Railway-deployed service. Requires a URL and optionally a Railway project name.
argument-hint: <service-url> [project-name]
---

Run `${CLAUDE_PLUGIN_ROOT}/scripts/doctor.sh "$1" "$2"` and interpret the output.

The script checks:
1. DNS: CNAME + `_railway-verify` TXT record propagation
2. SSL: cert validity and issuer
3. HTTP: `/api/health` response (expects `{ok: true, db_connected: true}`)
4. Railway CLI: project link status and recent logs tail

After the report prints, summarize: what's healthy, what's broken, what Louis should check next. Reference the `railway-deploy` skill for fix procedures.
