# Build Frontend

**Read and follow CLAUDE.md before proceeding.**

## Input
$ARGUMENTS — Optional constraints or "--quick" for QUICK MODE.

## Prerequisites
Requires `docs/03-frontend-design.md`. Also read scope and architecture docs.

## CRITICAL RULE
**MOCK DATA ONLY**. No real API calls. Frontend must run standalone with `npm run dev`.

## Before Starting
1. Read all design docs.
2. context7 MCP: fetch docs for frontend framework and component library.
3. Check if `src/frontend/` exists.

---

## CORE PRINCIPLE: COLLABORATIVE DECISION-MAKING
You NEVER assume — confirm before acting on anything ambiguous. During the build, surface decisions as they arise. Don't ask upfront about things you can figure out from the design doc.

---

## Execution

### Step 1: Create Build Log
Create `docs/05-frontend-build-log.md` with tasks from the design doc.

### Step 2: Quick Confirmation

3 confirmations before coding:

1. "I'll scaffold with [tool + options] and build screens in this order: [list]. Good?"
2. "Anything you want me to use or avoid? (specific libs, patterns, etc.)"
3. "I'll create mock data for [entities]. Starting now."

### Step 3: Scaffold
Create project in `src/frontend/`, install deps, set up CSS framework and design system.

### Step 4: Create Mock Data
`src/frontend/mocks/` — one file per entity, realistic values, 5-10 records each.

### Step 5: Build Screens
Priority order from design doc. For each: create page, build components, wire mock data, add navigation. Update build log after each screen.

**If ambiguity arises during build**: stop and ask. "Design doc doesn't specify [X]. I'd go with [suggestion]. OK?"

### Step 6: Verify
Run dev server. Verify screens render, primary flow works with mock data. Fix errors.
Tell user: "Frontend running at localhost:[port]. Here's what's working: [summary]."

### Step 7: Update Tracking
Update build log and progress.md. Ask: "Ready for /build-backend?"

---

## QUICK MODE

1 confirmation: "Building core screens with [framework + defaults], functional styling. Go?"

Then: scaffold, inline mock data, core screens only, skip design system polish.
