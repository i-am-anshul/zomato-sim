# Build Backend

**Read and follow CLAUDE.md before proceeding.**

## Input
$ARGUMENTS — Optional constraints or "--quick" for QUICK MODE.

## Prerequisites
Requires `docs/04-backend-design.md`. Also read scope and architecture docs.

## Before Starting
1. Read all design docs.
2. context7 MCP: fetch docs for backend framework, ORM, database driver.
3. Check if `src/backend/` exists.

---

## CORE PRINCIPLE: COLLABORATIVE DECISION-MAKING
You NEVER assume — confirm before acting on anything ambiguous. During the build, surface decisions as they arise. Don't ask upfront about things you can figure out from the design doc.

---

## Execution

### Step 1: Create Build Log
Create `docs/06-backend-build-log.md` with tasks from the design doc.

### Step 2: Quick Confirmation

3 confirmations before coding:

1. "I'll scaffold with [framework], [DB], and build endpoints in this order: [list]. Good?"
2. "Any environment constraints? (ports, Docker vs local, existing DB, etc.)"
3. "Starting now."

### Step 3: Scaffold
Create project in `src/backend/`, install deps, set up config and project structure.

### Step 4: Database
Create models from design doc, run migrations, create and run seed script.

**If ambiguity arises**: "Design doc says [X] but I think [Y] might work better because [reason]. Which?"

### Step 5: Build API Endpoints
Priority order. Auth first (if applicable), then core CRUD, then validation and error handling. Update build log after each group.

### Step 6: Verify
Start server, test each endpoint with curl. Show user working examples.
Tell user: "API running at localhost:[port]. Here are the working endpoints: [list]."

### Step 7: Update Tracking
Update build log and progress.md. Ask: "Ready for /integrate?"

---

## QUICK MODE

1 confirmation: "Building with [framework] + SQLite, core endpoints only, skipping auth. Go?"

Then: scaffold, core CRUD only, minimal validation, hardcoded test user.
