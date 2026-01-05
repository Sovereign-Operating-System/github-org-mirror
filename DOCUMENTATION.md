# Documentation Standards

This document defines documentation requirements for all repositories under SOS Canon governance.

## Required Documentation

### Root Level (Mandatory)

| File | Purpose | Minimum Content |
|------|---------|-----------------|
| `README.md` | Project overview | 10+ lines with description, setup, governance |
| `CONTRIBUTING.md` | Contribution guide | How to contribute, PR process |
| `SECURITY.md` | Security policies | Vulnerability reporting, security contacts |
| `LICENSE.md` | License terms | Proprietary notice |
| `IP_CANON.md` | IP protection | Intellectual property terms |
| `CHANGELOG.md` | Version history | Keep updated with changes |

### Documentation Folder (`docs/`)

| File | Purpose |
|------|---------|
| `docs/README.md` | Documentation index |
| `docs/architecture/overview.md` | System architecture |
| `docs/product/roadmap.md` | Product roadmap |
| `docs/runbooks/dev.md` | Development setup |
| `docs/runbooks/deploy.md` | Deployment guide |

### GitHub Folder (`.github/`)

| File | Purpose |
|------|---------|
| `.github/pull_request_template.md` | PR template |
| `.github/ISSUE_TEMPLATE/*.yml` | Issue templates |
| `.github/AGENTS.md` | Agent instructions |

## README.md Structure

Every README must include:

```markdown
# Project Name

Brief description of the project.

## Overview
What this project does and why it exists.

## Tech Stack
- Framework/language
- Key dependencies

## Getting Started
### Prerequisites
### Installation
### Running

## Governance
Link to governance docs (IP_CANON, LICENSE, etc.)

## Documentation
Links to docs folder contents.

## License
Proprietary notice with IP_CANON reference.
```

## Code Documentation

### Comments
- Document complex logic
- Explain "why" not "what"
- Keep comments current with code

### Function Documentation
```typescript
/**
 * Brief description of function purpose.
 *
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws Description of possible errors
 *
 * @example
 * const result = functionName(param);
 */
```

### API Documentation
- Document all public endpoints
- Include request/response examples
- Document error responses
- Keep OpenAPI/Swagger specs updated

## Documentation Updates

### When to Update

| Event | Update Required |
|-------|-----------------|
| New feature | README, CHANGELOG, API docs |
| Bug fix | CHANGELOG |
| Breaking change | README, CHANGELOG, migration guide |
| Architecture change | DECISIONS.md, architecture docs |
| Dependency update | CHANGELOG |
| Security fix | CHANGELOG, SECURITY.md if needed |

### CHANGELOG Format

```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Change description

### Fixed
- Bug fix description

### Security
- Security fix description

### Removed
- Removed feature description
```

## Documentation Quality

### Clarity
- Use simple, direct language
- Avoid jargon without explanation
- Include examples for complex concepts

### Accuracy
- Keep documentation in sync with code
- Review docs during code review
- Test setup instructions regularly

### Completeness
- Document all public APIs
- Include error handling
- Cover edge cases

## Documentation Review Checklist

- [ ] README accurately describes project
- [ ] Setup instructions work on clean environment
- [ ] All public functions documented
- [ ] API endpoints documented with examples
- [ ] CHANGELOG updated
- [ ] No outdated information
- [ ] Links are valid
- [ ] Code examples are tested

## Automated Enforcement

The `docs-guard.yml` workflow enforces:
- README.md exists and has content
- CONTRIBUTING.md exists
- SECURITY.md exists
- docs/ folder exists

## Templates

Documentation templates are available in:
- `sovereign-canon/pack/root/` - Root file templates
- `sovereign-canon/pack/root/docs/` - Docs folder templates

---

*Part of the SOS Canon governance framework.*
