# 🛡️ IAM Fuzzer: AWS Security Scanner

**A specialized security tool for detecting privilege escalation paths in AWS Identity & Access Management (IAM).** It scans both managed and inline policies to identify Shadow Admin risks based on dangerous permission combinations (e.g., `iam:CreateUser` + `iam:AttachUserPolicy`) and complex trust relationships.

---

## 🏗️ Architecture

```mermaid
flowchart LR
    %% Define Styles
    classDef tf fill:#7B42BC,stroke:#333,stroke-width:2px,color:white;
    classDef aws fill:#FF9900,stroke:#333,stroke-width:2px,color:white;
    classDef py fill:#3776AB,stroke:#333,stroke-width:2px,color:white;
    classDef html fill:#E34F26,stroke:#333,stroke-width:2px,color:white;
    classDef file fill:#F1F1F1,stroke:#333,stroke-width:1px,color:black,stroke-dasharray: 5 5;

    subgraph Infrastructure ["Phase 1: Infrastructure (Terraform)"]
        direction TB
        TFCode[main.tf]:::tf
        TFApply(terraform apply):::tf
        
        TFCode --> TFApply
    end

    subgraph Cloud ["Phase 2: AWS Cloud Environment"]
        direction TB
        IAM((IAM Service)):::aws
        
        TFApply -->|Deploys| IAM
        
        %% The Vulnerabilities
        RoleA(Role: Stranger Danger)
        RoleB(Role: Confused Deputy)
        RoleC(Role: Admin Access)
        
        IAM -.->|Creates| RoleA
        IAM -.->|Creates| RoleB
        IAM -.->|Creates| RoleC
    end

    subgraph Engine ["Phase 3: The Engine (Python)"]
        direction TB
        Collector[collector.py]:::py
        Analyzer[analyzer.py]:::py
        Visualizer[visualizer.py]:::py
        
        RawData[findings.json]:::file
        
        %% Data Flow
        Collector -->|Boto3: GetAccountAuthorizationDetails| IAM
        IAM -->|JSON Response| Collector
        Collector -->|Raw Policy Data| Analyzer
        
        %% Logic
        Analyzer -->|Logic: Check ExternalID & * Principal| RawData
        RawData -->|Input| Visualizer
    end

    subgraph UI ["Phase 4: Presentation (HTML5)"]
        direction TB
        Report[report.html]:::html
        Browser(Web Browser):::html
        
        Visualizer -->|Generates with Tesla UI| Report
        Report -->|Auto-Open| Browser
    end
    
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









