import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('User_List') # List name TBD

def lambda_handler(event, context):
    netID = event.get('netID')
    first_name = event.get('first_name')
    last_name = event.get('last_name')
    email = event.get('email')
    role = event.get('role')
    prior_courses = event.get('prior_courses')

    if not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: netID is required for update operations.')
        }

    update_expression = "SET"
    attribute_values = {}
    expression_attribute_names = {}
    if first_name:
        update_expression += " first_name = :first_name,"
        attribute_values[":first_name"] = first_name
    if last_name:
        update_expression += " last_name = :last_name,"
        attribute_values[":last_name"] = last_name
    if email:
        update_expression += " email = :email,"
        attribute_values[":email"] = email
    if role:
        update_expression += " #role_alias = :role," 
        attribute_values[":role"] = role
        expression_attribute_names["#role_alias"] = "role"
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
            ExpressionAttributeNames=expression_attribute_names
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