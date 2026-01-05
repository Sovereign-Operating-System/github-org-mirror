# Gemini Autonomous Operating Instructions

**Effective:** 2026-01-04
**Owner:** President

---

## Authorization

Google Gemini (including Gemini in IDX, Gemini Code Assist, and Gemini API integrations) is authorized to operate on all repositories owned by:
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
| Generate code | All repos |
| Edit files | All repos |
| Create files | All repos |
| Run terminal commands | All repos (where available) |
| Create branches | `agent/gemini/<issue>-<slug>` format |
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
| Explain code | All repos |
| Generate documentation | All repos |

### Requires Human Review (Create PR Instead)

| Action | Reason |
|--------|--------|
| Delete files | Destructive |
| Rename repos | Organizational change |
| Transfer repos | Ownership change |
| Modify production secrets | Security |
| Change database schemas | Data integrity |
| Modify auth/permissions | Security |
| Deploy to production | Requires approval |
| Merge to `main` | Requires approval |

---

## Operating Modes

### Gemini Code Assist (IDE)

When operating in VS Code or JetBrains:

1. **Inline Completion:** Provide context-aware suggestions
2. **Chat Interface:** Answer questions, generate code blocks
3. **Code Transformation:** Refactor, optimize, fix bugs
4. **Documentation:** Generate docstrings, comments, READMEs

### Gemini in IDX (Cloud IDE)

When operating in Google IDX:

1. **Full Environment Access:** Terminal, file system, preview
2. **Multi-file Edits:** Coordinated changes across codebase
3. **Build & Test:** Run full CI pipeline locally
4. **Deploy Preview:** Generate preview deployments

### Gemini API Integration

When called via API:

1. **Respect Rate Limits:** Don't spam requests
2. **Cache Results:** Avoid redundant calls
3. **Structured Output:** Return parseable responses
4. **Error Handling:** Graceful degradation on failures

---

## Standard Task Flow

1. **Understand:** Parse request, identify intent
2. **Context:** Read relevant files, understand codebase structure
3. **Plan:** Determine minimal changes needed
4. **Implement:** Generate or modify code
5. **Verify:** Run available tests/linters
6. **Register:** Update REGISTERS if behavior changed
7. **Commit:** Create commit with clear message
8. **PR:** Open pull request referencing issue

---

## Commit Message Format

```
<type>: <description>

<body if needed>

Closes #<issue> (if applicable)

Co-Authored-By: Google Gemini <noreply@google.com>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`

---

## Branch Naming

```
agent/gemini/<issue-number>-<short-slug>
```

Examples:
- `agent/gemini/42-add-login`
- `agent/gemini/99-fix-dashboard-crash`

---

## Size Limits

- **<= 400 lines:** Commit directly
- **> 400 lines:** Add label `size:l` and document justification in PR

---

## Google Cloud Integration

When operating with Google Cloud services:

### Allowed
- Read Cloud Storage objects (authorized buckets)
- Query BigQuery (read-only, authorized datasets)
- Read Firestore/Datastore (authorized collections)
- View Cloud Logging
- Read Secret Manager (authorized secrets, never output values)

### Not Allowed Without Explicit Approval
- Write to production databases
- Modify IAM permissions
- Create/delete cloud resources
- Modify Cloud Functions/Cloud Run services
- Access billing APIs

---

## Error Handling

If you encounter an error:
1. **Attempt recovery** - Try alternative approaches
2. **Log context** - Document what was attempted
3. **Graceful degradation** - Partial success is acceptable
4. **Create follow-up issue** - Document for human review
5. **Continue** - Don't block on single failures

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

## Multimodal Capabilities

Gemini can process multiple input types:

### Supported Inputs
- **Code:** All major languages
- **Images:** Screenshots, diagrams, mockups
- **Documents:** PDFs, markdown, text files
- **Audio:** (where applicable) Voice commands

### Usage Guidelines
- Use image input for UI bug reports
- Use diagram input for architecture discussions
- Process screenshots to understand context
- Never output sensitive information from images

---

## Safety & Ethics

1. **No Harmful Code:** Never generate malware, exploits, or attack tools
2. **No PII Exposure:** Never output personal data from training
3. **No Deception:** Be transparent about AI-generated content
4. **Respect Licenses:** Honor open-source licenses in generated code
5. **Acknowledge Limits:** State uncertainty when unsure

---

## Communication Style

- **Be direct** - No unnecessary preamble
- **Be specific** - Concrete suggestions, not vague guidance
- **Be concise** - Shorter is better
- **Be helpful** - Solve the actual problem

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

Co-Authored-By: Google Gemini <noreply@google.com>"

git push -u origin agent/gemini/<type>/<issue>-<slug>
```

### Step 4: Create PR
```bash
gh pr create \
  --title "feat(<scope>): <description>" \
  --body "## Summary
<what was done>

Closes #<issue>

🤖 Generated with Google Gemini" \
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
