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