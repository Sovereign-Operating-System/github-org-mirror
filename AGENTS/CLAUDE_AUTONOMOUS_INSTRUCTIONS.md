# Claude Autonomous Operating Instructions

**Effective:** 2026-01-04
**Owner:** President

---

## Authorization

Claude (including Claude Code CLI and Claude API integrations) is authorized to operate on all repositories owned by:
- `PresidentAnderson` (personal)
- `WisdomOS-Platform` (organization)
- `LexChronos-Legal` (organization)
- `King-Legend-Inc` (organization)
- `Sovereign-Operating-System` (organization)

**Execute tasks directly.** Do not ask for permission when operating within scope.

---

## Autonomous Actions (Pre-Approved)

### Always Allowed (No Confirmation Needed)

| Action | Scope |
|--------|-------|
| Read any file | All repos |
| Edit files | All repos |
| Create files | All repos |
| Run terminal commands | All repos |
| Create branches | `agent/claude/<issue>-<slug>` format |
| Commit to agent branches | All repos |
| Push to agent branches | All repos |
| Create/update issues | All repos |
| Create pull requests | All repos |
| Run tests | All repos |
| Run linters | All repos |
| Install dependencies | All repos |
| Create folders | `AGENTS/`, `LEGAL/`, `REGISTERS/`, `.github/` |
| Copy governance files | From sovereign-canon templates |
| Update YAML registers | `REGISTERS/*.yaml` |
| Search codebase | All repos |
| Multi-file refactoring | All repos |
| Web search for documentation | All repos |
| Fetch URLs for context | All repos |

### Requires Human Review (Create PR Instead)

| Action | Reason |
|--------|--------|
| Delete critical files | Destructive |
| Rename repos | Organizational change |
| Transfer repos | Ownership change |
| Modify production secrets | Security |
| Change database schemas | Data integrity |
| Modify auth/permissions | Security |
| Force push | Destructive |
| Merge to `main` | Requires approval |

---

## Claude Code CLI Mode

When operating via Claude Code CLI:

### Standard Task Flow

1. **Understand:** Read issue/request, explore codebase
2. **Plan:** Use TodoWrite for complex multi-step tasks
3. **Implement:** Make changes, use Edit tool for modifications
4. **Verify:** Run tests via Bash, check for errors
5. **Register:** Update REGISTERS if behavior changed
6. **Commit:** Create commit with clear message
7. **PR:** Open pull request referencing issue

### Agentic Behavior Rules

- **Be proactive** - Execute within scope, don't ask permission
- **Be thorough** - Use Glob/Grep to search before assuming
- **Be minimal** - Smallest change that solves the problem
- **Be safe** - Never commit secrets, never force push
- **Track progress** - Use TodoWrite for multi-step tasks

---

## Tool Usage Guidelines

### File Operations
- Use `Read` for reading files (not `cat`)
- Use `Edit` for modifications (not `sed`)
- Use `Write` for new files (not `echo >`)
- Use `Glob` for finding files (not `find`)
- Use `Grep` for searching content (not `grep`)

### Terminal Operations
- Use `Bash` for git, npm, docker, test runners
- Chain related commands with `&&`
- Use background execution for long-running tasks

### Research
- Use `WebSearch` for documentation lookups
- Use `WebFetch` to read specific URLs
- Use `Task` with Explore agent for codebase exploration

---

## Commit Message Format

```
<type>: <description>

<body if needed>

Closes #<issue> (if applicable)

Co-Authored-By: Claude <noreply@anthropic.com>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`

---

## Branch Naming

```
agent/claude/<issue-number>-<short-slug>
```

Examples:
- `agent/claude/42-add-login`
- `agent/claude/99-fix-dashboard-crash`

---

## Size Limits

- **<= 400 lines:** Commit directly
- **> 400 lines:** Add label `size:l` and document justification in PR

---

## Error Handling

If you encounter an error:
1. **Try to fix it** - Don't stop and ask
2. **Try alternative approaches** - Multiple solutions exist
3. **Document blockers** - Note in PR if unresolvable
4. **Create follow-up issue** - For future resolution
5. **Continue with other tasks** - Don't block entirely

---

## Reference Repos

When you need templates or examples, use **sovereign-canon** as the canonical source:

**Option 1: GitHub (preferred for remote operations)**
```
gh repo clone Sovereign-Operating-System/sovereign-canon /tmp/sovereign-canon
```

**Option 2: Environment variable (for local setups)**
```bash
export SOS_CANON_ROOT="$HOME/Projects/orgs/Sovereign-Operating-System/sovereign-canon"
```

**Template locations within sovereign-canon:**
```
sovereign-canon/
├── AGENTS/AGENT_INIT_CONTRACT.md
├── LEGAL/IP_CANON.md
├── REGISTERS/*.yaml
├── pack/root/                          # Root-level templates
├── pack/github/                        # .github/ templates
│   ├── pull_request_template.md
│   ├── ISSUE_TEMPLATE/*.md
│   └── workflows/*.yml
└── pack/scripts/                       # Automation scripts
```

**Raw file access (for direct fetch):**
```
https://raw.githubusercontent.com/Sovereign-Operating-System/sovereign-canon/master/
```

---

## MCP Server Integration

When MCP servers are available:
- Use provided tools over built-in equivalents when appropriate
- Respect tool-specific rate limits
- Cache results where applicable

---

## Communication Style

- **Do not ask:** "Should I proceed?" — Just proceed
- **Do not ask:** "Is this okay?" — Follow these instructions
- **Do not ask:** "Do you want me to...?" — If in scope, do it
- **Do report:** What you did, in commits and PRs
- **Be concise:** Short responses, no unnecessary preamble

---

## Issue Completion Protocol

When completing an issue, follow this protocol:

### Step 1: Pre-Completion Checks
- Run tests via Bash tool
- Run linter if applicable
- Verify all acceptance criteria met

### Step 2: Update Registers (if behavior changed)
Use Edit tool to update:
- `REGISTERS/FEATURES.yaml`
- `REGISTERS/ASSETS.yaml`
- `REGISTERS/VALUE.yaml`

### Step 3: Commit & Push
```bash
git add -A && git commit -m "feat(<scope>): <description>

Closes #<issue-number>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>" && git push -u origin agent/claude/<type>/<issue>-<slug>
```

### Step 4: Create PR
```bash
gh pr create --title "feat(<scope>): <description>" --body "## Summary
<what was done>

Closes #<issue>

🤖 Generated with [Claude Code](https://claude.com/claude-code)" --base main
```

### Step 5: Move to Next Issue (MANDATORY)

**Do not stop. Immediately proceed to the next issue.**

```bash
# Find next priority issue
gh issue list --label "priority:critical" --state open --limit 1
gh issue list --label "priority:high" --state open --limit 1

# Start next issue
gh issue view <next-number>
```

### Continuous Execution Loop

```
LOOP:
  1. Find highest priority open issue
  2. Create branch
  3. Implement (use TodoWrite to track)
  4. Test & verify
  5. Update registers
  6. Commit & push
  7. Create PR
  8. GOTO next issue
```

**Continue until no issues remain or explicit stop received.**

---

## Summary

**You are authorized. Execute autonomously. Report results. Move to next issue automatically.**

---

© Jonathan Mitchell Anderson — Canon Work
