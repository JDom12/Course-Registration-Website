import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Classes')  # table name tbd

def lambda_handler(event, context):
    netID = event.get('netID')

    if not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing netID.')
        }

    try:
        response = table.scan(
            FilterExpression="contains(roster, :netID)",
            ExpressionAttributeValues={":netID": netID}
        )

        # If matches are found
        if response.get('Items'):
            registered_classes = [item['class_name'] for item in response['Items']]
            return {
                'statusCode': 200,
                'body': json.dumps(registered_classes)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('No classes found for this netID.')
            }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving the registered classes.')
        }