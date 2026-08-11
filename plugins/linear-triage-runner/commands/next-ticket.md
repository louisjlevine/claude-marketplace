---
description: Fetch the highest-priority open Linear ticket for the current project and begin work on it. Requires Linear MCP to be connected.
---

1. Detect the current project from `pwd` and map it to a Linear team/project name.
   - `wedding-planner` → Wedding Planner team
   - `Contact Manaager` → Contact Manager team
   - `yoga-tracker` → YogaBiometrics team
   - `Recipe Website` → Recipe Website team
2. Call Linear's `list_issues` filtered to:
   - state: not Done, not Canceled, not In Review
   - sorted by priority descending, then updated_at descending
   - limit 1
3. If no ticket found: report "No open tickets — nothing to triage" and stop.
4. If a ticket found:
   - Read the ticket body.
   - Summarize: title, priority, acceptance criteria.
   - Ask Louis: "Start work on [PROJ-123] <title>? (yes / skip / pick-another)"
5. On "yes": create branch `fix/proj-123-<kebab-title>`, read relevant files, propose a plan.
6. On "skip": lower the ticket's priority one level (rotation) and fetch next.
7. On "pick-another": show top 5 by priority, let Louis pick.

Rule: NEVER close, delete, or move a ticket to Done. Only Louis marks tickets Done.
