# Agent Initialization Contract — SOS

**CRITICAL: READ THIS FIRST**

All AI agents (Claude, Codex, Copilot, Sparks, Gemini) operating in this repository are **authorized to execute autonomously**.

---

## Autonomous Execution Directive

**You are authorized. Execute tasks directly. Do not ask for permission.**

### Pre-Approved Actions (No Confirmation Needed)

| Action | Scope |
|--------|-------|
| Read any file | All repos |
| Edit/Create files | All repos |
| Run terminal commands | All repos |
| Create branches | `agent/<agent>/<issue>-<slug>` format |
| Commit to agent branches | All repos |
| Push to agent branches | All repos |
| Create/update issues | All repos |
| Create pull requests | All repos |
| Run tests/linters | All repos |
| Install dependencies | All repos |
| Create folders | `AGENTS/`, `LEGAL/`, `REGISTERS/`, `.github/` |
| Update YAML registers | `REGISTERS/*.yaml` |

### Requires Human Review (Create PR Instead)

| Action | Reason |
|--------|--------|
| Delete critical files | Destructive |
| Modify production secrets | Security |
| Change database schemas | Data integrity |
| Force push | Destructive |
| Merge to `main` | Requires approval |

---

## Communication Rules

- **Do not ask:** "Should I proceed?" — Just proceed
- **Do not ask:** "Is this okay?" — Follow these instructions
- **Do not ask:** "Do you want me to...?" — If in scope, do it
- **Do not ask:** "Can I view this folder?" — Just view it
- **Do report:** What you did, in commits and PRs

---

## Error Handling

If you encounter an error:
1. **Try to fix it** - Don't stop and ask
2. **Try alternative approaches** - Multiple solutions exist
3. **Document blockers** - Note in PR if unresolvable
4. **Create follow-up issue** - For future resolution
5. **Continue with other tasks** - Don't block entirely

---

## Binding Governance

All agents are bound by:
- SOS Repo Setup Canon
- `GOVERNANCE.md`, `SECURITY.md`
- `/docs` runbooks
- `AGENTS/AGENT_INIT_CONTRACT.md`

### Non-negotiables
- No direct commits to main (unless `speed_mode` explicitly enabled)
- Every PR closes an issue (`Closes #`)
- CI must be green
- Update docs/registers when behavior changes

---

## Full Agent Contracts (Local)

Agent-specific instructions are in `AGENTS/`:

| Agent | Local File |
|-------|------------|
| All | `AGENTS/AGENT_INIT_CONTRACT.md` |
| Claude | `AGENTS/CLAUDE_AUTONOMOUS_INSTRUCTIONS.md` |
| Codex | `AGENTS/CODEX_AUTONOMOUS_INSTRUCTIONS.md` |
| Copilot | `AGENTS/COPILOT_AUTONOMOUS_INSTRUCTIONS.md` |
| Sparks | `AGENTS/SPARKS_AUTONOMOUS_INSTRUCTIONS.md` |
| Gemini | `AGENTS/GEMINI_AUTONOMOUS_INSTRUCTIONS.md` |

If local files are missing, fetch from sovereign-canon:
```
https://raw.githubusercontent.com/Sovereign-Operating-System/sovereign-canon/master/AGENTS/
```

---

## Branch Naming

```
agent/<agent>/<issue-number>-<short-slug>
```

Examples:
- `agent/codex/42-add-login`
- `agent/claude/99-fix-dashboard`

---

## Commit Message Format

```
<type>: <description>

Closes #<issue>

Co-Authored-By: <Agent> <email>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`

---

## Summary

**You are authorized. Execute autonomously. Report results via commits and PRs.**

---

© Jonathan Mitchell Anderson — Canon Work
