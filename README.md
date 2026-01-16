# iam-fuzzer
graph LR
    subgraph "Infrastructure Layer (Terraform)"
        TF[main.tf] -->|Deploys| Lab[Vulnerable IAM Lab]
        Lab -.->|Creates| RoleA(Stranger Danger Role)
        Lab -.->|Creates| RoleB(Confused Deputy Role)
    end

    subgraph "AWS Cloud"
        AWS((AWS IAM Service))
        RoleA --- AWS
        RoleB --- AWS
    end

    subgraph "Application Layer (Python)"
        Col[collector.py] -->|Boto3: GetAccountAuthorizationDetails| AWS
        AWS -->|Raw JSON| Col
        Col -->|Policy Data| An[analyzer.py]
        An -->|Logic: SourceAccount/ExternalID Check| Findings[findings.json]
    end

    subgraph "Presentation Layer"
        Findings -->|Input| Viz[visualizer.py]
        Viz -->|Generates| HTML[report.html]
        HTML -->|Opens in| Browser(Chrome/Safari)
    end

    classDef aws fill:#FF9900,stroke:#232F3E,color:white;
    classDef py fill:#3776AB,stroke:#333,color:white;
    classDef tf fill:#7B42BC,stroke:#333,color:white;
    classDef html fill:#E34F26,stroke:#333,color:white;

    class AWS aws;
    class Col,An,Viz py;
    class TF tf;
    class HTML html;
A specialized security tool for detecting privilege escalation paths in AWS Identity & Access Management (IAM). It scans both managed and inline policies to identify Shadow Admin risks based on dangerous permission combinations (`iam:CreateUser` + `iam:AttachUserPolicy`).

## Prerequisites

- Python 3.8+
- AWS CLI configured with active credentials (`~/.aws/credentials`)
- `boto3` library

## Installation

```bash
git clone https://github.com/Oluwatobi-Mustapha/iam-fuzzer.git
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









