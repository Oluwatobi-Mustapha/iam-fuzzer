## 🏗️ Architecture

```mermaid
flowchart TD
    %% Define Styles
    classDef tf fill:#7B42BC,stroke:#333,stroke-width:2px,color:white;
    classDef aws fill:#FF9900,stroke:#333,stroke-width:2px,color:white;
    classDef py fill:#3776AB,stroke:#333,stroke-width:2px,color:white;
    classDef html fill:#E34F26,stroke:#333,stroke-width:2px,color:white;
    classDef file fill:#F1F1F1,stroke:#333,stroke-width:1px,color:black,stroke-dasharray: 5 5;

    %% Phase 1
    subgraph Infrastructure ["Phase 1: Infrastructure (Terraform)"]
        direction TB
        TFCode[main.tf]:::tf
        TFApply(terraform apply):::tf
        TFCode --> TFApply
    end

    %% Phase 2
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

    %% Phase 3
    subgraph Engine ["Phase 3: The Engine (Python)"]
        direction TB
        Collector[collector.py]:::py
        Analyzer[analyzer.py]:::py
        Visualizer[visualizer.py]:::py
        
        RawData[findings.json]:::file
        
        %% Data Flow
        Collector -->|1. Boto3 API| IAM
        IAM -->|2. JSON Response| Collector
        Collector -->|3. Policy Data| Analyzer
        Analyzer -->|4. Risk Logic| RawData
        RawData -->|5. Input| Visualizer
    end

    %% Phase 4
    subgraph UI ["Phase 4: Presentation (HTML5)"]
        direction TB
        Report[report.html]:::html
        Browser(Web Browser):::html
        
        Visualizer -->|Generates| Report
        Report -->|Auto-Open| Browser
    end

    %% Connections between phases
    Infrastructure --> Cloud
    Cloud --> Engine
    Engine --> UI