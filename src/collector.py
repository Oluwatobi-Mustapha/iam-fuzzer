import boto3
from botocore.exceptions import ClientError
from analyzer import analyze_policy             

# We pass the profile_name in as an argument
def list_customer_policies(profile_name):
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

            # Reporting
            if findings:
             print(f"Alert! Found risks {findings}")
            else:
             print(f"No Risk")

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
        
        # Confirming if a user have inline policy
        # API: list_user_policies (This is different from list_policies!)
        inline_policies = iam.list_user_policies(UserName=username)['PolicyNames']
        
        if inline_policies:
            print(f"\nHIDDEN RISK: User '{username}' has inline policies: {inline_policies}")
        else:
            print(f"\nUser '{username}' is clean (no inline policies).")

# The execution block
if __name__ == '__main__':
    # We call the function with the specific STRING name of the profile
    list_customer_policies("target-prod")
    list_inline_policies("target-prod")