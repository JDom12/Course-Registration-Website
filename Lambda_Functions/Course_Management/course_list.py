import boto3
from boto3.dynamodb.conditions import Attr
import json
from mock_dynamodb_setup import setup_fall_semester_table


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = setup_fall_semester_table(dynamodb)
    
    search_tag = event.get('search_tags')
    instructor = event.get('instructor')
    available_seats = event.get('available_seats')
    class_name = event.get('class_name')
    class_id = event.get('class_id')
    pre_requisites = event.get('pre_requisites')

    try:
        
        # Initialize an empty filter 
        filter_expression = None

        # Add conditions if provided
        if search_tag:
            condition = Attr("search_tags").contains(search_tag)
            filter_expression = condition if filter_expression is None else filter_expression & condition

        if instructor:
            condition = Attr("instructor").eq(instructor)
            filter_expression = condition if filter_expression is None else filter_expression & condition

        if class_name:
            condition = Attr("class_name").contains(class_name)
            filter_expression = condition if filter_expression is None else filter_expression & condition

        if class_id:
            condition = Attr("class_id").contains(class_id)
            filter_expression = condition if filter_expression is None else filter_expression & condition
            
        if available_seats:
            condition = Attr("available_seats").gte(int(available_seats))
            filter_expression = condition if filter_expression is None else filter_expression & condition
        
        if pre_requisites:
            condition = Attr("pre_requisites").contains(pre_requisites)
            filter_expression = condition if filter_expression is None else filter_expression & condition
        
        # If no filter conditions are provided
        if filter_expression is None:
            return {
                'statusCode': 400,
                'body': json.dumps('Please enter a keyword to search.')
            }

        response = table.scan(
            FilterExpression=filter_expression
        )
       
        # If matches are found
        if response.get('Items'):
            items = response.get('Items')
            
            for item in items:
                item['max_enrollment'] = int(item['max_enrollment'])
                item['available_seats'] = int(item['available_seats'])
            
            return {
                'statusCode': 200,
                'body': json.dumps(items),
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            }
        return {
            'statusCode': 404,
            'body': json.dumps(f'No classes found')
        }
    
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving classes.')
        }