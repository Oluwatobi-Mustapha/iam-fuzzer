## IAM Fuzzer: AWS Security Scanner

**A specialized security tool for detecting complex IAM vulnerabilities in AWS.** Unlike standard scanners, it uses context-aware logic to identify **Confused Deputy** risks, **Privilege Escalation** paths, and **Public Access** holes. It generates a Tesla-style interactive dashboard with historical tracking to distinguish between fresh risks and legacy debt.

## Prerequisites

- Python 3.9+
- AWS CLI configured with active credentials (`~/.aws/credentials`)
- `boto3` library

## Installation

```bash
git clone [https://github.com/Oluwatobi-Mustapha/iam-fuzzer.git](https://github.com/Oluwatobi-Mustapha/iam-fuzzer.git)
cd iam-fuzzer
pip install boto3
```
----
## Architecture Overview

![58EFF845-7D0A-46A2-AA5D-225FB63E0744_1_201_a](https://github.com/user-attachments/assets/a36552c6-02bd-4566-bf74-bab7f7005156)

-----
## Tool Usage

The tool operates in two stages: **collection** and **visualization**.

## 1. Scan Environment

Run the `collector.py` file with the `--profile` flag. This step ingests IAM data, applies the "Confused Deputy" detection logic, and serializes findings to disk with historical timestamps.

### Command

```bash
python3 src/collector.py --profile target-prod
```
## Usage Note

Replace `target-prod` with your specific AWS CLI profile name. If your profile name contains spaces, wrap it in quotes:

```bash
python3 src/collector.py --profile "My Profile Name"
```
## Output
```bash
findings.json
```
**Contains raw vulnerability data and creation dates.**

## 2. Generate Report

**Run the visualizer to parse the raw findings and generate the Tesla-style HTML dashboard.**
```bash
python3 src/visualizer.py
```
## Output 
```bash
report.html
```
* The generated `report.html` file is a standalone interactive security dashboard. This file will automatically open in your default web browser once you run  `python3 src/visualizer.py`

## 3. Artifacts

| File Name        | Description |
|------------------|-------------|
| `findings.json`  | JSON-formatted log of all detected risks, suitable for programmatic auditing |
| `report.html`    | Interactive HTML dashboard containing Context-Aware Remediation steps |



## 4. Dashboard Preview
The tool generates an interactive HTML report (`report.html`) that visualizes the risk paths and provides remediation steps.

<img width="2688" height="1680" alt="image" src="https://github.com/user-attachments/assets/3521a860-edb2-43ae-a361-aef8d056c663" />











