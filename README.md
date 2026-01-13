# iam-fuzzer

A specialized security tool for detecting privilege escalation paths in AWS Identity & Access Management (IAM). It scans both managed and inline policies to identify Shadow Admin risks based on dangerous permission combinations (`iam:CreateUser` + `iam:AttachUserPolicy`).

## Prerequisites

- Python 3.8+
- AWS CLI configured with active credentials (`~/.aws/credentials`)
- `boto3` library

## Installation

```bash
git clone [https://github.com/Oluwatobi-Mustapha/iam-fuzzer.git](https://github.com/Oluwatobi-Mustapha/iam-fuzzer.git)
cd iam-fuzzer
pip install boto3
```
# Usage

The tool operates in **two stages**: **collection** and **visualization**.

---

## Scan Environment

Run the collector to scan the `target-prod` profile. This step ingests IAM data, analyzes policy logic, and serializes findings to disk.

```bash
python src/collector.py
```
**Output**

```bash
findings.json
```
The generated findings.json file contains raw vulnerability data produced during the scan.

---
# Generate Report
Run the visualizer to parse the raw findings and generate a responsive HTML dashboard.
```bash
python src/visualizer.py
```
**Output**

`report.html`

The generated `report.html` file is a standalone interactive security dashboard.

---
## Artifacts

| File Name        | Description |
|------------------|-------------|
| `findings.json`  | JSON-formatted log of all detected risks, suitable for programmatic auditing |
| `report.html`    | Standalone HTML file containing the risk assessment dashboard |


