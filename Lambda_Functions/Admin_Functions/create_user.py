
import boto3
import json
from mock_dynamodb_setup import setup_dynamodb_user_list

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = setup_dynamodb_user_list(dynamodb)  
    
    first_name = event.get('first_name')
    last_name = event.get('last_name')
    netID = event.get('netID')  
    email = event.get('email')
    role = event.get('role')

    if not all([first_name, last_name, netID, email, role]):
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing required field.')
        }

    # Check if netID already exists in the table
    try:
        response = table.get_item(Key={'netID': netID})
        if 'Item' in response:
            return {
                'statusCode': 400,
                'body': json.dumps('Error: netID already exists in the table.')
            }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error checking for existing netID.')
        }

    # Determine the item based on the role
    if role == "student":
        item = {
            'netID': netID,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'role': role,
            'prior_courses': [],
            'current_courses' : []
        }
    else:
        item = {
            'netID': netID,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'role': role
        }

    try:
        response = table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps('User created successfully.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error creating the user.')
        }
