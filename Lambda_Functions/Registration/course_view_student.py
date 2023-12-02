import boto3
import json
from mock_dynamodb_setup import setup_dynamodb_user_list, setup_fall_semester_table




def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    students_table = setup_dynamodb_user_list(dynamodb)
    netID = event.get('netID')

    if not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Missing netID.')
        }

    try:
        response = students_table.get_item(
            Key={
                'netID' : netID
            }
        )
        student = response.get('Item')

        if not student:
            return {
                'statusCode': 400,
                'body': 'Error: Student not found.'
            }
       
        # If matches are found
        if student:
            retrieved_classes = []
            registered_classes = student.get('current_courses') 

            classes_table = setup_fall_semester_table(dynamodb)

            # fetch class information from Fall_Semester table
            for course in registered_classes: 
                response = classes_table.get_item(
                        Key={
                            'class_name' : course
                        }
                    )
                retrieved_classes.append(response.get('Item'))
                
            for item in retrieved_classes:
                item['max_enrollment'] = int(item['max_enrollment'])
                item['available_seats'] = int(item['available_seats'])
            
            return {
                'statusCode': 200,
                'body': json.dumps(retrieved_classes),
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
                    'Access-Control-Allow-Headers': 'Content-Type'
                    }
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps(f'No classes found for netID: {netID}.')
            }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving the registered classes.')
        }