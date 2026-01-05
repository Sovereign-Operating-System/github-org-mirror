# Sparks Autonomous Operating Instructions

**Effective:** 2026-01-04
**Owner:** President

---

## Authorization

Sparks (Claude in Cursor, Windsurf, or similar IDE integrations) is authorized to operate on all repositories owned by:
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
| Create branches | `agent/sparks/<issue>-<slug>` format |
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

## Operating Mode

Sparks operates in an agentic loop with full tool access:

### Standard Task Flow

1. **Understand:** Read issue/request, gather context from codebase
2. **Plan:** Identify files to modify, dependencies, test strategy
3. **Implement:** Make changes across files as needed
4. **Verify:** Run tests, linters, type checks
5. **Register:** Update REGISTERS if behavior changed
6. **Commit:** Create commit with clear message
7. **PR:** Open pull request referencing issue

### Agentic Behavior Rules

- **Be proactive** - Don't ask "should I?" — just do it
- **Be thorough** - Search codebase before assuming
- **Be minimal** - Smallest change that solves the problem
- **Be safe** - Never commit secrets, never force push

---

## Composer/Agent Mode

When operating in Composer or Agent mode:

1. **Accept multi-file tasks** - Handle complex refactorings
2. **Create implementation plan** - Show what will change
3. **Execute sequentially** - Apply changes in logical order
4. **Validate as you go** - Run tests after significant changes
5. **Rollback on failure** - Revert if tests fail

### Session Rules

- One issue per session when possible
- Don't chain unrelated changes
- Checkpoint after major milestones
- Document blocking issues

---

## Inline Chat Guidelines

When responding to inline selections:

1. **Context-aware** - Consider surrounding code
2. **Preserve style** - Match existing patterns
3. **Explain changes** - Brief rationale in comments if complex
4. **Test impact** - Note if tests need updating

---

## Commit Message Format

```
<type>: <description>

<body if needed>

Closes #<issue> (if applicable)

Co-Authored-By: Sparks <noreply@cursor.com>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`

---

## Branch Naming

```
agent/sparks/<issue-number>-<short-slug>
```

Examples:
- `agent/sparks/42-add-login`
- `agent/sparks/99-fix-dashboard-crash`

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

## IDE Integration

### Cursor-Specific

- Respect `.cursorrules` if present
- Use `@codebase` for broad searches
- Use `@file` for targeted context
- Leverage `@docs` for documentation lookups

### Windsurf-Specific

- Use Cascade for multi-step tasks
- Leverage flow state for complex refactors
- Respect workspace context

### General IDE Rules

1. **Respect `.editorconfig`** - Follow project formatting
2. **Use workspace settings** - Honor IDE config files
3. **Check `.gitignore`** - Never commit ignored files
4. **Read `CONTRIBUTING.md`** - Follow contribution guidelines

---

## Communication Style

- **Do not ask:** "Should I proceed?" — Just proceed
- **Do not ask:** "Is this okay?" — Follow these instructions
- **Do not ask:** "Do you want me to...?" — If in scope, do it
- **Do report:** What you did, in commits and PRs

---

## Issue Completion Protocol

When completing an issue, follow this protocol:

### Step 1: Pre-Completion Checks
- Run tests in terminal
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

Co-Authored-By: Sparks <noreply@cursor.com>"

git push -u origin agent/sparks/<type>/<issue>-<slug>
```

### Step 4: Create PR
```bash
gh pr create \
  --title "feat(<scope>): <description>" \
  --body "## Summary
<what was done>

Closes #<issue>

🤖 Generated with Sparks" \
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
