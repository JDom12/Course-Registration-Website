import boto3
import json
from mock_dynamodb_setup import setup_dynamodb_user_list

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = setup_dynamodb_user_list(dynamodb) 

    netID = event.get('netID')
    first_name = event.get('first_name')
    last_name = event.get('last_name')
    email = event.get('email')
    prior_courses = event.get('prior_courses')

    if not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: netID is required for update operations.')
        }

    update_expression = "SET"
    attribute_values = {}
    if first_name:
        update_expression += " first_name = :first_name,"
        attribute_values[":first_name"] = first_name
    if last_name:
        update_expression += " last_name = :last_name,"
        attribute_values[":last_name"] = last_name
    if email:
        update_expression += " email = :email,"
        attribute_values[":email"] = email
    if prior_courses:
        update_expression += " prior_courses = :prior_courses,"
        attribute_values[":prior_courses"] = prior_courses

    update_expression = update_expression.rstrip(',')

    try:
        response = table.update_item(
            Key={
                'netID': netID,
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=attribute_values,
            )
        return {
            'statusCode': 200,
            'body': json.dumps('User updated successfully.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error updating the user.')
        }