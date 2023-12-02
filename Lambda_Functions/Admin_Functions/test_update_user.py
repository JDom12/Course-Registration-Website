import pytest
from moto import mock_dynamodb
from update_user import lambda_handler  
import boto3

#TO TEST:
#       no netID
#       successful update 1
#       successful update 2

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_no_netID(dynamodb_mock):
    response = lambda_handler({
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: netID is required for update operations.' in response['body']

def test_successful_1(dynamodb_mock):
    response = lambda_handler({
        "netID" : "tbs20008",
        "first_name" : "Trent",
        "Last_name" : "Miller"
    }, None)
    assert response['statusCode'] == 200
    assert 'User updated successfully.' in response['body']

def test_successful_2(dynamodb_mock):
    response = lambda_handler({
        "netID" : "tbs20008",
        "prior_courses" : "Introduction to Software Engineering, Introduction to Academic Writing"
    }, None)
    assert response['statusCode'] == 200
    assert 'User updated successfully.' in response['body']

if __name__ == "__main__":
    pytest.main()