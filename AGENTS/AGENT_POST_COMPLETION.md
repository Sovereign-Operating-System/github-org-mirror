# Agent Post-Completion Protocol

This document defines required actions after completing any task, feature, or session.

## Session End Triggers

When the user indicates they want to end a session using phrases like:
- "close this session"
- "end session"
- "write documentation"
- "write my documentation"
- "shifting projects"
- "wrap up"

The agent MUST produce ALL deliverables defined below.

---

## Required Deliverables

### 1. Full Verbatim Session Transcript

**Location**: `SESSION_ARCHIVES/YYYY-MM-DD_[Topic]_Session.md`

**Required Content**:
- Complete word-for-word conversation log without modification
- All code snippets and tool outputs
- Chronological timeline of events
- All errors encountered and resolutions
- Full tool invocation logs
- Complete code diffs
- **Target**: 6000+ lines for comprehensive sessions

### 2. Session Summary Document

**Location**: `[TOPIC]_SESSION_SUMMARY.md` (project root)

**Required Content**:
- Executive summary of work completed
- All files created/modified with line counts
- Key decisions and technical choices
- Deployment details and URLs
- Testing checklist
- Performance metrics
- Future enhancement recommendations
- **Target**: 800-1000 lines for major features

### 3. Structured Todo List

**Location**: Within session summary

**Required Content**:
- All tasks completed (marked with ✅)
- Any remaining tasks for next session
- Manual testing required
- Known issues or blockers
- Priority levels (High/Medium/Low)

### 4. Decision Log / Changelog

**Location**: Within session summary

**Required Content**:
- Architecture decisions made
- Technology choices with rationale
- Trade-offs considered
- Git commit hashes and messages
- Deployment timestamps

### 5. TODO.md Update

**Location**: `TODO.md` (project root)

**Required Actions**:
- Add all pending tasks from session
- Include session date and context
- Organize by priority (High/Medium/Low)
- Link to session archive for full context
- Remove completed tasks

---

## Archive Structure

```
PROJECT_ROOT/
├── SESSION_ARCHIVES/
│   ├── YYYY-MM-DD_Feature_Name_Session.md
│   ├── YYYY-MM-DD_Bug_Fix_Session.md
│   ├── BUG_REPORT_YYYY-MM-DD_Description.md
│   └── README.md  # Index of all sessions
├── FEATURE_SESSION_SUMMARY.md
├── TODO.md
└── HANDOFF.md  # Current state for next session
```

---

## Session Archive Template

Each session archive MUST include these sections:

### Header
```markdown
# Session Archive: [Topic]

**Date Range**: YYYY-MM-DD to YYYY-MM-DD
**Duration**: X hours
**Topic**: [Feature/Task Name]
**Branch**: [Git branch name]
**Status**: ✅ Complete / 🚧 In Progress / ⚠️ Blocked
```

### Required Sections

1. **Executive Summary** - 2-3 paragraph overview with key deliverables and metrics
2. **User's Primary Requests** - Chronological list with exact quotes and responses
3. **Chronological Conversation Log** - Verbatim messages, tools used, code changes
4. **All Files Created/Modified** - With line counts, purpose, and code snippets
5. **Technical Decisions & Architecture** - Options considered, rationale, trade-offs
6. **Database Changes** - Schema modifications, migrations, RLS policies
7. **API Changes** - New/modified endpoints with request/response types
8. **UI/UX Changes** - New/modified components with props and styling
9. **Errors Encountered & Resolutions** - When, symptoms, root cause, solution
10. **Deployment Failures & Bug Reports** - Links to bug report files
11. **Testing & Validation** - Manual tests, automated tests, checklist for next session
12. **Deployment Process** - Git activity, Vercel/hosting details, environment variables
13. **Performance Metrics** - Bundle size, build time, query impact
14. **Dependencies Added/Modified** - Package changes with versions
15. **Knowledge & Insights Gained** - Technical learnings, gotchas, best practices
16. **Resources & References** - Documentation, libraries, issues/PRs
17. **Completed Tasks Checklist** - Implementation, deployment, documentation
18. **Pending Tasks for Next Session** - Prioritized by High/Medium/Low/Blocked
19. **Future Enhancements** - Short/Medium/Long term improvements
20. **Session Continuation Points** - Context, quick start commands, files to review
21. **Session Statistics** - Message counts, tool invocations, files changed
22. **Appendix** - Full tool outputs, complete code diffs, environment details

