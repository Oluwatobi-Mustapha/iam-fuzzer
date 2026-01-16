# Log 008: The Detection Engine & User Interface Improvement
**Date:** 2026-01-16

## 1. Objective
With the Crime Scene (Terraform Lab) active from Log 007, the goal today was to build the Python logic to detect those vulnerabilities and present them in a professional, audit-ready dashboard.

## 2. The Detection Logic (`src/analyzer.py`)
I built a "Hybrid Analyzer" to process both Trust Policies (Roles) and Permission Policies (Users).
* **Normalization:** Created a Universal Translator to handle AWS inconsistencies (converting simple strings like `"Principal": "*"` into lists to prevent crashes).
  
* **Trust Analysis (The "Confused Deputy" Check):**
    * Logic verifies if an external trust exists.
    * **Refinement:** Initially checked only for `sts:ExternalId`. Updated logic to also accept `aws:SourceAccount` or `aws:SourceArn` to prevent false positives on modern Service Roles.
 
* **Identity Analysis:** Added checks for "Admin Access" (Action: `*`) and "Privilege Escalation" (e.g., `iam:CreateUser`).

## 3. The Collector Upgrade (`src/collector.py`)
* **Integration:** Wired the `analyzer.py` logic into the scanning loop.
* **Historical Context:** Updated the Boto3 extraction to pull `CreateDate`.
    * **Why:** To distinguish between a fresh mistake (5 minutes ago) and legacy debt (3 years ago) which is a critical requirement for security auditing.

## 4. The Visualization Overhaul (`src/visualizer.py`)
I pivoted from a basic data table to a Tesla-style Product Dashboard to improve readability and executive presentation.
* **Design System:** Switched to Light Mode with "Floating Cards," utilizing `Inter` typography and high-contrast status dots (Red/Orange) instead of heavy banners.
  
* **Context-Aware Remediation:** Built a `get_remediation` engine that tailors advice based on the **Resource Name** + **Risk Type**.
    * *Example:* Explicitly warns **against** adding `ExternalID` for default Organization roles, while demanding it for Vendor roles.
 
* **Also add a link to relevant AWS official docs for quick mitigation**
    
* **UX Improvements:**
    * **Live Interaction:** Added JavaScript for instant Search and Severity Filtering (Critical vs. High).
    * **Cache Busting:** Appended `?t={timestamp}` to the report URL to force browsers to load fresh data on every run.
    * **Compliance:** Added Scan ID and Generated Time (UTC) to the header.

## 5. Final Architecture & Outcome

**Infrastructure: Terraform Lab (Vulnerable Resources).**

**Scanner: Python/Boto3 (Logic + History).**

**Report: HTML5/CSS3 (Interactive Dashboard).**

The **IAM Fuzzer v1.0** is feature-complete. It successfully deploys vulnerable infrastructure, detects complex logical risks with high precision, and generates a client-ready interactive report.

**_Screenshot_:**
<img width="2688" height="1680" alt="image" src="https://github.com/user-attachments/assets/82933c5a-4991-40e8-9969-8904b38f8960" />
