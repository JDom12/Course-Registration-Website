import json
import boto3
from mock_dynamodb_setup import setup_dynamodb_user_list, setup_fall_semester_table

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    
    netID = event.get('netID')
    
    if not netID:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: netID is required.')
        }

    #find instructor info from netID   
    students_table = setup_dynamodb_user_list(dynamodb)  
    response = students_table.get_item(
        Key = {
            'netID' : netID 
        }     
    )
    
    instructor = response.get('Item')
    
    #return if nothing is found
    if not instructor:
        return{
            'statusCode' : 404,
            'body' : json.dumps('Error: invalid netID')
            
        }
    
    #construct full name from netID
    instructor_first =instructor.get('first_name')
    instructor_last = instructor.get('last_name')
    instructor_name = instructor_first + " " + instructor_last

    #scan by full name for classes being taught
    classes_table = setup_fall_semester_table(dynamodb)
    response = classes_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('instructor').eq(instructor_name)
    )

    items = response.get('Items', [])
    
    for item in items:
        item['max_enrollment'] = int(item['max_enrollment'])
        item['available_seats'] = int(item['available_seats'])

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
