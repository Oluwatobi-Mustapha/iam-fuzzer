# Log 003: The Logic Engine & Integration
**Date:** 2026-01-12

## 1. Objective
Build the engine of the fuzzer. My goal was to create a modular logic engine (`analyzer.py`) that can take raw IAM JSON and mathematically prove if it is dangerous, then connect it to the live collector (`collector.py`).

## 2. The Inconsistency Problem
I discovered that AWS returns data inconsistently, which breaks Python loops.
* **Scenario A:** If a policy has one statement, AWS sends a **Dictionary**.
* **Scenario B:** If it has multiple statements, AWS sends a **List**.
* **In short:** AWS returns Statement as a Dictionary (if 1 item) or a List (if greater than 1 items). And this breaks loops.

* **Risk:** Writing code for one scenario causes the tool to crash (`AttributeError`) when it encounters the other.

## 3. The Solution: Normalization Pattern
I implemented a strict **Data Hygiene** layer at the start of `analyzer.py`.
* **Method:** Used `isinstance()` to check types. If the input is a String or Dict, I immediately wrap it in a List `[]`. (See [line 18 of the collector code](https://github.com/Oluwatobi-Mustapha/iam-fuzzer/blob/main/src/analyzer.py)).
* **Result:** The analysis logic only needs **one single loop**. I don't need to write duplicate code for different data shapes. This adheres to the **DRY (Don't Repeat Yourself)** principle.

## 4. The Logic Upgrade
I moved beyond simple Admin checks to catch what I refer to as **Demigod Users**.
* **Old Logic:** Checked for exact matches (`==`). Missed hackers hiding in larger lists.
* **New Logic:** Implemented **Membership Checks** (`if "iam:CreateUser" in action`).
* **Outcome:** Successfully flagged `Too-Permissive-Policy` which had broad S3 access but wasn't a full Admin.

## 5. Verification
Integrated `analyzer` into `collector`.
* **Result:** The tool successfully scanned `target-prod`, identified `Admin-Access-Trap`, and correctly flagged the inline policies.

* _Screenshot:_ <img width="1125" height="423" alt="7944EB0E-B3D6-48BB-8BCC-5D874EA4F3F8" src="https://github.com/user-attachments/assets/e2801eb0-b35e-498d-be2d-4f7203a4fefb" />

**Security Note:** The AWS accounts shown in screenshots are either deleted or modified. No live credentials are exposed. This was done intentionally for illustrative purposes.
