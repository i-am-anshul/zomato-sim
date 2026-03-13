# Verification

**Read and follow CLAUDE.md before proceeding.**

## Input
$ARGUMENTS — Optional focus area or "--quick" for QUICK MODE.

## Prerequisites
Requires completed integration. Check `docs/07-integration-log.md`.

## Before Starting
1. Read all docs.
2. Ensure both frontend and backend are running.

---

## CORE PRINCIPLE: COLLABORATIVE DECISION-MAKING
You NEVER assume what "correct" looks like — confirm expected behavior with the user. Surface ambiguous results for the user to judge.

---

## Execution

### Step 1: Align on Test Plan

2 confirmations:

1. "Here's the core flow I'll verify: [table: Step | Action | Expected Result]. Match your expectations?"
2. "Acceptance bar: core flow works e2e + data persists. That enough, or should I also test [edge cases]?"

### Step 2: Core Flow Test
| Step | Action | Expected | Actual | Status |
|------|--------|----------|--------|--------|

For failures: "[Step] produced [X] instead of [Y]. Blocker or acceptable?"

### Step 3: Edge Case Tests (if user wants them)
| Edge Case | Test | Expected | Actual | Status |
|-----------|------|----------|--------|--------|

### Step 4: Quality Checklist
| Area | Status | Notes |
|------|--------|-------|

### Step 5: Review Results with User
"Passed: [list]. Failed: [list]. Ambiguous: [list — need your call]. Fix anything before finalizing?"

### Step 6: Create Report
`docs/08-verification-report.md` — status, flow results, edge cases, known issues, next steps.

### Step 7: Update Tracking
Mark all phases complete. "Build complete. [summary]."

---

## QUICK MODE

1 confirmation: "Testing this flow: [steps]. Pass/fail enough?"

Core flow test only. 1 paragraph report.
