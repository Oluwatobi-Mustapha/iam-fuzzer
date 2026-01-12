# import boto3
# from botocore.exceptions import ClientError

# def list_customer_policies(profile_name):
#     profile = [
#         'target_prod'
#     ]

#     try:
#             # Create session for this profile
#             session = boto3.Session(profile_name=profile)

#             # Create an iam for the profile
#             iam = session.client('iam')

#             # The "Scope='Local'" part is the filter.
#             response = iam.list_policies(Scope='Local') 

#             for policy in policies:
#                  print(f"")





# if __name__ == '_main':
#     list_customer_policies()
