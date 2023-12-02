import boto3
import json
from mock_dynamodb_setup import setup_dynamodb_user_list, setup_fall_semester_table




def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    class_table = setup_fall_semester_table(dynamodb)

    class_name = event.get('class_name')
    netID = event.get('netID')

    if not class_name or not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing class name or netID.')
        }
    
    try:
        class_response = class_table.get_item(
            Key={
                'class_name': class_name
            }
        )

        if 'Item' not in class_response:
            return {
                'statusCode': 400,
                'body': json.dumps('Class not found.')
            }
        
        student_table = setup_dynamodb_user_list(dynamodb)
        
        student_response = student_table.get_item(
            Key={
                'netID' : netID
            }
        )
        
        roster = class_response['Item'].get('roster', [])
        current_courses = student_response['Item'].get('current_courses', [])
        available_seats = class_response['Item'].get('available_seats')

        if netID not in roster:
            return {
                'statusCode': 400,
                'body': json.dumps('Student is not registered for this course.')
            }
        
        
        # Remove the student's netID from the roster and class from current courses
        roster.remove(netID)
        current_courses.remove(class_name)
        available_seats += 1

        class_table = setup_fall_semester_table(dynamodb)


        update_class = class_table.update_item (
            Key={'class_name': class_name},
            UpdateExpression="SET roster = :r, available_seats = :as",
            ExpressionAttributeValues={
                ':r': roster,
                ':as': available_seats
            }
        )

        student_table = setup_dynamodb_user_list(dynamodb)
        
        update_student = student_table.update_item (
            Key={'netID' : netID},
            UpdateExpression = "SET current_courses = :current_courses",
            ExpressionAttributeValues={':current_courses': current_courses}
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully dropped from the course.')
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error dropping the course.')
        }