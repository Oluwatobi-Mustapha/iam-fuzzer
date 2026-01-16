import json
import os
import webbrowser
import time

def get_remediation(finding):
    name = finding['Name'].lower()
    risk_str = str(finding['Risks']).lower()
    
    # Default Structure
    remediation = {
        "action": ["Manual investigation required."],
        "link": "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"
    }

    # Scenario 1: Org Roles
    if "organizationaccountaccessrole" in name:
        remediation['action'] = [
            "<strong>Context:</strong> Default AWS Organization Role.",
            "<strong>Action:</strong> Verify Principal is Management Account.",
            "<strong>Note:</strong> Do NOT add ExternalId unless required."
        ]
        remediation['link'] = "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html"
        return remediation

    # Scenario 2: CI/CD
    if "terraform" in name or "github" in name or "jenkins" in name:
        remediation['action'] = [
            "<strong>Context:</strong> CI/CD Automation Role.",
            "<strong>Action:</strong> Lock Principal to Repo ARN or IP.",
            "<strong>Check:</strong> Enforce Least Privilege."
        ]
        remediation['link'] = "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html"
        return remediation

    # Scenario 3: Confused Deputy
    if "confused deputy" in risk_str:
        remediation['action'] = [
            "<strong>Risk:</strong> Cross-Account trust missing lock.",
            "<strong>Fix (Vendor):</strong> Add 'sts:ExternalId' condition.",
            "<strong>Fix (Internal):</strong> Add 'aws:SourceAccount' condition."
        ]
        remediation['link'] = "https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html"
        return remediation

    # Scenario 4: Public Access
    if "trusts everyone" in risk_str:
        remediation['action'] = [
            "<strong>CRITICAL:</strong> Remove '*' Principal.",
            "<strong>Fix:</strong> Replace with specific Account ID."
        ]
        remediation['link'] = "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html"
        return remediation

    # Scenario 5: Admin Access
    if "admin access" in risk_str:
        remediation['action'] = [
            "<strong>Violation:</strong> Excessive Permissions.",
            "<strong>Fix:</strong> Downgrade to 'PowerUserAccess'.",
            "<strong>Exception:</strong> Enable MFA if Break Glass."
        ]
        remediation['link'] = "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html"
        return remediation

    # Scenario 6: Privilege Escalation
    if "privilege escalation" in risk_str:
         remediation['action'] = [
            "<strong>Risk:</strong> User can create backdoors.",
            "<strong>Fix:</strong> Remove 'iam:CreateUser' permissions.",
            "<strong>Check:</strong> Audit CloudTrail logs."
        ]
         remediation['link'] = "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege"
         return remediation

    return remediation

