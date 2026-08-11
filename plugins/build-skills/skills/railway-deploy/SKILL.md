---
name: railway-deploy
description: Deploy, configure, and debug Railway.app services. Use whenever Louis mentions Railway, custom domains with Railway, _railway-verify TXT records, _acme-challenge SSL, Railway volumes, Postgres on Railway, Railway scheduled jobs, Railway environment variables, or debugging Railway deployment errors (401, 500, DNS issues, "waiting for DNS update"). Also use proactively when deploying a Next.js, FastAPI, or Node project that Louis has previously deployed to Railway.
---

# Railway Deploy Skill

Encodes the deploy + debug workflow Louis has re-solved across wedding-planner, Contact Manager, and Recipe Website.

## Canonical config file

Every Louis project gets a `railway.toml` at repo root:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "<project-specific>"
healthcheckPath = "/api/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

Add a `/api/health` endpoint returning `{ok: true, db_connected: <bool>}` to every service. Louis checks this constantly during debug.

## Custom domain setup — order of operations

Railway uses TWO DNS records for custom domains. Missing either causes the "waiting for DNS update" state indefinitely.

1. **CNAME** — `<subdomain>` → `<railway-provided-target>.up.railway.app`
2. **TXT** at `_railway-verify.<subdomain>` — value is unique per domain, shown in Railway dashboard

Only after BOTH propagate (check with `dig TXT _railway-verify.example.com +short`) will Railway issue the Let's Encrypt cert via `_acme-challenge` — that third record is managed by Railway automatically, don't try to add it manually.

Propagation is usually 5–15 minutes. If >30 minutes, delete the domain in Railway and re-add.

## Postgres service wiring

When replacing SQLite with Postgres:
1. Add Postgres plugin in Railway dashboard.
2. Reference the connection string as `${{Postgres.DATABASE_URL}}` in the service's variables (NOT a copy-paste of the URL — reference syntax auto-updates).
3. In the app, use `DATABASE_URL` env var; if absent, fall back to SQLite for local dev.
4. On first deploy after wiring, run migrations explicitly — Railway does not auto-run them.

## Volumes

Volumes are mounted per-service at a path you pick (e.g. `/data`). Set in Railway dashboard under Service → Settings → Volumes, NOT in `railway.toml`. If Louis says "I can't find volume," direct him to Service settings, not the project-level settings page.

## Scheduled jobs

Three options, use in this priority:
1. **Claude Code scheduled tasks** (`~/.claude/scheduled-tasks/`) — for agent-driven work. Minimum interval 1 hour, cron in UTC.
2. **Railway cron service** — for simple periodic scripts. Create a separate service with `cron` restart policy.
3. **APScheduler inside the main service** — only if job must share process memory. Set `ENABLE_SCHEDULER=true` env var and check logs for "APScheduler background thread started."

## Common failure modes (ranked by frequency from Louis's sessions)

| Symptom | Root cause | Fix |
|---|---|---|
| "waiting for DNS update" >30min | TXT record missing or CNAME pointed wrong | Verify both records with `dig` |
| 500 on first request after deploy | Missing env var | Check Service → Variables; referenced secrets need `${{...}}` syntax |
| 401 on inbound webhook | Basic Auth middleware matched the webhook path | Exclude webhook path from auth middleware |
| "two services not connected" | Reference variable pointing to wrong service | Re-pick from dropdown in Variables panel |
| Data not persisting across devices | Still on SQLite, or DB volume not mounted | Move to Postgres plugin |
| Logs show errors but app seems fine | Old deploy cached | Force redeploy from dashboard |

## Auth middleware exclusion pattern

Louis uses Basic Auth on most Railway services. Inbound webhooks (Resend, Gmail push, etc.) must be excluded:

```python
# FastAPI example
EXCLUDED = {"/api/health", "/api/webhooks/resend", "/api/webhooks/gmail"}

@app.middleware("http")
async def basic_auth(request, call_next):
    if request.url.path in EXCLUDED:
        return await call_next(request)
    # ... auth check
```

## Debug workflow

When Louis reports a Railway issue, ALWAYS:
1. Ask for or check the Railway logs tail (last 50 lines).
2. Check `/api/health` response.
3. List expected env vars vs. what's set.
4. Confirm DNS state with `dig`.
5. Only THEN propose code changes.

Do not propose speculative fixes before checking logs.
