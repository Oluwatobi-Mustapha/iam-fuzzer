def analyze_policy(policy_json):
    findings = []
    statements = policy_json.get('Statement', [])
    if isinstance(statements, dict):
        statements = [statements]

    for stmt in statements:
        effect = stmt.get('Effect', '')
        if effect != 'Allow':
            continue
            
        action = stmt.get('Action', [])
        resource = stmt.get('Resource', [])
        
        # Normalize Action
        if isinstance(action, str):
            action = [action]
            
        # Normalize Resource
        if isinstance(resource, str):
            resource = [resource]
            
        # Check for Admin Access
        if "*" in action and "*" in resource:
            findings.append("RISK_ADMIN_ACCESS")
    return findings
    
if __name__ == "__main__":
    # A mock policy to verify the logic locally without needing AWS
    bad_policy = {
        "Version": "2012-10-17",
        "Statement": [{ "Effect": "Allow", "Action": "*", "Resource": "*" }]
    }
    
    result = analyze_policy(bad_policy)
    print(result)
