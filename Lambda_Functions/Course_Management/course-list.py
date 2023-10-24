#WIP

import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Fall_Semester')

def lambda_handler(event, context):
    
    search_tags = event.get('search_tags')
    
    response = table.scan(ProjectionExpression = "search_tags")
    
    items = response['Items']
    
    for item in items:
        for tag in search_tags:
            break
        
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }