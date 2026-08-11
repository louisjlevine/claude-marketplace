---
name: nextjs-full-stack-bootstrap
description: Scaffold a new Next.js 14+ full-stack app in Louis's canonical pattern — Tailwind frontend, Zustand state, Postgres persistence, Basic Auth, Railway-ready deploy config. Use when starting a new project from scratch or when Louis says "new app," "new site," "start a project," or references wedding-planner, Recipe Website, or Contact Manager as a template. Pairs with the website-design skill for styling and the railway-deploy skill for deploy.
---

# Next.js Full-Stack Bootstrap

Standardized scaffold derived from wedding-planner and Recipe Website.

## Build sequence (strict order)

Louis has learned to enforce this order. Deviating causes rework.

1. **`lib/types.ts`** — All domain types FIRST. Every other file imports from here.
2. **`lib/plan-store.ts`** (or equivalent Zustand store) — State shape, actions, persistence adapter.
3. **`lib/db.ts`** — Postgres client + migration runner. SQLite fallback for local.
4. **`lib/auth.ts`** — Basic Auth middleware + session helpers.
5. **`app/api/health/route.ts`** — Health endpoint returning DB connectivity.
6. **`app/api/<resource>/route.ts`** — API routes, one per resource.
7. **`components/sections/<Section>.tsx`** — UI sections. APPLY the `website-design` skill here, do not freestyle styling.
8. **`app/page.tsx`** — Compose sections.
9. **`railway.toml`** + `.env.example` — Deploy config. See `railway-deploy` skill.

## Directory structure

```
project/
├── CLAUDE.md                    # project-specific overrides
├── .env.example                 # all env vars, no values
├── railway.toml                 # deploy config
├── next.config.js
├── tailwind.config.ts
├── app/
│   ├── api/
│   │   ├── health/route.ts
│   │   └── <resource>/route.ts
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/                      # primitives (Button, Input, Card)
│   └── sections/                # page sections
├── lib/
│   ├── types.ts                 # all shared types
│   ├── plan-store.ts            # Zustand store
│   ├── db.ts                    # Postgres + migrations
│   └── auth.ts                  # Basic Auth middleware
└── public/
```

## SQLite → Postgres migration

Louis always starts on SQLite for local speed, then moves to Postgres when cross-device sync matters. When the conversation hits "data is not persisting across devices":

1. Add Postgres via Railway (see `railway-deploy` skill).
2. Create `lib/db.ts` that prefers `DATABASE_URL`, falls back to SQLite.
3. Write a one-shot migration script in `scripts/migrate-to-postgres.ts` that reads SQLite, writes Postgres, and is safe to re-run.
4. Set `DATABASE_URL` in Railway via `${{Postgres.DATABASE_URL}}`.
5. Deploy, run migration once, verify with `/api/health` showing `db_connected: true, row_count: >0`.

## Styling directive

Always invoke the `website-design` skill for any component work. Never write styles freestyle.

## Testing pattern (from wedding-planner)

If the project uses Vitest with the Anthropic SDK, always use class-based mocks — arrow functions can't be `new`-ed:

```typescript
vi.mock("@anthropic-ai/sdk", () => {
  class MockAnthropic {
    messages = { create: vi.fn().mockResolvedValue({ content: [{ type: "text", text: "..." }] }) };
  }
  return { default: MockAnthropic };
});
```

For per-test control, use `vi.hoisted()` with a `mockCreate` ref.
