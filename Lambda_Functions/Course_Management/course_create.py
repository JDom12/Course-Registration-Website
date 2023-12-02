import boto3
import json
from mock_dynamodb_setup import setup_fall_semester_table




def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = setup_fall_semester_table(dynamodb)

    class_id = event.get('class_id')
    class_name = event.get('class_name')
    instructor = event.get('instructor')
    room = event.get('room')  
    meeting_time = event.get('meeting_time')
    pre_requisites = event.get('pre_requisites', [])  
    search_tags = event.get('search_tags')  
    max_enrollment = event.get('max_enrollment')
 
    roster = []


    if not all([class_id, class_name, instructor, room, meeting_time, max_enrollment]):
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing required field.')
        }
    
    available_seats = max_enrollment

    if isinstance(room, str):
        room = [room]
    if isinstance(search_tags, str):
        search_tags = [search_tags]
    if isinstance(pre_requisites, str):
        pre_requisites = [pre_requisites]

    try:
        response = table.put_item(
            Item={
                'class_id': class_id,
                'class_name': class_name,
                'instructor': instructor,
                'room': room,
                'meeting_time': meeting_time,
                'pre_requisites': pre_requisites,
                'search_tags': search_tags,
                'max_enrollment': max_enrollment,
                'roster': roster,
                'available_seats' : available_seats
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Class created successfully.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error creating the class.')
        }
