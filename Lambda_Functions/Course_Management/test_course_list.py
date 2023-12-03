import pytest
from moto import mock_dynamodb
from course_list import lambda_handler  
import boto3

#TO TEST:
#       no filters
#       no classes found
#       successful retrieval 1
#       successful retrieval 2


@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_missing_filter(dynamodb_mock):
    response = lambda_handler({
    }, None)
    assert response['statusCode'] == 400
    assert 'Please enter a keyword to search.' in response['body']

def test_no_classes(dynamodb_mock):
    response = lambda_handler({
        "instructor" : "Flint Drugswell"
    }, None)
    assert response['statusCode'] == 404
    assert 'No classes found' in response['body']

def test_successful_1_input(dynamodb_mock):
    response = lambda_handler({
        "instructor" : "Tom Hanks"
    }, None)
    assert response['statusCode'] == 200
    assert '[{"class_name": "immunology", "available_seats": 19, "class_id": "PHAR 3000", "instructor": "Tom Hanks", "max_enrollment": 20, "meeting_time": "M / W / F 2:30-3:20", "pre_requisites": ["PHAR 1000"], "room": "Room 101", "roster": ["tbs20008"], "search_tags": ["PHAR"]}]' in response['body']

def test_successful_2_input(dynamodb_mock):
    response = lambda_handler({
        "instructor" : "Tom Hanks",
        "search_tags" : "PHAR"
    }, None)
    assert response['statusCode'] == 200
    assert '[{"class_name": "immunology", "available_seats": 19, "class_id": "PHAR 3000", "instructor": "Tom Hanks", "max_enrollment": 20, "meeting_time": "M / W / F 2:30-3:20", "pre_requisites": ["PHAR 1000"], "room": "Room 101", "roster": ["tbs20008"], "search_tags": ["PHAR"]}]' in response['body']

def test_successful_multiple_returns(dynamodb_mock):
    response = lambda_handler({
        "available_seats" : 45
    }, None)
    assert response['statusCode'] == 200
    assert '[{"class_name": "Introduction to Computer Science", "available_seats": 49, "class_id": "CSE 1010", "instructor": "Sandra Bullock", "max_enrollment": 50, "meeting_time": "F 1:00 - 1:50", "pre_requisites": [], "room": ["Engineering II 302"], "roster": ["xyz12345"], "search_tags": ["CSE"]}, {"class_name": "Introduction to American Studies", "available_seats": 75, "class_id": "ENG 1201", "instructor": "William Shakespeare", "max_enrollment": 75, "meeting_time": "M / W / F 2:00 - 3:00", "pre_requisites": [], "room": ["BOUS 101"], "roster": [], "search_tags": ["ENG"]}]' in response['body']

if __name__ == "__main__":
    pytest.main()