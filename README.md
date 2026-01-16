## 🏗️ Architecture

```mermaid
flowchart LR
    %% GLOBAL STYLES
    classDef tf fill:#6A4495,stroke:#333,stroke-width:2px,color:white;
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:white;
    classDef py fill:#3776AB,stroke:#333,stroke-width:2px,color:white;
    classDef html fill:#E34F26,stroke:#333,stroke-width:2px,color:white;
    classDef data fill:#F1F1F1,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5,color:black;

    %% PHASE 1: INFRASTRUCTURE
    subgraph P1 [Phase 1: Infrastructure]
        direction TB
        TF[main.tf]:::tf
        CMD(terraform apply):::tf
        TF --> CMD
    end

    %% PHASE 2: CLOUD ENV
    subgraph P2 [Phase 2: AWS Cloud]
        direction TB
        IAM((IAM Service)):::aws
        
        %% Vulnerable Resources
        R1(Role: Stranger Danger):::aws
        R2(Role: Confused Deputy):::aws
        R3(Role: Admin Access):::aws
        
        IAM --- R1
        IAM --- R2
        IAM --- R3
    end

    %% PHASE 3: ENGINE
    subgraph P3 [Phase 3: The Engine]
        direction TB
        Col[collector.py]:::py
        Ana[analyzer.py]:::py
        
        %% Data Store
        JSON[(findings.json)]:::data
        
        Col -->|1. Fetch| Ana
        Ana -->|2. Logic| JSON
    end

    %% PHASE 4: UI
    subgraph P4 [Phase 4: Presentation]
        direction TB
        Viz[visualizer.py]:::py
        Rep[report.html]:::html
        Web(Browser):::html
        
        Viz -->|3. Generate| Rep
        Rep -->|4. View| Web
    end

    %% CONNECTIONS BETWEEN PHASES
    CMD ====================>|Deploys Resources| IAM
    IAM -.->|Boto3 API| Col
    JSON ==>|Input Data| Viz

    %% LINK STYLING
    linkStyle default stroke-width:2px,fill:none,stroke:#333;