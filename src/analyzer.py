import json

def analyze_policy(policy_json):
    findings = []
    
    # Safety Check: Handle empty inputs or strings
    if not policy_json or isinstance(policy_json, str):
        return []

    # GET THE STATEMENTS
    # We use .get() to avoid crashing if 'Statement' is missing entirely
    statements = policy_json.get('Statement', [])
    
    # NORMALIZE (The Fix)
    # If it's a single dictionary, wrap it in a list [ ] so we can loop over it safely.
    if isinstance(statements, dict):
        statements = [statements]

    # Now we can start the loop safely
    for stmt in statements:
        # Default to 'Allow' if missing (AWS defaults to Deny, but we only hunt Allows)
        effect = stmt.get('Effect', 'Allow') 
        
        if effect != 'Allow':
            continue
            
        # Extract the key ingredients for our checks
        action = stmt.get('Action', [])
        resource = stmt.get('Resource', [])
        principal = stmt.get('Principal', None) # Crucial for Trust Policies
        condition = stmt.get('Condition', {})

        # Block 2: TRUST POLICY LOGIC (Who can assume this?) 
        if principal:       
            
            # Check 1: (Principal: *)
            # This means anyone with an AWS account can assume this role.
            # It can appear as "Principal": "*" or "Principal": { "AWS": "*" }
            if principal == '*' or (isinstance(principal, dict) 
                                    and principal.get('AWS') == '*'):
                findings.append("CRITICAL: Role trusts everyone (Principal: *)")
                continue # We found the worst risk, stop checking this statement.

            # Check 2: Stranger Danger & Confused Deputy
            # We need to look inside the "AWS" key to see exactly WHICH accounts are trusted.
            if isinstance(principal, dict) and 'AWS' in principal:
                trusted_entities = principal['AWS']
                
                # If trusted_entities is just a single string, we wrap it in brackets [] to make it a list.
                if isinstance(trusted_entities, str):
                    trusted_entities = [trusted_entities]

                for entity_arn in trusted_entities:
                    # Logic: We only care about Account ARNs, not Services (like ec2.amazonaws.com)
                    if "arn:aws:iam::" in entity_arn:
                        
                        # The confused deputy check 
                        # If you trust an external account, you MUST check for 'sts:ExternalId' in the Condition.
                        # We convert the condition dict to a string for a quick search.
                        if "sts:ExternalId" not in str(condition):
                            findings.append(f"HIGH: Confused Deputy Risk! Trusting {entity_arn} without ExternalId.")
                        else:
                            # It has the secret, but we still flag it so you know the door exists.
                            findings.append(f"WARNING: Cross-Account Trust detected to {entity_arn}")
            
                # BLOCK 3: PERMISSION POLICY LOGIC (What can this do?)
        else:
            # 1. Normalize Action/Resource to lists
            if isinstance(action, str): 
                action = [action]
            if isinstance(resource, str): 
                resource = [resource]

            # 2. Admin Access Check (The "God Mode" Check)
            # If Action is "*" AND Resource is "*", they are an Admin.
            if ("*" in action) and ("*" in resource):
                findings.append("CRITICAL: Admin Access (Action: *)")

            # 3. Privilege Escalation Check (The "Backdoor" Check)
            # If they can create new users, they can create an Admin for themselves.
            if "iam:CreateUser" in action:
                findings.append("HIGH: Potential Privilege Escalation (iam:CreateUser)")

    return findings