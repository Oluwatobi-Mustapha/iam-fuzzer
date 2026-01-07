import boto3
from botocore.exceptions import ClientError, ProfileNotFound

def verify_profiles():
    # The list of profiles I configured in my architecture
    profiles = [
        'fuzzer-admin',
        'target-prod',
        'target-dev',
        'audit-logs',
        'sandbox'
    ]
    print(f"\nStarting Connectivity Checks for {len(profiles)} profiles...")

    for profile in profiles:
        try:
            # Create session for this profile
            session = boto3.Session(profile_name=profile)

            # Create an STS(Security Token Service) for the profile
            sts = session.client("sts")

            # Calling the function that asks AWS "Who am I?"
            identity = sts.get_caller_identity()
            account_id = identity['Account']
            print(f"[PASS] {profile:<15} connected to account id: {account_id}")
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            print(f"[FAIL] {profile:<15} AWS client error {e}")
        except ProfileNotFound:
            print(f"[FAIL]{profile:<15}: Profile name not in ~./aws credentials")
        except Exception as e:
            print(f"[FAIL] {profile:<15} Unexpected error {e}")
    print("\n Connectivity Check Complete!")

if __name__ == '__main__':
    verify_profiles()



