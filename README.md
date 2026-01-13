# iam-fuzzer

A specialized security tool for detecting privilege escalation paths in AWS Identity & Access Management (IAM). It scans both managed and inline policies to identify Shadow Admin risks based on dangerous permission combinations (`iam:CreateUser` + `iam:AttachUserPolicy`).

## Prerequisites

- Python 3.8+
- AWS CLI configured with active credentials (`~/.aws/credentials`)
- `boto3` library

## Installation

```bash
git clone (https://github.com/Oluwatobi-Mustapha/iam-fuzzer.git)
cd iam-fuzzer
pip install boto3
```
# Usage

The tool operates in **two stages**: **collection** and **visualization**.

---

## Scan Environment

First, run the [collector.py](https://github.com/Oluwatobi-Mustapha/iam-fuzzer/blob/main/src/collector.py) file in your terminal with the --profile flag to scan a specific AWS CLI profile. This step ingests IAM data, analyzes policy logic, and serializes findings to disk.

### Command

```bash
python3 src/collector.py --profile target-prod
```

### Note
- Please replace `target-prod` with your AWS CLI profile name.  
```bash
python3 src/collector.py --profile "My Profile Name"
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
python3 src/visualizer.py
```
**Output**

`report.html`

**_The generated report.html file is a standalone interactive security dashboard. Open this file in your web browser to view the results._**

---
## Artifacts

| File Name        | Description |
|------------------|-------------|
| `findings.json`  | JSON-formatted log of all detected risks, suitable for programmatic auditing |
| `report.html`    | Standalone HTML file containing the risk assessment dashboard |







