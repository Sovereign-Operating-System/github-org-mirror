# Agent Initialization Contract (Binding)

All AI agents operating in this repo (and any repo adopting this canon) are bound by the following rules.

## 1) Scope & authority
- Agents act as implementation assistants, not as ultimate decision-makers.
- Agents must follow repo governance and architecture constraints.
- Agents must not introduce policy/legal claims beyond what is already approved.

## 2) Branch & PR discipline
- Use `agent/*` branches when applicable.
- Every PR must:
  - reference the governing issue (`Closes #123`) when applicable,
  - keep CI green (or explicitly document waiver by owner),
  - include a clear summary and test/verification notes.

## 3) Size limits (anti-chaos)
- If diff > 400 lines, agent must:
  - split into smaller PRs, OR
  - add label `size:xl` and provide justification + rollback plan.

## 4) Register updates (anti-drift)
If a PR changes product behavior, UI flows, APIs, data models, or business logic,
it must update one or more:
- `REGISTERS/FEATURES.yaml`
- `REGISTERS/ASSETS.yaml`
- `REGISTERS/VALUE.yaml`

## 5) Security & secrets
- Never commit secrets.
- Never output secrets into issues or logs.
- Use environment variables and secret managers.

## 6) Evidence-grade changes
For work touching disputes, identity, access, payments, or legal posture:
- preserve audit trails,
- avoid destructive migrations without a recovery plan,
- document chain-of-custody where relevant.

## 7) Tone & collaboration
Templates should be calm, factual, and non-hostile.

## 8) Precedence
If there is a conflict:
1) Master Brief (current edition)
2) This Agent Contract
3) Repo-level architecture rules
4) Issue acceptance criteria
