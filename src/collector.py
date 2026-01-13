import boto3
import json # This allows us to speak File lanaguage
from botocore.exceptions import ClientError
from analyzer import analyze_policy             

# Global lines to store findings
findings_list = []
# We pass the profile_name in as an argument
def list_customer_policies(profile_name): # Managed policy
    try:
        # Create session 
        session = boto3.Session(profile_name=profile_name)

        # Create the IAM client 
        iam = session.client('iam')

        print(f"\nScanning account using profile: {profile_name}...")

        # Get the list. Scope='Local' means "Only show policies I created"
        response = iam.list_policies(Scope='Local') 

        # Extract the list of policies from the bogus JSON response
        policies = response['Policies']

        # Looping through them
        for policy in policies:
            print(f"\nFound Policy: {policy['PolicyName']}")
            print(f"\nArn: {policy['Arn']}")

            # Everything below is INDENTED to stay INSIDE the loop

            # Get the Policy Version(For example, v1, v2, etc.)
            version_id = policy['DefaultVersionId']

            # Fetch the full JSON body details. VersionId (CamelCase according to Official Boto3 Doc.)
            version_details = iam.get_policy_version(PolicyArn = policy['Arn'], VersionId = version_id)

            # Extract details needed from the JSON document fetched
            policy_document = version_details['PolicyVersion']['Document']

            # Run the analyzer
            findings = analyze_policy(policy_document)

            # Reporting and storing
            if findings:
                print(f"\nAlert! Founds risks {findings} in {policy['PolicyName']}")

                # Creating a dictionary for this specific finding
                finding_data = {
                    "Type": "Managed Policy",
                    "Name": policy['PolicyName'],
                    "ARN" : policy['Arn'],
                    "Risks": findings
                }
                # Adding it to the final bucket
                findings_list.append(finding_data)
            else:
                print(f"\nNo risk!")
            
    except ClientError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def list_inline_policies(profile_name):
    session = boto3.Session(profile_name=profile_name)
    iam = session.client('iam')

    print(f"\nScanning USERS for hidden Inline Policies in {profile_name}...")
    
    # Get every user in the account
    users = iam.list_users()['Users']
    
    for user in users:
        username = user['UserName']
        
        # Get the list of inline policy NAMES
        policy_names = iam.list_user_policies(UserName=username)['PolicyNames']
        
        if not policy_names:
            print(f"\nUser '{username}' has no inline policies.")

            continue

        for policy_name in policy_names:

            # Fetch the actual Policy Document (JSON)
            response = iam.get_user_policy(
                UserName=username, 
                PolicyName=policy_name
            )
            policy_document = response['PolicyDocument']
            
            # Analyze it from my analyzer.py
            findings = analyze_policy(policy_document)
            
            # Report based on Real risks findings
            if findings:
                print(f"HIDDEN RISK! User: '{username}' - Policy '{policy_name}': {findings}\n")

                # Create the dictionary
                finding_data = {
                    "Type": "Inline Policy",
                    "Name": f"{username} - {policy_name}",
                    "ARN" : "N/A",
                    "Risks": findings
                }

                # Add to the Master Bucket
                findings_list.append(finding_data)
            else:
                print(f"User '{username}' - Policy '{policy_name}' is safe.\n")
def save_findings():
    """Writes the the findings_list into a JSON file"""
    print(f"\n Saving results to findings.json...")

    #  Context Manager A.K.A 'with'; guarantee that file closed properly
    #  Open or create a new file called 'findings.json' in 'write' mode ('w')
    #  And temporary handle (variable) named f representing the open file; open door to the file

    with open('findings.json', 'w') as f: 

        # Dump the python list into the file as JSON text
        json.dump(findings_list, f, indent=4)
        print(f"\nFile saved successfully!")
# The execution block
if __name__ == '__main__':
    # We call the function with the specific STRING name of the profile
    list_customer_policies("target-prod")
    list_inline_policies("target-prod")
    save_findings()