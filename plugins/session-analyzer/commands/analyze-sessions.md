---
description: Scrape ~/.claude/projects and return a usage pattern breakdown (tools, projects, intents, candidate skills)
---

Run `${CLAUDE_PLUGIN_ROOT}/scripts/analyze.py` and return its stdout formatted as a markdown report.

If the script fails, report the error and suggest running `python3 --version` to verify Python 3.9+ is available.

After the report prints, ask Louis if he wants to:
1. Generate draft SKILL.md files for the top candidate skills
2. Filter to a specific project
3. Do nothing (just show the report)
