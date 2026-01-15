# Log 006: The Robot & The Pipeline (CI/CD)
**Date:** 2026-01-14

## Objective
Shift from manual local testing to automated **Continuous Integration (CI)**. My goal was to prove the tool's portability by having a neutral remote server (GitHub Actions) install and test the application automatically on every code push.

## The Infrastructure Change
I moved from "It works on my machine" to **"It works everywhere."**

* **GitHub Actions or The Robot:** Configured a YAML workflow (`ci-test.yml`) that acts as a sterile testing environment.
* **The Trigger:** The pipeline wakes up automatically whenever code is pushed to the repository, acting as a quality gate before anyone (including me) can claim the code is "stable."

_This mirrors real-world DevSecOps practices where security tools must run inside pipelines, not just on analyst laptops._

## The Tech Stack
* **Automation:** GitHub Actions (YAML configuration).
* **Environment Management:** Used `actions/setup-python` to provision ephemeral Linux containers.
* **Dependency Management:** Strict version control using `requirements.txt` to align local dev environments with the cloud runner.

## The Challenge (The "Red X")
The initial pipeline failed immediately despite the code working locally.
* **The Error:** `ERROR: Could not find a version that satisfies the requirement black==25.12.0`.
* **Root Cause:** The default GitHub runner was using **Python 3.9**, but my local development (and the `black` formatter) relied on **Python 3.10+**.

* So, I simply upgraded the workflow configuration to force **Python 3.11**, matching my local environment.

* Achieved a passing build (Green Checkmark). And the remote server successfully checked out the code, installed dependencies, and ran the `collector.py --help` command without crashing.

* _Screenshot:_
  ![1E93C91D-F5A9-41FD-ACFE-D5B158065585_1_201_a](https://github.com/user-attachments/assets/26e2dcc7-9704-4fa5-a769-5de2c561dbde)

  ![6110C633-D387-49DB-A046-F33180463CCB_1_201_a](https://github.com/user-attachments/assets/fc499984-3666-464d-87eb-6bf4ce3035b0)
  
  

<<<<<<< Updated upstream
=======
Achieved a passing build (Green Checkmark). And the remote server successfully checked out the code, installed dependencies, and ran the `collector.py --help` command without crashing.
>>>>>>> Stashed changes

