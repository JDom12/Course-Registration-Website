import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('User_List')  

def lambda_handler(event, context):
    
    instructorid = event.get('instructorid')
    courseid = event.get('courseid')

    if not all([instructorid, courseid]):
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing required field.')
        }

    try:
        response = table.update_item(
            Key={
                'instructorid': instructorid
            },
            UpdateExpression='SET courses = list_append(courses, :c)',
            ExpressionAttributeValues={
                ':c': {
                    'L': [{'S': courseid}]
                }
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Course assigned successfully.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error assigning the course.')
        }