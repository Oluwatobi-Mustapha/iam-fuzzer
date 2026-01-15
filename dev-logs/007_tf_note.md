# Log 007: Building the Crime Scene using Terraform
**Date:** 2026-01-15

## 1. Objective
Before writing the detection logic, I needed a reproducible test environment. I used **Terraform** to deploy three specific IAM Roles that simulate real-world security vulnerabilities.

## 2. The Infrastructure (The Lab)
I created three roles in my **Trusting Account** to test different attack vectors:

* **Role A (Stranger Danger):**
    * **Configuration:** Trusts a completely external/unknown AWS Account ID (Account B).
    * **The Risk:** Simulates a developer accidentally granting access to the wrong account or a malicious 3rd party.

* **Role B (The Confused Deputy):**
    * **Configuration:** Trusts a "Vendor" account (simulated using my own Account ID) but is **missing** the `sts:ExternalId` condition.
    * **The Risk:** Vulnerable to the "Confused Deputy" attack, where a malicious customer of the Vendor could trick the Vendor into assuming this role.

* **Role C (The Secure Control):**
    * **Configuration:** Trusts the same "Vendor" account but **enforces** the `sts:ExternalId` condition.
    * **The Outcome:** Secure. Only the specific Vendor entity with the correct secret can assume this role.

## 3. Engineering Decisions
* **Dynamic Data Sources:** Used `data "aws_caller_identity"` to fetch the Account ID dynamically, ensuring the code is portable for any user to simulate the Vendor scenarios.

* Used `jsonencode` for cleaner policy definitions and properly tagged resources for environment tracking(Teraform official doc pointed me to it)

## 4. Outcome
Running `terraform apply` successfully deployed the 3 roles. The vuln.lab is live and ready for scanning.