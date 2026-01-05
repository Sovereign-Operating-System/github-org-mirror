# Agent Post-Completion Protocol

This document defines required actions after completing any task or feature.

## Purpose

Ensure all work is properly documented, tested, and ready for production or handoff.

## Post-Completion Checklist

### 1. Code Quality
- [ ] Code follows `CODE_STYLE.md` guidelines
- [ ] No console.log/print statements left in code
- [ ] No commented-out code blocks
- [ ] No hardcoded secrets or credentials
- [ ] Error handling is complete
- [ ] Edge cases are handled

### 2. Testing
- [ ] Unit tests written for new functions
- [ ] Integration tests updated if needed
- [ ] All tests passing (`npm test` / `pytest` / etc.)
- [ ] Manual testing completed
- [ ] Edge cases tested

### 3. Documentation
- [ ] Code comments for complex logic
- [ ] README.md updated if needed
- [ ] API documentation updated
- [ ] CHANGELOG.md updated with changes
- [ ] DECISIONS.md updated for architectural choices

### 4. Git Hygiene
- [ ] Changes committed with descriptive message
- [ ] Commit follows conventional commit format
- [ ] Branch pushed to remote
- [ ] No merge conflicts with main branch
- [ ] PR created (if applicable)

### 5. IP Protection
- [ ] IP footer present in new source files
- [ ] `scripts/ip_footer_inject.sh` run on new files
- [ ] No third-party code added without license check

### 6. Security
- [ ] No secrets in code or commits
- [ ] Input validation on user-facing functions
- [ ] SECURITY.md reviewed for compliance
- [ ] Dependencies scanned for vulnerabilities

## Completion Report

After completing significant work, provide a summary:

```markdown
## Completion Report

### Task
[Brief description of what was completed]

### Changes Made
- `file1.ts`: [description]
- `file2.ts`: [description]

### Testing
- [x] Unit tests: PASS
- [x] Integration tests: PASS
- [x] Manual testing: PASS

### Documentation Updated
- [x] README.md
- [x] CHANGELOG.md
- [ ] API docs (not applicable)

### Next Steps
- [Any follow-up work needed]
- [Related tasks to consider]

### Notes
- [Any important context for future reference]
```

## Commit Message Format

```
type(scope): brief description

- Detail 1
- Detail 2

Closes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## File Cleanup

Before marking complete:
1. Remove any temporary files
2. Delete unused imports
3. Remove debug code
4. Clean up TODO comments (resolve or create issues)

## Verification Commands

Run before declaring completion:

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
```

## Session End Protocol

When ending a session after completing work:

1. Run verification commands
2. Commit all changes
3. Push to remote
4. Update HANDOFF.md (if continuing later)
5. Provide completion summary to user

---

*Part of the SOS Canon governance framework.*
