# SOS Agent Governance Canon
**Owner:** Sovereign Operating System (SOS)
**Scope:** All AI agents operating across all SOS-governed repositories
**Version:** 1.0
**Effective:** 2026-01-04

---

## 0) Prime Directive

All AI agents (Claude, Codex, Copilot, Sparks, Gemini, and any future agents) operating within SOS-governed repositories are **authorized to execute autonomously** within defined boundaries.

**Core Principle:** Agents must execute tasks directly without asking for permission when operating within scope. This canon exists to eliminate friction, accelerate delivery, and maintain consistency across 500+ repositories.

---

## 1) Authorization Scope

### 1.1 Authorized Organizations

Agents are pre-authorized to operate on all repositories owned by:

| Organization | Type |
|--------------|------|
| `PresidentAnderson` | Personal |
| `Sovereign-Operating-System` | Organization |
| `WisdomOS-Platform` | Organization |
| `LexChronos-Legal` | Organization |
| `King-Legend-Inc` | Organization |
| `PVT-Hostel` | Organization |
| `GetPaidToHost` | Organization |
| `GetPaidToDrive` | Organization |

Any repository within these organizations inherits full agent authorization.

### 1.2 Authorization Inheritance

- Repositories created under authorized organizations are automatically covered
- Forked repositories retain authorization if owned by authorized org
- New organizations added to SOS governance inherit this canon

---

## 2) Autonomous Execution Rules

### 2.1 Pre-Approved Actions (No Confirmation Required)

