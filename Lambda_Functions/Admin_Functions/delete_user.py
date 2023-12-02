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
            'body': json.dumps('Error: netID is required to delete a user.')
        }

    try:
        response = table.get_item(
            Key={
                'netID': netID
            }
        )

        # If the item does not exist, return an error response
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps('Error: User with the provided netID does not exist.')
            }

        # If the item exists, proceed to delete
        table.delete_item(
            Key={
                'netID': netID
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('User deleted successfully.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error deleting the user.')
        }