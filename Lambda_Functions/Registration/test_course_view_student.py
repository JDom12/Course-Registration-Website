import pytest
from moto import mock_dynamodb
from course_view_student import lambda_handler  
import boto3

# Test cases
# TO TEST:
#       missing netID
#       invalid netID
#       succcesful retrieval 1
#       succcesful retrieval 2

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_missing_netID(dynamodb_mock):
    response = lambda_handler({
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing netID.' in response['body']

def test_invalid_netID(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'yip13008'
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Student not found' in response['body']

def test_valid_retrieval_1(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'tbs20008'
    }, None)
    assert response['statusCode'] == 200
    assert '[{"class_name": "immunology", "available_seats": 19, "class_id": "PHAR 3000", "instructor": "Tom Hanks", "max_enrollment": 20, "meeting_time": "M / W / F 2:30-3:20", "pre_requisites": ["PHAR 1000"], "room": "Room 101", "roster": ["tbs20008"], "search_tags": ["PHAR"]}]' in response['body']

def test_valid_retrieval_2(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'xyz12345'
    }, None)
    assert response['statusCode'] == 200
    assert '[{"class_name": "Introduction to Computer Science", "available_seats": 49, "class_id": "CSE 1010", "instructor": "Sandra Bullock", "max_enrollment": 50, "meeting_time": "F 1:00 - 1:50", "pre_requisites": [], "room": ["Engineering II 302"], "roster": ["xyz12345"], "search_tags": ["CSE"]}]' in response['body']


if __name__ == "__main__":
    pytest.main()