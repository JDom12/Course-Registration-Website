import boto3
import json

dynamodb = boto3.resource('dynamodb')
classes_table = dynamodb.Table('Fall_Classes')
students_table = dynamodb.Table('User_List')

def lambda_handler(event, context):
    student_netID = event.get('netID')
    class_id = event.get('class_id')

    student_response = students_table.get_item(
        Key={
            'netID': student_netID
        }
    )
    student = student_response.get('Item')

    class_response = classes_table.get_item(
        Key={
            'class_id': class_id
        }
    )
    course = class_response.get('Item')

    if not student or not course:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Student or class not found.')
        }

    student_courses = student.get('prior_courses', [])
    course_prerequisites = course.get('pre-requisites', [])

    for prereq in course_prerequisites:
        if prereq not in student_courses:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Error: Missing prerequisite {prereq}.')
            }

    roster = course.get('roster', [])
    max_enrollment = course.get('max_enrollment', 100)  

    if student_netID in roster:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Student already registered.')
        }

    if len(roster) >= max_enrollment:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Class is full.')
        }

    roster.append(student_netID)
    update_response = classes_table.update_item(
        Key={
            'class_id': class_id
        },
        UpdateExpression="SET roster = :r",
        ExpressionAttributeValues={
            ':r': roster
        }
    )

    if update_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully registered for the class.')
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Error registering for the class.')
        }