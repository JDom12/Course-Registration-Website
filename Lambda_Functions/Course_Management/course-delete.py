import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Classes')  #table name TBD

def lambda_handler(event, context):
    class_id = event.get('class_id')
    
    if not class_id:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing class_id.')
        }

    try:
        response = table.delete_item(
            Key={
                'class_id': class_id
            }
        )
        
        if response.get('Attributes'):
            return {
                'statusCode': 200,
                'body': json.dumps('Class deleted successfully.')
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Class not found.')
            }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error deleting the class.')
        }