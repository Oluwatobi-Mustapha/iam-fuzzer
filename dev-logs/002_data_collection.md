# Log 002: IAM Data Collection & The Inline Blind Spot
**Date:** 2026-01-08
**Status:** Complete

## 1. Objective
Build the "Harvester" component of the fuzzer. The goal is to extract custom IAM policies from a target account so they can be analyzed for logic flaws.

## 2. The "Blind Spot" Problem
I discovered that the standard AWS API call `list_policies()` is insufficient for a security audit.
* **Limitation:** It only lists **Managed Policies** (standalone documents).
* **Risk:** It completely ignores **Inline Policies** (embedded directly on users). Hackers often use Inline Policies to hide backdoors because standard scanners miss them.

## 3. The Solution: Dual-Scanner Architecture
I implemented a two-part collection strategy in `src/collector.py`:

### A. The Managed Scanner (`list_customer_policies`)
* **Method:** Uses `list_policies(Scope='Local')`.
* **Purpose:** Filters out default AWS noise to find customer-created logic.

### B. The Inline Scanner (`list_inline_policies`)
* **Method:** Iterates through `list_users()`, then calls `list_user_policies()` on each individual.
* **Analogy:** "Frisking" every user in the room instead of just reading the notice board.

## 4. Verification
Ran the collector against `target-prod`.
* **Result:** Successfully detected the bait policies (`fuzzer-test-admin-flaw`) AND the hidden inline policy on the test user.