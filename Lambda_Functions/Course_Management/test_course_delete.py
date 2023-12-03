import pytest
from moto import mock_dynamodb
from course_delete import lambda_handler  
import boto3

#TO TEST:
#       missing class name
#       class not found
#       successful class deletion


@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_missing_class_name(dynamodb_mock):
    response = lambda_handler({
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing class name.' in response['body']

def test_class_not_found(dynamodb_mock):
    response = lambda_handler({
        'class_name' : 'Introduction to Software Engineering'
    }, None)
    assert response['statusCode'] == 404
    assert 'Class not found.' in response['body']   

def test_successful_deletion(dynamodb_mock):
    response = lambda_handler({
        'class_name' : 'immunology'
    }, None)
    assert response['statusCode'] == 200
    assert 'Class deleted successfully.' in response['body']     

if __name__ == "__main__":
    pytest.main()