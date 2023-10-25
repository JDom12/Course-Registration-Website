
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Student_List')  

def lambda_handler(event, context):
    
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

    try:
        response = table.put_item(
            Item={
                'netID': netID,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'role': role
            }
        )
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
