# Backend Design

**Read and follow CLAUDE.md before proceeding.**

## Input
$ARGUMENTS — Optional constraints or "--quick" for QUICK MODE.

## Prerequisites
Requires `docs/01-scope.md` and `docs/02-architecture.md`.

## Before Starting
1. Read scope and architecture docs.
2. context7 MCP: resolve and query docs for backend framework and ORM.
3. WebSearch: domain-specific API patterns.

---

## CORE PRINCIPLE: COLLABORATIVE DECISION-MAKING
You NEVER assume — you suggest and ask. Present your backend design with reasoning, and confirm key decisions before creating the design doc.

---

## FULL MODE

### Step 1: Create Todo
Create `docs/04-backend-todo.md` with tasks.

### Step 2: Research
- context7: framework structure, ORM docs
- WebSearch: domain-specific API patterns

### Step 3: Present Proposal & Ask Key Questions

ONE round, 5-6 questions:

"Here's the backend design I'd propose:

1. **Project structure**: I'd organize as [summary]. Any preferences?
2. **Schema detail**: Here's the full schema: [table per entity with fields, types, constraints]. Any fields to add or change?
3. **API endpoints**: [table: Method | Path | Description | Status Codes]. Any to add or modify?
4. **Auth**: I'd suggest [approach] for the demo because [reason]. Your preference?
5. **Validation rules**: [table: Operation | Rules | Edge Cases]. Anything missing?
6. **Seed data**: I'd create [X records for Y entities] covering [scenarios]. Enough for a demo?"

Wait for answers.

### Step 4: Create Design Doc

After confirmation, create `docs/04-backend-design.md`:

```
# Backend Design: [System Name]

## Project Structure
[confirmed structure]

## Database Schema (Detailed)
### [Table Name]
| Field | Type | Constraints | Index | Notes |
|-------|------|-------------|-------|-------|

### Relationships

## API Endpoints (Detailed)
### [Group]
| Method | Path | Description | Request | Response | Status Codes |
|--------|------|-------------|---------|----------|-------------|

## Business Logic Rules
| Operation | Validation Rules | Edge Cases |
|-----------|-----------------|------------|

## Error Handling
| Error Type | HTTP Status | Response Format |
|-----------|-------------|-----------------|

## Seed Data
| Entity | Count | Purpose |
|--------|-------|---------|
```

3 pages max.

### Step 5: Review with user, update tracking.

---

## QUICK MODE

Pareto: 4 questions.

1. "Schema: [entities with key fields]. Look right?"
2. "Core endpoints: [list 5-8]. Any missing?"
3. "Auth: [simple approach] for demo. OK?"
4. "Seed data: [X records for Y entities]. Enough?"

After answers: create design doc (1 page). Done.
