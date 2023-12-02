import pytest
from moto import mock_dynamodb
from course_update import lambda_handler  
import boto3

#TO TEST:
#       missing class name
#       class does not exist
#       successful update 1
#       successful update 2

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_no_class_name(dynamodb_mock):
    response = lambda_handler({
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: class_name is required.' in response['body']


def test_invalid_class(dynamodb_mock):
    response = lambda_handler({
        'class_name' : 'Introduction to Software Engineering'
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: No class found with class_name: Introduction to Software Engineering' in response['body']


def test_successful_1(dynamodb_mock):
    response = lambda_handler({
        'class_name' : 'immunology',
        'instructor' : 'Trent Drugsbad'
    }, None)
    assert response['statusCode'] == 200
    assert 'Class immunology updated successfully.' in response['body']

def test_successful_2(dynamodb_mock):
    response = lambda_handler({
        'class_name' : 'immunology',
        'room' : 'ITE 118',
        'meeting_time' : 'T / TH 2:00 - 3:00'
    }, None)
    assert response['statusCode'] == 200
    assert 'Class immunology updated successfully.' in response['body']


if __name__ == "__main__":
    pytest.main()
