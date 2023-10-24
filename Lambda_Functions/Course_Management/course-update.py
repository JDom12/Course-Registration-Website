import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Fall_Semester')  # table name 

def lambda_handler(event, context):
    class_name = event.get('class_name')
    
    if not class_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: class_name is required.')
        }

    try:
        response = table.get_item(
            Key={
                'class_name': class_name
            }
        )
        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps(f'Error: No class found with class_name: {class_name}.')
            }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error fetching the class.')
        }

    update_expression = 'SET '
    attribute_values = {}
    for key, value in event.items():
        if key != 'class_name' and value is not None:  
            update_expression += f"{key} = :{key}, "
            attribute_values[f":{key}"] = value
    update_expression = update_expression.rstrip(', ')

    try:
        table.update_item(
            Key={
                'class_name': class_name
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=attribute_values
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f'Class {class_name} updated successfully.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error updating the class.')
        }