# Copilot Autonomous Operating Instructions

**Effective:** 2026-01-04
**Owner:** President

---

## Authorization

GitHub Copilot (including Copilot Workspace and Copilot Chat) is authorized to operate on all repositories owned by:
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
| Generate code completions | All repos |
| Suggest refactorings | All repos |
| Create branches | `agent/copilot/<issue>-<slug>` format |
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

### Requires Human Review (Create PR Instead)

| Action | Reason |
|--------|--------|
| Delete files | Destructive |
| Rename repos | Organizational change |
| Transfer repos | Ownership change |
| Modify production secrets | Security |
| Change database schemas | Data integrity |
| Modify auth/permissions | Security |
| Merge to `main` | Requires approval |

---

## Copilot Workspace Tasks

When using Copilot Workspace for multi-file changes:

1. **Task Specification:** Accept issue-driven tasks
2. **Plan Review:** Generate implementation plan
3. **Implementation:** Execute changes across files
4. **Validation:** Run tests and linters
5. **PR Creation:** Open PR with `Closes #<issue>`

### Workspace Session Rules

- Keep sessions focused on single issues
- Do not chain multiple unrelated changes
- Preserve existing code style
- Update registers when behavior changes

---

## Copilot Chat Guidelines

When responding to chat queries:

1. **Context First:** Read relevant files before suggesting changes
2. **Minimal Changes:** Suggest smallest effective modification
3. **Explain Reasoning:** Provide rationale for suggestions
4. **Reference Governance:** Point to relevant canon docs when applicable

### Chat Commands

| Command | Action |
|---------|--------|
| `/explain` | Explain selected code |
| `/fix` | Suggest bug fixes |
| `/tests` | Generate test cases |
| `/docs` | Generate documentation |

---

## Commit Message Format

```
<type>: <description>

<body if needed>

Closes #<issue> (if applicable)

Co-Authored-By: GitHub Copilot <noreply@github.com>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`

---

## Branch Naming

```
agent/copilot/<issue-number>-<short-slug>
```

Examples:
- `agent/copilot/42-add-login`
- `agent/copilot/99-fix-dashboard-crash`

---

## Size Limits

- **<= 400 lines:** Commit directly
- **> 400 lines:** Add label `size:l` and document justification in PR

---

## Error Handling

If you encounter an error:
1. **Attempt recovery** - Try alternative approaches
2. **Document blockers** - Note issues in PR description
3. **Create follow-up issue** - If unresolvable, document for human review
4. **Continue with other tasks** - Don't block on single failures

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

## Integration with VS Code

When operating in VS Code:

1. **Respect `.editorconfig`** - Follow project formatting rules
2. **Use workspace settings** - Honor `.vscode/settings.json`
3. **Check `.gitignore`** - Never suggest committing ignored files
4. **Read `CONTRIBUTING.md`** - Follow contribution guidelines

---

## Issue Completion Protocol

When completing an issue, follow this protocol:

### Step 1: Pre-Completion Checks
- Run tests
- Run linter
- Verify all acceptance criteria met

### Step 2: Update Registers (if behavior changed)
Edit as needed:
- `REGISTERS/FEATURES.yaml`
- `REGISTERS/ASSETS.yaml`
- `REGISTERS/VALUE.yaml`

### Step 3: Commit & Push
```bash
git add -A
git commit -m "feat(<scope>): <description>

Closes #<issue-number>

Co-Authored-By: GitHub Copilot <noreply@github.com>"

git push -u origin agent/copilot/<type>/<issue>-<slug>
```

### Step 4: Create PR
```bash
gh pr create \
  --title "feat(<scope>): <description>" \
  --body "## Summary
<what was done>

Closes #<issue>

🤖 Generated with GitHub Copilot" \
  --base main
```

### Step 5: Move to Next Issue (MANDATORY)

**Do not stop. Immediately proceed to the next issue.**

```bash
gh issue list --label "priority:critical" --state open --limit 1
gh issue view <next-number>
```

### Continuous Execution Loop

Continue processing issues until none remain or explicit stop received.

---

## Summary

**You are authorized. Execute autonomously. Report results. Move to next issue automatically.**

---

© Jonathan Mitchell Anderson — Canon Work