def generate_report():
    input_file = 'findings.json'
    output_file = 'report.html'

    try:
        with open(input_file, 'r') as f:
            findings = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return

    # Metrics
    total_risks = len(findings)
    critical = sum(1 for f in findings if any("CRITICAL" in r for r in f['Risks']))
    high = sum(1 for f in findings if any("HIGH" in r for r in f['Risks']))
    scan_time = time.strftime("%b %d, %Y • %I:%M %p UTC")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IAM Security Report</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #ffffff;
                --surface: #f9f9f9;
                --text-main: #171a20; /* Tesla Black */
                --text-sub: #5c5e62;  /* Tesla Grey */
                --accent: #3e6ae1;    /* Tesla Blue */
                --danger: #e82127;    /* Tesla Red */
                --warning: #f49342;
                --border: #e2e2e2;
                --shadow: 0 4px 24px rgba(0,0,0,0.06);
            }}
            
            body {{
                font-family: 'Inter', sans-serif;
                background-color: var(--bg);
                color: var(--text-main);
                margin: 0;
                padding: 0;
                -webkit-font-smoothing: antialiased;
            }}

            /* HERO SECTION */
            .hero {{
                padding: 80px 40px 40px;
                text-align: center;
                background: linear-gradient(180deg, #fff 0%, #f4f4f4 100%);
            }}
            
            h1 {{
                font-weight: 600;
                font-size: 42px;
                letter-spacing: -0.5px;
                margin: 0 0 10px 0;
            }}
            
            .meta {{
                font-size: 14px;
                color: var(--text-sub);
                font-weight: 500;
                margin-bottom: 40px;
            }}

            /* METRICS - Clean, floating cards */
            .metrics-container {{
                display: flex;
                justify-content: center;
                gap: 40px;
                margin-bottom: 60px;
            }}
            
            .metric {{
                text-align: center;
            }}
            
            .metric .num {{
                font-size: 56px;
                font-weight: 600;
                line-height: 1;
                display: block;
                margin-bottom: 5px;
            }}
            
            .metric .label {{
                font-size: 13px;
                font-weight: 500;
                color: var(--text-sub);
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            /* CONTROLS */
            .controls {{
                max-width: 1200px;
                margin: 0 auto 30px;
                padding: 0 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            input {{
                background: var(--surface);
                border: 1px solid transparent;
                padding: 14px 20px;
                border-radius: 8px;
                width: 320px;
                font-size: 14px;
                color: var(--text-main);
                outline: none;
                transition: 0.2s;
            }}
            input:focus {{ background: #fff; border-color: var(--border); box-shadow: var(--shadow); }}
            
            .filters button {{
                background: transparent;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                color: var(--text-sub);
                cursor: pointer;
                transition: 0.2s;
                border-radius: 20px;
            }}
            .filters button:hover {{ color: var(--text-main); background: var(--surface); }}
            .filters button.active {{ background: var(--text-main); color: #fff; }}

            /* DATA TABLE */
            .container {{
                max-width: 1200px;
                margin: 0 auto 100px;
                padding: 0 40px;
            }}
            
            .card-list {{
                display: flex;
                flex-direction: column;
                gap: 16px;
            }}
            
            .risk-card {{
                background: #fff;
                border-radius: 16px;
                padding: 30px;
                box-shadow: var(--shadow);
                display: grid;
                grid-template-columns: 2fr 3fr 2fr;
                gap: 30px;
                align-items: start;
                transition: transform 0.2s, box-shadow 0.2s;
                border: 1px solid transparent;
            }}
            
            .risk-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.1);
            }}

            /* Resource Column */
            .res-type {{
                font-size: 12px;
                font-weight: 600;
                color: var(--text-sub);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 8px;
                display: block;
            }}
            .res-name {{
                font-size: 18px;
                font-weight: 600;
                color: var(--text-main);
                display: block;
                margin-bottom: 6px;
            }}
            .res-arn {{
                font-family: 'Inter', sans-serif; /* Monospace can look dirty, stick to Inter */
                font-size: 12px;
                color: var(--text-sub);
                background: var(--surface);
                padding: 4px 8px;
                border-radius: 6px;
                display: inline-block;
            }}
            .date-tag {{
                font-size: 11px;
                color: var(--text-sub);
                margin-top: 8px;
                display: block;
                font-weight: 500;
            }}

            /* Findings Column */
            .badge {{
                display: inline-flex;
                align-items: center;
                margin-bottom: 8px;
                font-size: 14px;
                font-weight: 500;
            }}
            .dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 10px;
            }}
            .crit .dot {{ background: var(--danger); box-shadow: 0 0 0 2px rgba(232, 33, 39, 0.2); }}
            .crit {{ color: var(--danger); }}
            .high .dot {{ background: var(--warning); }}
            .high {{ color: var(--warning); }}

            /* Action Column */
            .action-box ul {{
                margin: 0;
                padding: 0;
                list-style: none;
            }}
            .action-box li {{
                font-size: 13px;
                color: var(--text-sub);
                margin-bottom: 6px;
                line-height: 1.5;
            }}
            .action-box strong {{
                color: var(--text-main);
                font-weight: 600;
            }}
            .link-btn {{
                display: inline-block;
                margin-top: 15px;
                font-size: 13px;
                font-weight: 600;
                color: var(--accent);
                text-decoration: none;
                transition: 0.2s;
            }}
            .link-btn:hover {{ text-decoration: underline; }}
            
            /* Hidden State */
            .hidden {{ display: none; }}
        </style>
    </head>
    <body>

        <div class="hero">
            <h1>IAM Security Report</h1>
            <div class="meta">Generated {scan_time} • ID {int(time.time())}</div>
            
            <div class="metrics-container">
                <div class="metric">
                    <span class="num">{total_risks}</span>
                    <span class="label">Total Findings</span>
                </div>
                <div class="metric">
                    <span class="num" style="color: var(--danger)">{critical}</span>
                    <span class="label">Critical Risks</span>
                </div>
                <div class="metric">
                    <span class="num" style="color: var(--warning)">{high}</span>
                    <span class="label">High Priority</span>
                </div>
            </div>
        </div>

        <div class="controls">
            <input type="text" id="searchInput" placeholder="Search resources..." onkeyup="filterTable()">
            <div class="filters">
                <button class="active" onclick="filterRisk('all', this)">View All</button>
                <button onclick="filterRisk('CRITICAL', this)">Critical</button>
                <button onclick="filterRisk('HIGH', this)">High Priority</button>
            </div>
        </div>

        <div class="container">
            <div class="card-list" id="cardList">
    """

    for f in findings:
        # Badge Logic
        badges = ""
        risk_class = "all"
        for r in f['Risks']:
            clean_text = r.replace("CRITICAL:", "").replace("HIGH:", "").replace("WARNING:", "").strip()
            if "CRITICAL" in r: 
                badges += f'<div class="badge crit"><div class="dot"></div>{clean_text}</div>'
                risk_class += " CRITICAL"
            elif "HIGH" in r: 
                badges += f'<div class="badge high"><div class="dot"></div>{clean_text}</div>'
                risk_class += " HIGH"
            else:
                badges += f'<div class="badge high"><div class="dot"></div>{clean_text}</div>'

        # Remediation
        rem = get_remediation(f)
        steps = "".join([f"<li>{s}</li>" for s in rem['action']])
        date_str = f.get('Date', 'Unknown')

        html_content += f"""
            <div class="risk-card {risk_class}">
                <div>
                    <span class="res-type">{f['Type']}</span>
                    <span class="res-name">{f['Name']}</span>
                    <span class="res-arn">{f['ARN']}</span>
                    <span class="date-tag">Created {date_str}</span>
                </div>

                <div>
                    {badges}
                </div>

                <div class="action-box">
                    <ul>{steps}</ul>
                    <a href="{rem['link']}" target="_blank" class="link-btn">Read Documentation →</a>
                </div>
            </div>
        """

    html_content += """
            </div>
        </div>

        <script>
            function filterTable() {
                const input = document.getElementById("searchInput").value.toLowerCase();
                const cards = document.querySelectorAll(".risk-card");
                cards.forEach(card => {
                    const text = card.innerText.toLowerCase();
                    card.style.display = text.includes(input) ? "grid" : "none";
                });
            }

            function filterRisk(level, btn) {
                document.querySelectorAll("button").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                const cards = document.querySelectorAll(".risk-card");
                cards.forEach(card => {
                    if (level === 'all') card.style.display = "grid";
                    else card.style.display = card.classList.contains(level) ? "grid" : "none";
                });
            }
        </script>
    </body>
    </html>
    """

    with open(output_file, 'w') as f:
        f.write(html_content)

    print(f"✅ Dashboard generated: {os.path.abspath(output_file)}")
    url = 'file://' + os.path.abspath(output_file) + f"?t={time.time()}"
    webbrowser.open(url)

if __name__ == "__main__":
    generate_report()