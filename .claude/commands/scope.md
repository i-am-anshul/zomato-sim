# Requirements Discovery

**Read and follow CLAUDE.md before proceeding.**

## Input
$ARGUMENTS — Problem statement to scope. If contains "--quick", run in QUICK MODE (strip "--quick" from the problem statement).

## Prerequisites
None — this is the first phase.

## Before Starting
1. Check if `docs/progress.md` exists. Create it if not.
2. If scope already complete (check progress.md), confirm with user before overwriting.
3. Create `docs/` directory if it doesn't exist.

---

## CORE PRINCIPLE: COLLABORATIVE DECISION-MAKING
You NEVER assume — you suggest and ask. Present your analysis, give recommendations with reasoning, and ask the user to confirm key decisions before proceeding.

---

## FULL MODE

### Step 1: Create Todo
Create `docs/01-scope-todo.md`:
- [ ] Analyze problem and present initial assessment
- [ ] Ask user key scoping questions
- [ ] Launch 5 perspective agents with confirmed decisions
- [ ] Synthesize into scope document
- [ ] Review with user
- [ ] Update progress tracker

### Step 2: Present Analysis & Ask Key Questions

Read the problem statement. Do your own analysis first. Then present it to the user as a structured proposal with 5-7 questions in ONE round. Don't spread across multiple rounds — be efficient.

Present your thinking, then ask:

"Here's my initial read on this. I have a few questions before I go deeper:

1. **Users & core problem**: I'm seeing [personas] solving [problem]. Does that match, or is the focus different?
2. **MVP features**: I'd prioritize these for MVP: [table: Feature | Priority | Why]. What would you add, remove, or change?
3. **Out of scope**: I'd cut [list] from MVP. Agree, or should any of these stay?
4. **Scale targets**: I'm estimating [DAU, QPS, storage] based on [reasoning]. Roughly right, or are we targeting something different?
5. **Tech stack**: I'd go with [stack] because [reasons]. Any preferences or constraints?
6. **Biggest risk**: The hardest part looks like [X]. Is that where you'd focus too?
7. **Anything else**: Hard constraints I should know about? (compliance, existing systems, specific cloud, etc.)"

Wait for answers.

### Step 3: Launch 5 Agents with Confirmed Context

ONLY after the user has answered, launch agents. Pass the CONFIRMED decisions into each prompt.

Use the Agent tool to launch ALL 5 simultaneously.

**Agent 1 — CTO (Technical Feasibility)**
Description: "CTO perspective on requirements"
Prompt: "You are a CTO evaluating a new project.
Problem: [PROBLEM STATEMENT]
Confirmed decisions: [PASTE USER'S CONFIRMED CHOICES]

Given these CONFIRMED requirements, analyze in TABLE format:
1. Technical constraints and infrastructure requirements
2. Validate scalability projections against the user's targets — flag concerns
3. Real-time vs batch processing needs
4. Integration complexity with external systems
5. Tech stack validation: Component | Technology | Risks | Considerations
6. Performance requirements: latency targets, throughput, availability SLA

Be specific with numbers. Back-of-envelope math. 1 page max. Tables only.
Flag anything that conflicts with the user's decisions — do NOT silently override them."

**Agent 2 — Product Lead (Product Requirements)**
Description: "Product Lead perspective on requirements"
Prompt: "You are a Product Lead validating scope.
Problem: [PROBLEM STATEMENT]
Confirmed decisions: [PASTE USER'S CONFIRMED CHOICES]

Given these CONFIRMED requirements:
1. Validate personas — any gaps? (table: Persona | Goal | Pain Point | Gap?)
2. Refine user stories from confirmed features (table: As a [user] I want [action] so that [value]) — 5-8 max
3. Validate feature priorities (table: Feature | User's Priority | Your Assessment | Flag if Different)
4. Success metrics (3-5 KPIs with targets)
5. Validate MVP scope — flag if too big or missing something critical
6. Refine primary user journey (numbered steps)

Respect confirmed decisions. Flag concerns, don't override. 1 page max. Tables only."

**Agent 3 — Design Lead (UX Requirements)**
Description: "Design Lead perspective on UX"
Prompt: "You are a Design Lead evaluating UX needs.
Problem: [PROBLEM STATEMENT]
Confirmed decisions: [PASTE USER'S CONFIRMED CHOICES]

Given these CONFIRMED requirements:
1. Key screens needed (table: Screen | Route | Purpose | Priority: Core/Secondary)
2. Primary user flow (numbered steps with screen transitions)
3. Secondary flows (just list them)
4. Information architecture — what data on which screen
5. Mobile vs desktop priority
6. Critical UX details: loading states, empty states, error states

1 page max. Tables only."

**Agent 4 — Devil's Advocate (Risk & Edge Cases)**
Description: "Devil's Advocate risk analysis"
Prompt: "You are the Devil's Advocate. Find what could go wrong.
Problem: [PROBLEM STATEMENT]
Confirmed decisions: [PASTE USER'S CONFIRMED CHOICES]

Stress-test the CONFIRMED decisions:
1. Dangerous assumptions (table: Assumption | Why Dangerous | What If Wrong)
2. Edge cases that break the system (table: Scenario | Impact | Mitigation)
3. Scale failure scenarios against confirmed targets
4. Security and abuse vectors
5. Data consistency risks
6. Risks specific to the chosen tech stack

Be pessimistic. Real problems only. 1 page max. Tables only."

**Agent 5 — 11th Man (Fresh Perspectives)**
Description: "11th Man unconventional analysis"
Prompt: "You are the 11th Man — the contrarian.
Problem: [PROBLEM STATEMENT]
Confirmed decisions: [PASTE USER'S CONFIRMED CHOICES]

Challenge the confirmed approach (respectfully):
1. What if we're solving the wrong problem? Reframe it.
2. 2 unconventional approaches the team hasn't considered
3. A radically simpler version — 80% value in 20% effort
4. Emerging tech that could leapfrog the chosen approach
5. What to cut with 1/10th the time?
6. Cross-industry insight

Creative but grounded. 1 page max."

### Step 4: Synthesize

After ALL 5 agents return, combine into `docs/01-scope.md`:

```
# Scope: [System Name]

## Problem Statement
[2-3 sentences]

## Functional Requirements
| Feature | Priority | Complexity | Notes |
|---------|----------|------------|-------|

## Non-Functional Requirements
| Requirement | Target | Justification |
|-------------|--------|---------------|

## Back-of-Envelope Estimates
| Metric | Estimate | Calculation |
|--------|----------|-------------|

## MVP Scope
**In Scope:** [bulleted list]
**Out of Scope:** [bulleted list]

## Primary User Journey
1. [step]

## Key Risks & Mitigations
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|

## Alternative Approaches Considered
| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|

## Tech Stack
| Component | Technology | Why | Alternative |
|-----------|-----------|-----|-------------|
```

3-4 pages max.

### Step 5: Review & Finalize
Present scope. Highlight any agent flags that conflict with confirmed decisions.
Ask: "Does this capture what we discussed? Any changes before /architect?"

### Step 6: Update Tracking
- Update `docs/01-scope-todo.md` and `docs/progress.md`

---

## QUICK MODE

Pareto: 4-5 questions that drive 80% of the scope.

1. "Who's the primary user and what's the #1 thing they need? I'd say [suggestion]."
2. "Core MVP features: [list 5-7]. Quick thumbs up/down on each?"
3. "Tech stack — I'd go with [stack]. OK, or preference?"
4. "Biggest risk I see is [X]. Agree?"
5. "Anything else I must know?"

After answers: create `docs/01-scope.md` (1-2 pages), update progress. Done.