---

## Deployment Failure Bug Reporting

When a deployment failure occurs, AUTOMATICALLY create a bug report:

**Location**: `SESSION_ARCHIVES/BUG_REPORT_YYYY-MM-DD_[Description].md`

**Required Content**:
```markdown
# Bug Report: [Brief Description]

**Bug ID**: BUG-YYYY-MM-DD-XXX
**Severity**: 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low
**Status**: 🚨 Open / 🔍 Investigating / 🔧 In Progress / ✅ Resolved
**Date**: YYYY-MM-DD HH:MM:SS

## Summary
Brief description of the failure.

## Environment
- Platform: Vercel / Netlify / etc.
- Node version: vXX.XX.XX
- Branch: [branch name]
- Commit: [commit hash]

## Error Output
```bash
[Full error output and stack trace]
```

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Files Involved
- `path/to/file1.ts`
- `path/to/file2.ts`

## Attempted Solutions
1. Solution 1 - Result
2. Solution 2 - Result

## Root Cause Analysis
[If known]

## Recommended Fix
[Proposed solution]

## Related
- Session Archive: [link]
- GitHub Issue: [link if created]
```

**Triggers** (automatic bug report creation):
- Vercel/Netlify build failures
- Git push failures
- Database migration failures
- API deployment errors
- Any deployment step with non-zero exit code

---

## Post-Task Checklist

### Code Quality
- [ ] Code follows `CODE_STYLE.md` guidelines
- [ ] No console.log/print statements left in code
- [ ] No commented-out code blocks
- [ ] No hardcoded secrets or credentials
- [ ] Error handling is complete
- [ ] Edge cases are handled

### Testing
- [ ] Unit tests written for new functions
- [ ] Integration tests updated if needed
- [ ] All tests passing
- [ ] Manual testing completed

### Documentation
- [ ] Code comments for complex logic
- [ ] README.md updated if needed
- [ ] API documentation updated
- [ ] CHANGELOG.md updated with changes
- [ ] DECISIONS.md updated for architectural choices

### Git Hygiene
- [ ] Changes committed with descriptive message
- [ ] Commit follows conventional commit format
- [ ] Branch pushed to remote
- [ ] No merge conflicts with main branch

### IP Protection
- [ ] IP footer present in new source files
- [ ] `scripts/ip_footer_inject.sh` run on new files
- [ ] No third-party code added without license check

### Session Documentation
- [ ] Session transcript created in SESSION_ARCHIVES/
- [ ] Session summary created in project root
- [ ] TODO.md updated with pending tasks
- [ ] HANDOFF.md updated for next session
- [ ] Bug reports created for any failures

---

## Commit Message Format

```
type(scope): brief description

- Detail 1
- Detail 2

Closes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: [Agent Name] <noreply@anthropic.com>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## Session Statistics Template

Include at end of every session archive:

```markdown
## Session Statistics

| Statistic | Value |
|-----------|-------|
| **Total Messages** | XX |
| **User Messages** | XX |
| **Assistant Messages** | XX |
| **Tool Invocations** | XX |
| **Tools Used** | X (list) |
| **Files Read** | XX |
| **Files Created** | XX |
| **Files Modified** | XX |
| **Lines Added** | XX |
| **Lines Deleted** | XX |
| **Git Commits** | XX |
| **Deployments** | XX |
| **Errors Encountered** | XX |
| **Bugs Reported** | XX |
```

---

## Quick Reference Commands

Run before declaring session complete:

```bash
# Lint check
npm run lint

# Type check
npm run type-check

# Tests
npm test

# Build verification
npm run build

# IP footer check
scripts/ip_footer_inject.sh --check

# Git status
git status
git log --oneline -5
```

---

*Part of the SOS Canon governance framework.*
