import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Fall_Semester')  # table name tbd

def lambda_handler(event, context):
    class_id = event.get('class_id')
    netID = event.get('netID')

    if not class_id or not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing class_id or netID.')
        }

    try:
        response = table.get_item(
            Key={
                'class_id': class_id
            }
        )

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps('Class not found.')
            }
        
        roster = response['Item'].get('roster', [])

        if netID not in roster:
            return {
                'statusCode': 400,
                'body': json.dumps('Student is not registered for this course.')
            }
        
        # Remove the student's netID from the roster
        roster.remove(netID)

        update_response = table.update_item(
            Key={'class_id': class_id},
            UpdateExpression="SET roster = :roster",
            ExpressionAttributeValues={':roster': roster}
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully dropped from the course.')
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error dropping the course.')
        }