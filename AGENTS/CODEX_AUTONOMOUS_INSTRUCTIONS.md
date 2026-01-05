# Codex Autonomous Operating Instructions

**Effective:** 2026-01-04
**Owner:** President

---

## Authorization

Codex is authorized to operate autonomously on all repositories owned by:
- `PresidentAnderson` (personal)
- `WisdomOS-Platform` (organization)
- `LexChronos-Legal` (organization)
- `King-Legend-Inc` (organization)
- `Sovereign-Operating-System` (organization)

**Do not ask for permission.** Execute tasks directly.

---

## Autonomous Actions (Pre-Approved)

### Always Allowed (No Confirmation Needed)

| Action | Scope |
|--------|-------|
| Read any file | All repos |
| Create branches | `agent/codex/<issue>-<slug>` format |
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
| Update templates | `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/*` |
| Add CI workflows | `.github/workflows/` |
| Commit directly to `main` | For governance/infrastructure rollouts only |

### Requires Human Review (Create PR Instead)

| Action | Reason |
|--------|--------|
| Delete files | Destructive |
| Rename repos | Organizational change |
| Transfer repos | Ownership change |
| Modify production secrets | Security |
| Change database schemas | Data integrity |
| Modify auth/permissions | Security |

---

## Standard Tasks

### 1. Repo Docs Pack Rollout

Execute without asking:

```bash
# 1. Create structure
mkdir -p AGENTS LEGAL REGISTERS

# 2. Copy from reference repo (goals-tracking-system or sovereign-canon)
cp <ref>/AGENTS/AGENT_INIT_CONTRACT.md AGENTS/
cp <ref>/LEGAL/IP_CANON.md LEGAL/
cp <ref>/.github/pull_request_template.md .github/
cp <ref>/.github/ISSUE_TEMPLATE/*.md .github/ISSUE_TEMPLATE/
cp <ref>/.github/workflows/agent-branch-guard.yml .github/workflows/

# 3. Create REGISTERS (customize by reading README and src/)
# - REGISTERS/FEATURES.yaml
# - REGISTERS/ASSETS.yaml
# - REGISTERS/VALUE.yaml

# 4. Commit and push
git add -A
git commit -m "chore: roll out Sovereign Canon Repo Docs Pack v1.0"
git push
```

### 2. Feature Implementation

1. Create branch: `agent/codex/<issue>-<slug>`
2. Implement feature
3. Update REGISTERS if applicable
4. Commit with `Closes #<issue>`
5. Push and create PR
6. **Do not wait for approval to start**

### 3. Bug Fixes

1. Create branch: `agent/codex/<issue>-<slug>`
2. Fix bug
3. Add/update tests
4. Commit with `Closes #<issue>`
5. Push and create PR

---

## Commit Message Format

```
<type>: <description>

<body if needed>

Closes #<issue> (if applicable)

Co-Authored-By: Codex <noreply@github.com>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`

---

## Branch Naming

```
agent/codex/<issue-number>-<short-slug>
```

Examples:
- `agent/codex/42-add-login`
- `agent/codex/99-fix-dashboard-crash`

---

## Size Limits

- **<= 400 lines:** Commit directly
- **> 400 lines:** Add label `size:l` and document justification in PR

---

## Error Handling

If you encounter an error:
1. **Do not stop and ask.** Try to fix it.
2. If unfixable, create an issue describing the problem
3. Continue with other tasks
4. Document blockers in the PR description

---

## Communication

- **Do not ask:** "Should I proceed?" — Just proceed.
- **Do not ask:** "Is this okay?" — Follow these instructions.
- **Do not ask:** "Do you want me to...?" — If it's in scope, do it.
- **Do report:** What you did, in commit messages and PR descriptions.

---

## Reference Repos

When you need templates or examples, use **sovereign-canon** as the canonical source:

**Option 1: GitHub (preferred for remote operations)**
```
gh repo clone Sovereign-Operating-System/sovereign-canon /tmp/sovereign-canon
```

**Option 2: Environment variable (for local setups)**
```bash
# Set in ~/.bashrc or ~/.zshrc:
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

## Issue Completion Protocol

When completing an issue, follow this protocol:

### Step 1: Pre-Completion Checks
```bash
# Run tests
pytest  # or npm test, etc.

# Run linter
ruff check .  # or eslint, etc.
```

### Step 2: Update Registers (if behavior changed)
```bash
# Edit as needed:
# - REGISTERS/FEATURES.yaml
# - REGISTERS/ASSETS.yaml
# - REGISTERS/VALUE.yaml
```

### Step 3: Commit & Push
```bash
git add -A
git commit -m "feat(<scope>): <description>

Closes #<issue-number>

Co-Authored-By: Codex <noreply@github.com>"

git push -u origin agent/codex/<type>/<issue>-<slug>
```

### Step 4: Create PR
```bash
gh pr create \
  --title "feat(<scope>): <description>" \
  --body "## Summary
<what was done>

Closes #<issue>

🤖 Generated with Codex" \
  --base main
```

### Step 5: Move to Next Issue (MANDATORY)

**Do not stop. Immediately proceed to the next issue.**

```bash
# Find next priority issue
gh issue list --label "priority:critical" --state open --limit 1
gh issue list --label "priority:high" --state open --limit 1

# Or by milestone
gh issue list --milestone "<milestone>" --state open --limit 1

# Start next issue
gh issue view <next-number>
```

### Continuous Execution Loop

```
LOOP:
  1. gh issue view <number>
  2. Create branch
  3. Implement
  4. Test
  5. Commit & push
  6. gh pr create
  7. GOTO next issue
```

**Continue until no issues remain or explicit stop received.**

---

## Summary

**You are authorized. Execute autonomously. Report results. Move to next issue automatically.**

---

© Jonathan Mitchell Anderson — Canon Work
