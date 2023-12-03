import pytest
from moto import mock_dynamodb
from course_drop import lambda_handler  
import boto3

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_successful_course_drop(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'immunology',
        'netID': 'tbs20008'
    }, None)
    assert response['statusCode'] == 200
    assert 'Successfully dropped from the course' in response['body']

def test_course_not_found(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'Introduction to Software Engineering',
        'netID': 'tbs20008'
    }, None)
    assert response['statusCode'] == 400
    assert 'Class not found' in response['body']

def test_student_not_enrolled(dynamodb_mock):
    response = lambda_handler({
        'class_name': 'immunology',
        'netID': 'xyz12345'
    }, None)
    assert response['statusCode'] == 400
    assert 'Student is not registered for this course' in response['body']

def test_missing_information(dynamodb_mock): 
    response = lambda_handler({
        'class_name': 'English 2000',
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing class name or netID.' in response['body']


if __name__ == "__main__":
    pytest.main()