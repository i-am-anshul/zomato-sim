# Build System

## Overview
Structured pair programming workflow for rapid prototyping. Eight phases, each with its own slash command. Commands chain sequentially — each reads previous phase output.

## Workflow
```
/scope → /architect → /design-frontend + /design-backend (parallel) → /build-frontend + /build-backend (parallel) → /integrate → /verify
```

## Modes

### Full Mode (default)
Multi-perspective analysis using 5 parallel agents:
- **CTO**: Technical feasibility, infra, scalability, tech stack
- **Product Lead**: User stories, features, MVP scope, success metrics
- **Design Lead**: UX flows, information architecture, accessibility
- **Devil's Advocate**: Risks, edge cases, failure scenarios, security
- **11th Man**: Unconventional angles, simpler alternatives, contrarian views

### Quick Mode (append `--quick` to any command)
Single-agent fast execution. Same output structure, condensed depth. Use when time-constrained.
Example: `/scope --quick Design a ride-sharing app`

## Documentation Rules
1. EVERY phase creates/updates `docs/progress.md`
2. EVERY phase creates a todo file before starting work, follows it, updates it
3. Documents are **3-4 pages MAX**
4. Use **tables** for comparisons and decisions — not paragraphs
5. Show **reasoning** with every choice: "Chose X because Y. Alternative: Z."
6. Visual aids: diagrams (text-based), tables, checklists over prose

## File Convention
```
docs/
├── progress.md                ← Master tracker (updated every phase)
├── 01-scope.md                ← /scope output
├── 02-architecture.md         ← /architect output
├── 03-frontend-design.md      ← /design-frontend output
├── 04-backend-design.md       ← /design-backend output
├── 05-frontend-build-log.md   ← /build-frontend tracking
├── 06-backend-build-log.md    ← /build-backend tracking
├── 07-integration-log.md      ← /integrate tracking
├── 08-verification-report.md  ← /verify output

src/
├── frontend/                  ← Frontend code
├── backend/                   ← Backend code
```

## Quality Bar
- Every decision has a WHY and an alternative considered
- Code is demo-ready (works, shows core flow) not production-ready
- Frontend with mock data must be demo-able standalone (`npm run dev` shows something)
- Backend with seed data must respond to API calls standalone
- Concise > comprehensive. 3 pages that matter > 20 pages of filler.

## Tool Usage
- **WebSearch**: Research best practices and current library versions BEFORE implementing
- **context7 MCP**: Fetch up-to-date docs for frameworks/libraries. Always: `resolve-library-id` → `query-docs`
- **frontend-design skill**: For high-quality UI components and design system
- **webapp-testing skill**: For Playwright-based verification
- **Agent tool**: For multi-perspective analysis in full mode (5 parallel agents)

## Tech Defaults (override based on problem)
| Component | Default | Why |
|-----------|---------|-----|
| Frontend | React/Next.js + Tailwind | Fast to scaffold, great DX |
| Backend | Python Django/DRF or Node Express | Depends on problem complexity |
| Database | PostgreSQL | ACID, flexible, well-supported |
| Cache | Redis | Fast, versatile, well-documented |
| Cloud | AWS | Industry standard |

## Collaboration Rules (CRITICAL)
- **NEVER assume** — always suggest with reasoning and ask the user for confirmation
- Every significant decision must be confirmed by the user before proceeding
- Present options as tables with tradeoffs, give your recommendation, then wait
- In **Full Mode**: ask 5-7 key questions in ONE round, with your suggestions — don't drag it out
- In **Quick Mode**: Pareto principle — ask only 4-5 questions that drive 80% of the outcome
- Always provide your suggestion with reasoning: "I'd recommend X because Y. Alternative: Z."
- If you encounter ambiguity during any phase, stop and ask — don't guess
- The user is the decision-maker. You are the expert advisor who leads but defers.

## Important Rules
- Read `docs/progress.md` before ANY command to understand current state
- Do NOT start coding until design phase is complete
- Do NOT mix frontend and backend concerns — separate builds
- Mock data should be realistic and representative
- Keep terminal output clean — don't dump walls of logs
- If a previous phase is missing, warn and offer to run it in quick mode
