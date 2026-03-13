# System Architecture

**Read and follow CLAUDE.md before proceeding.**

## Input
$ARGUMENTS — Optional refinements or "--quick" for QUICK MODE.

## Prerequisites
Requires `docs/01-scope.md`. If not found, tell user to run `/scope` first.

## Before Starting
1. Read `docs/01-scope.md` completely.
2. Read `docs/progress.md` — verify scope is complete.

---

## CORE PRINCIPLE: COLLABORATIVE DECISION-MAKING
You NEVER assume — you suggest and ask. Present your architecture proposal with reasoning, and ask the user to confirm key decisions before proceeding.

---

## FULL MODE

### Step 1: Create Todo
Create `docs/02-architecture-todo.md` with tasks.

### Step 2: Research
- WebSearch: architecture patterns for this type of system
- context7 MCP: `resolve-library-id` → `query-docs` for chosen frameworks

### Step 3: Present Proposal & Ask Key Questions

Do your analysis. Then present the architecture as a proposal with 5-6 questions in ONE round:

"Here's the architecture I'd propose. A few decisions I need your input on:

1. **Architecture pattern**: I'd go with [monolith/modular monolith/services] because [reason]. Alternative: [X]. Your call?
2. **Database schema**: Here are the entities I see: [table: Entity | Key Fields | Relationships]. Any missing or wrong?
3. **Core API surface**: [table: Method | Endpoint | Purpose] — these cover the main journey. Anything to add?
4. **Auth approach**: I'd suggest [JWT/session/etc.] because [reason]. Preference?
5. **Communication pattern**: [REST/WebSocket/GraphQL] because [reason]. Agree?
6. **Caching/hot path**: I'd cache [X] in [Redis/memory] because [reason]. Makes sense?"

Wait for answers.

### Step 4: Launch 5 Agents with Confirmed Decisions

Pass CONFIRMED choices into each agent.

**Agent 1 — CTO (System Architecture)**
Description: "CTO architecture validation"
Prompt: "Validate and detail this CONFIRMED architecture.
Scope: [summary]. Confirmed decisions: [PASTE].
- Component breakdown (table: Component | Responsibility | Technology | Scaling Strategy)
- Data flow for primary journey
- Text-based architecture diagram
- Flag concerns with confirmed decisions
1 page max. Tables."

**Agent 2 — Product Lead (API Design)**
Description: "Product Lead API validation"
Prompt: "Detail the CONFIRMED API design.
Scope: [summary]. Confirmed decisions: [PASTE].
- Full endpoint spec (table: Method | Path | Description | Request | Response | Auth)
- Pagination, filtering conventions
- Error response format
- Flag gaps in confirmed endpoints
1 page max. Tables."

**Agent 3 — Design Lead (Data Architecture)**
Description: "Design Lead data architecture"
Prompt: "Detail the CONFIRMED data design.
Scope: [summary]. Confirmed decisions: [PASTE].
- Full schema (table per entity: Field | Type | Constraints | Index | Notes)
- Entity relationships with cardinality
- Indexing strategy for confirmed access patterns
- Caching detail
1 page max. Tables."

**Agent 4 — Devil's Advocate (Architecture Review)**
Description: "Devil's Advocate architecture review"
Prompt: "Stress-test the CONFIRMED architecture.
Scope: [summary]. Confirmed decisions: [PASTE].
- Single points of failure (table: Component | Impact | Mitigation)
- Bottlenecks — where does it break first?
- Over-engineering for MVP?
- Under-engineering that'll bite us immediately?
- Security gaps
1 page max. Tables."

**Agent 5 — 11th Man (Architecture Alternatives)**
Description: "11th Man architecture alternatives"
Prompt: "Challenge the CONFIRMED architecture constructively.
Scope: [summary]. Confirmed decisions: [PASTE].
1. Simpler version that still works for MVP
2. What changes at 100x scale?
3. Zero-cost infrastructure option
1 page max."

### Step 5: Synthesize into `docs/02-architecture.md`

Standard structure: overview diagram, components, API, schema, relationships, data flow, key decisions, caching, scaling plan. 3-4 pages max.

### Step 6: Review with User
Highlight agent concerns. Ask: "Architecture look right? Changes before design?"

### Step 7: Update Tracking

---

## QUICK MODE

Pareto: 4-5 decisions that drive 80% of the architecture.

1. "Monolith or services? I'd go [X] because [reason]."
2. "Schema: [entities + relationships]. Look right?"
3. "Core endpoints: [list 5-8]. Any missing?"
4. "Auth: [approach]. OK?"
5. "Anything else architecturally important?"

After answers: create `docs/02-architecture.md` (2 pages). Done.
