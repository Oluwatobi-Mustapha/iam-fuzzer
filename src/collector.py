import boto3
from botocore.exceptions import ClientError

# We pass the profile_name in as an argument
def list_customer_policies(profile_name):
    try:
        # Create session 
        session = boto3.Session(profile_name=profile_name)

        # Create the IAM client 
        iam = session.client('iam')

        print(f"Scanning account using profile: {profile_name}...")

        # Get the list. Scope='Local' means "Only show policies I created"
        response = iam.list_policies(Scope='Local') 

        # Extract the list of policies from the messy JSON response
        policies = response['Policies']

        # Looping through them
        for policy in policies:
            print(f"Found Policy: {policy['PolicyName']}")
            print(f"Arn: {policy['Arn']}")

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
        # API: list_user_policies (This is ifferent from list_policies!)
        inline_policies = iam.list_user_policies(UserName=username)['PolicyNames']
        
        if inline_policies:
            print(f"  HIDDEN RISK: User '{username}' has inline policies: {inline_policies}")
        else:
            print(f"  User '{username}' is clean (no inline policies).")

# The execution block
if __name__ == '__main__':
    # We call the function with the specific STRING name of the profile
    list_customer_policies("target-prod")
    list_inline_policies("target-prod")