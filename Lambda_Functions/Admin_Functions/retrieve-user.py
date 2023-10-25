import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('User_List')  
def lambda_handler(event, context):

    netID = event.get('netID') 
    
    if not id:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing ID field.')
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