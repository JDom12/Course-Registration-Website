import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Fall_Semester')  # table name tbd

def lambda_handler(event, context):
    class_name = event.get('class_name')

    if not class_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing class_name.')
        }

    try:
        response = table.get_item(
            Key={
                'class_name': class_name
            }
        )

        if 'Item' in response:
            item = response['Item']
            if 'max_enrollment' in item:
                item['max_enrollment'] = float(item['max_enrollment'])
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
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
            'body': json.dumps('Error retrieving the class information.')
        }