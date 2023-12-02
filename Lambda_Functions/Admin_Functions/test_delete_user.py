import pytest
from moto import mock_dynamodb
from delete_user import lambda_handler  
import boto3

#TO TEST:
#       no netID
#       invalid netID
#       successful deletion

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_no_netID(dynamodb_mock):
    response = lambda_handler({
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: netID is required to delete a user.' in response['body']

def test_invalid_netID(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'gyt87001'
    }, None)
    assert response['statusCode'] == 404
    assert 'Error: User with the provided netID does not exist.' in response['body']

def valid_deletion(dynamodb_mock):
    response = lambda_handler({
        'netID' : 'tbs20008'
    }, None)
    assert response['statusCode'] == 200
    assert 'User deleted successfully.' in response['body']    

if __name__ == "__main__":
    pytest.main()