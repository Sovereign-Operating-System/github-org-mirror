# Agent Handoff Protocol

This document defines the standard procedure for handing off work between AI agents or between sessions.

## Purpose

Ensure continuity of work when:
- A session ends mid-task
- Work is transferred between agents
- Context needs to be preserved for future sessions

## Handoff Document Requirements

When ending a session or handing off work, create a `HANDOFF.md` file in the repository root containing:

### 1. Session Summary
```markdown
## Session Summary
- **Date**: YYYY-MM-DD
- **Agent**: [Claude/Copilot/Codex/etc.]
- **Duration**: [approximate time]
- **Branch**: [current branch name]
```

### 2. Work Completed
```markdown
## Completed
- [ ] Task 1 description
- [ ] Task 2 description
```

### 3. Work In Progress
```markdown
## In Progress
- [ ] Task currently being worked on
  - Current state: [description]
  - Next step: [what needs to happen]
  - Blocker (if any): [description]
```

### 4. Pending Work
```markdown
## Pending
- [ ] Task not yet started
- [ ] Another pending task
```

### 5. Context & Decisions
```markdown
## Context
- Key decision made: [description and rationale]
- Architecture note: [relevant technical context]
- Dependencies: [external factors]
```

### 6. Files Modified
```markdown
## Files Changed
- `path/to/file1.ts` - [brief description of changes]
- `path/to/file2.ts` - [brief description of changes]
```

### 7. Commands to Resume
```markdown
## Resume Commands
```bash
git checkout [branch]
npm install  # if dependencies changed
npm run dev  # to start development
```
```

### 8. Warnings & Notes
```markdown
## Warnings
- Do not modify X until Y is complete
- Tests are currently failing because [reason]
- API key expires on [date]
```

## Handoff Checklist

Before ending a session:

- [ ] All work committed to git
- [ ] Branch pushed to remote
- [ ] HANDOFF.md created/updated
- [ ] No uncommitted secrets or credentials
- [ ] Development server stopped
- [ ] Any running processes documented

## File Location

- Primary: `/HANDOFF.md` (repository root)
- Archive: `/docs/handoffs/HANDOFF-YYYY-MM-DD.md`

## Automatic Handoff

Agents should automatically create a handoff document when:
1. User indicates session is ending
2. Complex task is partially complete
3. Explicit handoff is requested
4. Session timeout is approaching

---

*Part of the SOS Canon governance framework.*
