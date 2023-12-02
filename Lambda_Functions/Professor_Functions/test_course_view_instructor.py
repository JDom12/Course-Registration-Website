import pytest
from moto import mock_dynamodb
from course_view_instructor import lambda_handler  
import boto3

#TO TEST
#       no netID
#       invalid netID
#       success 1
#       success 2

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_no_netID(dynamodb_mock):
    response = lambda_handler({
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: netID is required.' in response['body']

def test_invalid_netID(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'gyt19001'
    }, None)
    assert response['statusCode'] == 404
    assert 'Error: invalid netID' in response['body']

def test_successful_1(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'tmh20000'
    }, None)
    assert response['statusCode'] == 200
    assert '[{"class_name": "immunology", "available_seats": 19, "class_id": "PHAR 3000", "instructor": "Tom Hanks", "max_enrollment": 20, "meeting_time": "M / W / F 2:30-3:20", "pre_requisites": ["PHAR 1000"], "room": "Room 101", "roster": ["tbs20008"], "search_tags": ["PHAR"]}]' in response['body']

def test_successful_2(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'sab19000'
    }, None)
    assert response['statusCode'] == 200
    assert '[{"class_name": "Introduction to Computer Science", "available_seats": 49, "class_id": "CSE 1010", "instructor": "Sandra Bullock", "max_enrollment": 50, "meeting_time": "F 1:00 - 1:50", "pre_requisites": [], "room": ["Engineering II 302"], "roster": ["xyz12345"], "search_tags": ["CSE"]}]' in response['body']

if __name__ == "__main__":
    pytest.main()