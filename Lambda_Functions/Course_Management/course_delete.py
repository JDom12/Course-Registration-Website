import boto3
import json
from mock_dynamodb_setup import setup_fall_semester_table, setup_dynamodb_user_list


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = setup_fall_semester_table(dynamodb) 

    class_name = event.get('class_name')
    
    if not class_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing class name.')
        }

    try:
        # Get the class item to retrieve the roster
        class_item = table.get_item(Key={'class_name': class_name})
        if 'Item' not in class_item:
            return {
                'statusCode': 404,
                'body': json.dumps('Class not found.')
            }

        roster = class_item['Item'].get('roster', [])

        table_student = setup_dynamodb_user_list(dynamodb)

        # remove class from enrolled student's current_courses attribute
        for netID in roster:
            student = table_student.get_item(Key={'netID': netID})
            if 'Item' in student:
                current_courses = student['Item'].get('current_courses', [])
                if class_name in current_courses:
                    current_courses.remove(class_name)
                    table_student.update_item(
                        Key={'netID': netID},
                        UpdateExpression="set current_courses=:c",
                        ExpressionAttributeValues={
                            ':c': current_courses
                        }
                    )

        # delete course
        table = setup_fall_semester_table(dynamodb) 
        response = table.delete_item(Key={'class_name': class_name})
        return {
            'statusCode': 200,
            'body': json.dumps('Class deleted successfully.')
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error deleting the class.')
        }