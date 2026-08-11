# louis-local

Personal Claude Code marketplace. One repo for review agents, project bootstrap skills, and workflow commands — install once per machine, use in any session, no folder paths to remember.

## Install

```bash
# in Claude Code
/plugin marketplace add louisjlevine/claude-marketplace
/plugin install dev-agents@louis-local
/plugin install build-skills@louis-local
```

Install only what a given machine needs. Each plugin versions independently.

## Plugins

| Plugin | Provides | Contents |
|---|---|---|
| `dev-agents` | 10 subagents | Plan-phase: `cto`, `system-analyst`, `ux-designer`. Post-build: `backend-qa`, `frontend-qa`, `security-reviewer`, `spaghetti`. Workflow: `deployment-verifier`, `feedback-to-linear`, `ui-polish-reviewer` |
| `build-skills` | 3 skills | `nextjs-full-stack-bootstrap`, `railway-deploy`, `swift-healthkit` |
| `session-analyzer` | `/session-analyzer:analyze-sessions` | Usage pattern breakdown across sessions |
| `railway-doctor` | `/railway-doctor:doctor <url>` | Railway health diagnosis — DNS, SSL, env, DB |
| `linear-triage-runner` | `/linear-triage-runner:next-ticket` | Pull and start the top-priority Linear ticket |

## Agents

Invoke by name — no wizard, no config:

```
use the security-reviewer agent on my last commit
```

**Model assignment.** Agents are split by the kind of thinking they do. Judgment, ambiguity, and adversarial reasoning run on Opus; well-specified checklist execution runs on Fable.

| Opus 5 | Fable 5 |
|---|---|
| `cto`, `system-analyst`, `security-reviewer`, `ux-designer` | `backend-qa`, `frontend-qa`, `spaghetti`, `deployment-verifier`, `feedback-to-linear`, `ui-polish-reviewer` |

**Design conventions.** Every agent shares an execution contract:

- Ordered steps, no silent skipping
- Every finding cites `file:line` — unlocatable findings are dropped, not reported
- A mandatory **"Not checked"** section, so a skipped step can never read as a pass
- An explicit tool-call budget
- Reviewers never apply fixes

Agents discover project context adaptively — `CLAUDE.md` first, then `docs/project/` if present, then `package.json` or the ecosystem equivalent. They never guess a test command.

## Auto-update

Enable via `/plugin` → Marketplaces → `louis-local` → Auto-update, or in `settings.json`:

```json
{
  "extraKnownMarketplaces": [
    { "url": "https://github.com/louisjlevine/claude-marketplace", "autoUpdate": true }
  ]
}
```

Run `/reload-plugins` after an update — no restart needed.

## Adding a plugin

1. `mkdir -p plugins/<name>/.claude-plugin`
2. Write `plugins/<name>/.claude-plugin/plugin.json` with `name`, `version`, `description`, `author`
3. Add `agents/`, `skills/`, `commands/`, or `hooks/` as needed
4. Register it in the `plugins` array of `.claude-plugin/marketplace.json`
5. Commit and push — installed machines pick it up on next update

## Scope

Generic tooling only. Anything carrying client intel, personal voice, or runtime state stays out of this repo by design — this is public.
