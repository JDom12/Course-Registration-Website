import pytest
from moto import mock_dynamodb
from course_create import lambda_handler  
import boto3

#TO TEST:
#       missing data 1
#       missing data 2
#       successful class creation


@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_missing_data_1(dynamodb_mock):
    response = lambda_handler({
        "class_id": "FREN 1101",
        "class_name": "Elementary French I",
        "instructor": "Napoleon Bonaparte",
        "room": "Gentry 203",
        "pre_requisites": "",
        "search_tags": "FREN",
        "max_enrollment": 60
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing required field.' in response['body']

def test_missing_data_2(dynamodb_mock):
    response = lambda_handler({
        "class_id": "FREN 1101",
        "class_name": "Elementary French I",
        "meeting_time" : "M / W / F 4-5"
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing required field.' in response['body']

def test_successful_creation(dynamodb_mock):
    response = lambda_handler({
        "class_id": "FREN 1101",
        "class_name": "Elementary French I",
        "instructor": "Napoleon Bonaparte",
        "room": "Gentry 203",
        "meeting_time" : "M / W / F 4:00-5:00",
        "pre_requisites": "",
        "search_tags": "FREN",
        "max_enrollment": 60
    }, None)
    assert response['statusCode'] == 200
    assert 'Class created successfully.' in response['body']

if __name__ == "__main__":
    pytest.main()