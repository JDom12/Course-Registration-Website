import pytest
from moto import mock_dynamodb
from retrieve_user import lambda_handler  
import boto3

#TO TEST:
#       no netID
#       user not found
#       successful retrieval

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_no_netID(dynamodb_mock):
    response = lambda_handler({
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing netID field.' in response['body']

def test_user_not_found(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'gyt81001'
    }, None)
    assert response['statusCode'] == 404
    assert 'Error: User not found.' in response['body']

def test_successful_retrieval(dynamodb_mock): 
    response = lambda_handler({
        'netID' : 'tbs20008'
    }, None)
    assert response['statusCode'] == 200
    assert '{"netID": "tbs20008", "current_courses": ["immunology"], "email": "tren.stiller@uconn.edu", "first_name": "Tren", "last_name": "Stiller", "prior_courses": ["PHAR 1000"], "role": "student"}' in response['body']

if __name__ == "__main__":
    pytest.main()