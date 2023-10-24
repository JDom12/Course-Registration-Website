import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('User_List')

def lambda_handler(event, context):
    instructorid = event.get('instructorid')
    if not all([instructorid]) :
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing required field.')
        }
    try:
        response = table.get_item(
            Key= {
                'instructorid' : instructorid
            },
            ProjectExpression='schedule'
        )
        return {
            'statusCode' : 200,
            'body': json.dumps('Schedule found successfully.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error finding schedule.')
        }
