import boto3
import json
from mock_dynamodb_setup import setup_dynamodb_user_list

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = setup_dynamodb_user_list(dynamodb)

    netID = event.get('netID') 
    
    if not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing netID field.')
        }

   
    try:
        response = table.get_item(
            Key={
                'netID': netID
            }
        )

        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps('Error: User not found.')
            }


        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving the user.')
        }