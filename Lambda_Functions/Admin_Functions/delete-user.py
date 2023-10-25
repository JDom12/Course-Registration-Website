import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('User_List')

def lambda_handler(event, context):
    netID = event.get('netID')

    if not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: netID is required to delete a user.')
        }

    try:
        response = table.delete_item(
            Key={
                'netID': netID,
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