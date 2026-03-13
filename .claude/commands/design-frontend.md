# Frontend Design

**Read and follow CLAUDE.md before proceeding.**

## Input
$ARGUMENTS — Optional constraints or "--quick" for QUICK MODE.

## Prerequisites
Requires `docs/01-scope.md` and `docs/02-architecture.md`. If missing, tell user to run prior phases.

## Before Starting
1. Read scope and architecture docs.
2. WebSearch: current best practices, component libraries for the chosen framework.
3. context7 MCP: resolve and query docs for the frontend framework.

---

## CORE PRINCIPLE: COLLABORATIVE DECISION-MAKING
You NEVER assume — you suggest and ask. Present your design proposal with reasoning, and confirm key decisions before creating the design doc.

---

## FULL MODE

### Step 1: Create Todo
Create `docs/03-frontend-todo.md` with tasks.

### Step 2: Research
- WebSearch for component libraries, design trends
- context7 for framework patterns (routing, state management)
- Check for frontend-design skill

### Step 3: Present Proposal & Ask Key Questions

ONE round, 5-6 questions:

"Here's the frontend design I'd propose:

1. **Component library**: I'd use [X] because [reason]. Alternatives: [Y, Z]. Preference?
2. **Screens**: Here are the screens I'd build: [table: Screen | Route | Purpose | Priority]. Any to add, remove, or reprioritize?
3. **Primary flow**: [numbered screen-to-screen journey]. Does this flow make sense?
4. **State management**: [Context/Zustand/Redux] for global, [React Query/SWR] for server data. Good?
5. **Polish level**: Functional (proves concept) / Presentable (clean, professional) / Polished (animations, transitions)? I'd suggest [X] given time.
6. **Colors/style**: I'd go with [color scheme + font]. Any brand preferences?"

Wait for answers.

### Step 4: Create Design Doc

After confirmation, create `docs/03-frontend-design.md`:

```
# Frontend Design: [System Name]

## Design System
| Element | Value | Reasoning |
|---------|-------|-----------|

## Screen Inventory
| Screen | Route | Purpose | Priority | Key Data |
|--------|-------|---------|----------|----------|

## Component Hierarchy
[tree structure]

## State Management
| State | Location | Type | Reason |
|-------|----------|------|--------|

## Primary User Flow (Screen by Screen)
1. [step]

## Mock Data Plan
| Entity | Fields Needed | Sample Count | Source |
|--------|--------------|-------------|--------|
```

3 pages max.

### Step 5: Review with user, update tracking.

---

## QUICK MODE

Pareto: 4 questions.

1. "Component library: I'd use [X]. OK?"
2. "Core screens: [list]. Any changes?"
3. "Primary flow: [steps]. Right?"
4. "Polish level: [functional/presentable]. Agree?"

After answers: create design doc (1 page). Done.
