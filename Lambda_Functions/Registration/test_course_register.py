import pytest
from moto import mock_dynamodb
from course_register import lambda_handler  
import boto3

# Test cases
# TO TEST:
#       Student or class not found
#       missing prereq
#       already enrolled
#       class is full
#       schedule conflict
#       successful register

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_unavailable_course_information(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'Introduction to Software Engineering',
        'netID': 'tbs20008'
    }, None)
    assert response['statusCode'] == 400
    assert 'Student or class not found' in response['body']

def test_missing_prereq(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'immunology',
        'netID': 'xyz12345'
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing prerequisite PHAR 1000' in response['body']

def test_already_enrolled(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'immunology',
        'netID': 'tbs20008'
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Student already registered.' in response['body']

def test_already_full(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'Peoples and Cultures of the World',
        'netID': 'tbs20008'
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Class is full.' in response['body']

def test_schedule_conflict(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'Introduction to American Studies',
        'netID': 'tbs20008'
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Class schedule conflicts with current courses.' in response['body']

def test_successful_register(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'Introduction to Computer Science',
        'netID': 'tbs20008'
    }, None)
    assert response['statusCode'] == 200
    assert 'Successfully registered for the class.' in response['body']

if __name__ == "__main__":
    pytest.main()
