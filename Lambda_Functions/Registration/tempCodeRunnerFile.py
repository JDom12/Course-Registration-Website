import pytest
import json
from moto import mock_dynamodb
import boto3
from course_drop import lambda_handler
import os


os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

@mock_dynamodb
def setup_dynamodb_user_list():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # table schema
    table = dynamodb.create_table(
        TableName='User_List',
        KeySchema=[
            {
                'AttributeName': 'netID',
                'KeyType': 'HASH'  
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'netID',
                'AttributeType': 'S'  
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName='User_List')

    # Add sample data to the table
    sample_users = [
        {
            'netID': 'tbs2008',
            'current_courses': ['Immunology'],
            'email': 'tren.stiller@uconn.edu',
            'first_name': 'Tren',
            'last_name': 'Stiller',
            'prior_courses': ['PHAR 1000'],
            'role': 'student'
        },
        {
            'netID': 'abc12345',
            'current_courses': ['Introduction to Computer Science'],
            'email': 'john.doe@uconn.edu',
            'first_name': 'John',
            'last_name': 'Doe',
            'prior_courses': ['Introductory Astronomy'],
            'role': 'student'
        }
    ]

    for user in sample_users:
        table.put_item(Item=user)

    return table

def setup_fall_semester_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # table schema
    table = dynamodb.create_table(
        TableName='Fall_Semester',
        KeySchema=[
            {
                'AttributeName': 'class_name',
                'KeyType': 'HASH'  
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'class_name',
                'AttributeType': 'S'  
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName='Fall_Semester')

    sample_classes = [
        {
            'class_name': 'Cellular Biology',
            'available_seats': 19,
            'class_id': 'PHAR 3000',
            'instructor': 'Tom Hanks',
            'max_enrollment': 20,
            'meeting_time': 'M / W / F 2:30-3:20',
            'pre_requisites': ['PHAR 1000'],
            'room': 'Room 101',
            'roster': ['tbs20008'],
            'search_tags': ['PHAR']
        },
        {
            'class_name': 'Introduction to Computer Science',
            'available_seats': 49,
            'class_id': 'CSE 1010',
            'instructor': 'Sandra Bullock',
            'max_enrollment': 50,
            'meeting_time': 'F 1 - 1:50',
            'pre_requisites': [],
            'room': ['Engineering II 302'],
            'roster': ['xyz12345'],
            'search_tags': ['CSE']
        },
        {
            'class_name': 'Peoples and Cultures of the World',
            'available_seats': 0,
            'class_id': 'ANTH 1010',
            'instructor': 'Jen Filler',
            'max_enrollment': 200,
            'meeting_time': 'M / W / F 2:30-3:20',
            'pre_requisites': [],
            'room': ['SU 845'],
            'roster': [],
            'search_tags': ['ANTH']
        }
    ]

    for class_info in sample_classes:
        table.put_item(Item=class_info)

    return table


setup_fall_semester_table()
setup_dynamodb_user_list()