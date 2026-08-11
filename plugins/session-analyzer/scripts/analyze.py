#!/usr/bin/env python3
"""Session analyzer - walks ~/.claude/projects, reports usage patterns."""
import json, os, re, glob, sys
from collections import Counter, defaultdict

ROOT = os.path.expanduser("~/.claude/projects")
if not os.path.isdir(ROOT):
    print(f"ERROR: {ROOT} not found. Are you using Claude Code?")
    sys.exit(1)

sessions = glob.glob(f"{ROOT}/**/*.jsonl", recursive=True)
tool_calls = Counter()
project_msg = Counter()
bash_cmds = Counter()
file_dirs = Counter()

def project_from_cwd(cwd):
    if not cwd: return 'unknown'
    cwd = cwd.replace(os.path.expanduser('~/'), '')
    cwd = re.sub(r'/\.claude/worktrees/.*$', '', cwd)
    parts = cwd.split('/')
    if parts[0] == 'Projects' and len(parts) >= 2: return parts[1]
    return parts[0] if parts else 'unknown'

for fp in sessions:
    try:
        with open(fp) as f:
            cwd = None
            for line in f:
                try: d = json.loads(line)
                except: continue
                if cwd is None: cwd = d.get('cwd')
                project = project_from_cwd(cwd or d.get('cwd'))
                msg = d.get('message', {})
                if not isinstance(msg, dict): continue
                content = msg.get('content')
                if d.get('type') == 'user' and isinstance(content, str):
                    if not content.startswith('[{') and '<tool_use_id>' not in content:
                        project_msg[project] += 1
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get('type') == 'tool_use':
                            tool_calls[c.get('name','')] += 1
                            if c.get('name') == 'Bash':
                                cmd = (c.get('input',{}) or {}).get('command','').strip()
                                if cmd: bash_cmds[cmd.split()[0] if cmd.split() else ''] += 1
                            if c.get('name') in ('Edit','Write','Read'):
                                p = (c.get('input',{}) or {}).get('file_path','')
                                if p:
                                    parts = p.replace(os.path.expanduser('~/'),'').split('/')
                                    file_dirs['/'.join(parts[:2])] += 1
    except: pass

print(f"# Session Analysis\n")
print(f"Sessions: {len(sessions)}  |  Total tool calls: {sum(tool_calls.values())}\n")
print("## Top projects (by user messages)\n")
for p,n in project_msg.most_common(10):
    print(f"- **{p}**: {n}")
print("\n## Top tools\n")
for t,n in tool_calls.most_common(12):
    print(f"- {t}: {n}")
print("\n## Top bash commands\n")
for c,n in bash_cmds.most_common(10):
    print(f"- {c}: {n}")
print("\n## Top directories touched\n")
for d,n in file_dirs.most_common(10):
    print(f"- {d}: {n}")