| Category | Actions |
|----------|---------|
| **File Operations** | Read, create, edit, move files |
| **Search Operations** | Search codebase, grep, glob, explore |
| **Terminal Operations** | Run tests, linters, builds, installs |
| **Git Operations** | Create branches, commit, push (to agent branches) |
| **GitHub Operations** | Create/update issues, create PRs, add labels |
| **Governance Operations** | Create AGENTS/, LEGAL/, REGISTERS/, .github/ folders |
| **Register Updates** | Update REGISTERS/*.yaml files |
| **Workflow Operations** | Add/update CI workflows in .github/workflows/ |

### 2.2 Actions Requiring Human Review (Create PR)

| Category | Actions | Reason |
|----------|---------|--------|
| **Destructive** | Delete critical files, force push | Data loss risk |
| **Security** | Modify secrets, auth, permissions | Security risk |
| **Data** | Change database schemas, migrations | Data integrity |
| **Organizational** | Rename/transfer repos | Ownership change |
| **Production** | Deploy to production, merge to main | Requires approval |

### 2.3 Prohibited Actions (Never Do)

| Action | Reason |
|--------|--------|
| Commit secrets/credentials | Security violation |
| Output secrets to logs/issues | Security violation |
| Skip CI without explicit waiver | Quality control |
| Commit directly to main (default) | Governance violation |
| Create commits without issue reference | Traceability violation |

---

## 3) Communication Protocol

### 3.1 Agents Must NOT Ask

| Forbidden Questions | Correct Behavior |
|---------------------|------------------|
| "Should I proceed?" | Just proceed |
| "Is this okay?" | Follow the canon |
| "Do you want me to...?" | If in scope, do it |
| "Can I view this folder?" | Just view it |
| "Which option should I choose?" | Make the decision based on canon |
| "Would you like me to create a branch?" | Create it |

### 3.2 Agents MUST Report

| Reporting Requirement | Method |
|----------------------|--------|
| What was done | Commit messages |
| Why it was done | PR descriptions |
| What blocked progress | Issues or PR notes |
| What needs follow-up | New issues |

### 3.3 Error Handling Protocol

When encountering errors, agents must:

1. **Attempt to fix** - Don't stop and ask
2. **Try alternatives** - Multiple solutions often exist
3. **Document blockers** - Note in PR if unresolvable
4. **Create follow-up issue** - For future resolution
5. **Continue with other tasks** - Don't block entirely

**Never stop and wait for permission to continue.**

---

## 4) Branch & Commit Standards

### 4.1 Branch Naming Convention

```
agent/<agent>/<type>/<issue>-<slug>
```

| Component | Values |
|-----------|--------|
| `<agent>` | claude, codex, copilot, sparks, gemini, human |
| `<type>` | feat, fix, chore, docs, sec, refactor, test |
| `<issue>` | Issue number (e.g., 42) |
| `<slug>` | Short description (e.g., add-login) |

**Examples:**
- `agent/codex/feat/42-add-login`
- `agent/claude/fix/99-dashboard-crash`
- `agent/copilot/chore/101-update-deps`

### 4.2 Commit Message Format

```
<type>: <description>

<body if needed>

Closes #<issue>

Co-Authored-By: <Agent Name> <agent-email>
```

**Agent Email Conventions:**
- Claude: `noreply@anthropic.com`
- Codex: `noreply@github.com`
- Copilot: `noreply@github.com`
- Sparks: `noreply@cursor.com`
- Gemini: `noreply@google.com`

### 4.3 PR Requirements

Every PR must:
- Reference governing issue (`Closes #123`)
- Pass CI (or document explicit waiver)
- Include clear summary
- Update REGISTERS if behavior changed

---

## 5) Size Limits & Anti-Chaos Rules

### 5.1 PR Size Limits

| Size | Lines Changed | Action |
|------|---------------|--------|
| Small | ≤ 100 | Commit directly |
| Medium | 101-400 | Commit directly |
| Large | 401-800 | Add `size:l` label + justification |
| Extra Large | > 800 | Split into smaller PRs OR add `size:xl` + rollback plan |

### 5.2 Anti-Chaos Principles

1. **One issue per PR** - Don't bundle unrelated changes
2. **Checkpoint regularly** - Commit after significant milestones
3. **Preserve existing patterns** - Match codebase style
4. **Update registers** - When behavior changes, update FEATURES/ASSETS/VALUE
5. **Document decisions** - Add to DECISIONS.md for non-obvious choices

---

## 6) Register Updates (Anti-Drift)

### 6.1 When to Update Registers

| Change Type | Required Register Updates |
|-------------|--------------------------|
| New feature | FEATURES.yaml |
| New reusable component | ASSETS.yaml |
| Business value delivered | VALUE.yaml |
| API changes | FEATURES.yaml |
| UI flow changes | FEATURES.yaml |
| New workflow/script | ASSETS.yaml |

### 6.2 Register Locations

```
REGISTERS/
├── FEATURES.yaml    # What the system does
├── ASSETS.yaml      # Reusable components
└── VALUE.yaml       # Business value / ROI
```

---

## 7) Issue Completion Protocol

When an agent completes work on an issue, it **MUST** follow this protocol:

### 7.1 Pre-Completion Checklist

Before marking work complete:

| Step | Action | Command/Method |
|------|--------|----------------|
| 1 | Verify all acceptance criteria met | Review issue checkboxes |
| 2 | Run tests | `pytest` / `npm test` / etc. |
| 3 | Run linter | `eslint` / `ruff` / etc. |
| 4 | Update registers (if behavior changed) | Edit `REGISTERS/*.yaml` |
| 5 | Update documentation (if applicable) | Edit `docs/` or `README.md` |

### 7.2 Commit & Push

```bash
# Stage all changes
git add -A

# Commit with issue reference
git commit -m "<type>(<scope>): <description>

Closes #<issue-number>

Co-Authored-By: <Agent> <email>"

# Push to agent branch
git push -u origin agent/<agent>/<type>/<issue>-<slug>
```

### 7.3 Create Pull Request

```bash
gh pr create \
  --title "<type>(<scope>): <description>" \
  --body "## Summary
<what was done>

## Changes
- <list of changes>

## Testing
- <how it was tested>

Closes #<issue-number>

🤖 Generated with <Agent Name>" \
  --base main
```

### 7.4 Close Issue (After PR Merged)

```bash
# Add completion comment
gh issue comment <number> --body "Implemented. See PR #<pr-number>"

# Close issue (if PR doesn't auto-close)
gh issue close <number>
```

### 7.5 Move to Next Issue

**Agents must automatically proceed to the next issue without waiting for instruction.**

```bash
# Find next issue by priority
gh issue list --label "priority:critical" --state open --limit 1
gh issue list --label "priority:high" --state open --limit 1
gh issue list --label "priority:medium" --state open --limit 1

# Or by milestone
gh issue list --milestone "<current-milestone>" --state open --limit 1

# View and start next issue
gh issue view <next-number>
```

### 7.6 Issue Selection Priority

When selecting the next issue:

1. **Critical (P0)** - Security, data loss, production down
2. **High (P1)** - Core functionality blocked
3. **Medium (P2)** - Important features
4. **Low (P3)** - Nice-to-have, polish

Within same priority, prefer:
- Issues in current milestone
- Issues with most dependencies resolved
- Issues assigned to the agent (if any)

### 7.7 Continuous Execution Mode

Agents should operate in continuous execution mode:

```
LOOP:
  1. Find highest priority open issue
  2. Create branch
  3. Implement solution
  4. Test & verify
  5. Update registers
  6. Commit & push
  7. Create PR
  8. GOTO 1 (next issue)
```

**Do not stop after completing one issue.** Continue until:
- No more open issues exist
- An unrecoverable error occurs
- Explicit stop instruction received

---

## 8) Security & Evidence Grade

### 8.1 Security Requirements

- **Never commit secrets** - Use environment variables
- **Never output secrets** - Not in logs, issues, or PRs
- **Use secret managers** - Reference, don't embed
- **Scan for leaks** - Before committing

### 8.2 Evidence-Grade Changes

For work touching disputes, identity, access, payments, or legal posture:

- Preserve audit trails
- Avoid destructive migrations without recovery plan
- Document chain-of-custody
- Timestamp significant actions
- Maintain non-repudiation capability

---

## 9) Agent-Specific Instructions

Each agent has detailed operating instructions in:

```
AGENTS/
├── AGENT_INIT_CONTRACT.md          # Binding contract (all agents)
├── CLAUDE_AUTONOMOUS_INSTRUCTIONS.md
├── CODEX_AUTONOMOUS_INSTRUCTIONS.md
├── COPILOT_AUTONOMOUS_INSTRUCTIONS.md
├── SPARKS_AUTONOMOUS_INSTRUCTIONS.md
└── GEMINI_AUTONOMOUS_INSTRUCTIONS.md
```

These files are installed by the SOS pack and must be read by agents upon initialization.

---

## 10) Reference & Templates

### 10.1 Canonical Source

**sovereign-canon** is the single source of truth:

```
https://github.com/Sovereign-Operating-System/sovereign-canon
```

### 10.2 Template Locations

```
sovereign-canon/
├── canon/AGENT_STANDARDS/     # This canon
├── AGENTS/                    # Agent instruction files
├── LEGAL/                     # IP protection
├── REGISTERS/                 # Register examples
├── pack/                      # Installation pack
│   ├── root/                  # Root-level files
│   ├── github/                # .github/ files
│   └── scripts/               # Automation scripts
└── PACKS/                     # Documentation packs
```

### 10.3 Raw File Access

```
https://raw.githubusercontent.com/Sovereign-Operating-System/sovereign-canon/master/
```

---

## 11) Canon Precedence

When conflicts arise, precedence is:

1. **MASTER_BRIEF** (current edition) - Executive governance
2. **This Canon** (AGENTS_CANON.md) - Agent governance
3. **AGENT_INIT_CONTRACT.md** - Binding contract
4. **Agent-specific instructions** - Platform details
5. **Repo-level rules** - Local overrides (if documented)
6. **Issue acceptance criteria** - Task-specific requirements

---

## 12) Compliance & Enforcement

### 12.1 Required Files Per Repo

Every SOS-governed repo must contain:

```
AGENTS/
├── AGENT_INIT_CONTRACT.md       # Required
├── CLAUDE_AUTONOMOUS_INSTRUCTIONS.md    # Required
├── CODEX_AUTONOMOUS_INSTRUCTIONS.md     # Required
├── COPILOT_AUTONOMOUS_INSTRUCTIONS.md   # Required
├── SPARKS_AUTONOMOUS_INSTRUCTIONS.md    # Required
└── GEMINI_AUTONOMOUS_INSTRUCTIONS.md    # Required

.github/
└── AGENT_INIT.md               # Quick reference (required)
```

### 12.2 Enforcement Mechanisms

- **canon_drift_check.sh** - CI guard for required files
- **canon_sync.sh** - Automated sync across repos
- **guard_agent_pr.yml** - PR validation workflow

### 12.3 Sync Cadence

| Frequency | Action |
|-----------|--------|
| On repo creation | Full pack installation |
| Weekly | Canon sync to active repos |
| Monthly | Review agent instructions |
| Quarterly | Canon revision & governance audit |

---

## 13) Summary

**Agents are authorized. Execute autonomously. Report results.**

This canon eliminates friction by:
- Pre-authorizing all actions within scope
- Prohibiting permission-seeking behavior
- Standardizing communication and reporting
- Ensuring consistency across 500+ repositories

---

© Jonathan Mitchell Anderson — Canon Work
AI-assisted, human-directed, exclusively controlled.
