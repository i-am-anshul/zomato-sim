# Integration

**Read and follow CLAUDE.md before proceeding.**

## Input
$ARGUMENTS — Optional focus area or "--quick" for QUICK MODE.

## Prerequisites
Requires completed frontend AND backend builds. Check both build logs.

## Before Starting
1. Read all docs — scope, architecture, designs, both build logs.
2. Verify both servers run independently.

---

## CORE PRINCIPLE: COLLABORATIVE DECISION-MAKING
You NEVER assume — surface any mismatches between frontend and backend before writing code. Ask about resolution strategy.

---

## Execution

### Step 1: Create Integration Log
Create `docs/07-integration-log.md` with tasks.

### Step 2: Pre-Integration Check

3 confirmations:

1. "I compared mock data shapes vs API responses. Mismatches: [table: Screen | Issue | Suggested Fix]. I'll adjust [frontend/backend]. OK?"
2. "Integration order: [screen priority list]. Agree?"
3. "Starting with API client setup and CORS config."

### Step 3: Configure Connection
Set API base URL, configure CORS, set up API client.

### Step 4: Replace Mock Data
One screen at a time. For each: create API functions, replace mocks, add loading/error states, test.

**Surface issues**: "Screen [X] expects [shape] but API returns [different]. Adjust frontend or backend?"

### Step 5: End-to-End Test
Walk through primary flow. Verify data persists, changes reflect. Document issues.

### Step 6: Update Tracking
Ask: "Integration complete. [X/Y] screens connected. Ready for /verify?"

---

## QUICK MODE

1 confirmation: "Connecting primary flow only ([screens]), skipping loading/error states. Go?"

Then: primary flow only, minimal CORS, one journey end-to-end.
