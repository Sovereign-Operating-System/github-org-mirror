
---

## Sovereign Canon Compliance

This repository is governed by the **Sovereign Operating System (SOS)** canon.

- Agent contract: `.github/AGENT_INIT.md`
- Product & ops docs: `/docs` (and Wiki if enabled)
- Roadmap: `docs/product/roadmap.md`

Deployment posture:
- Frontend defaults to **Vercel**
- Docker is enabled only when logical (service/worker or Dockerfile present)

Releases:
- Default: build-tag Release per main update (`build-YYYYMMDD-<shortsha>`)
