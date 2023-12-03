import pytest
from moto import mock_dynamodb
from create_user import lambda_handler  
import boto3

#TO TEST:
#       Missing field 1
#       Missing field 2
#       user exists already
#       successful creation 1
#       successful creation 2

@pytest.fixture(scope="function")
def dynamodb_mock():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        yield dynamodb

def test_missing_field_1(dynamodb_mock):
    response = lambda_handler({
        'first_name': 'Ben',
        'last_name': 'Jamin',
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing required field.' in response['body']

def test_missing_field_2(dynamodb_mock):
    response = lambda_handler({
        'first_name': 'Ben',
        'last_name': 'Jamin',
        'email' : 'ben.jamin@uconn.edu',
        'role' : 'admin'
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: Missing required field.' in response['body']

def test_user_already_exists(dynamodb_mock):
    response = lambda_handler({
        'first_name': 'Tren',
        'last_name': 'Stiller',
        'email' : 'tren.stiller@uconn.edu',
        'role' : 'student',
        'netID' : 'tbs20008'
    }, None)
    assert response['statusCode'] == 400
    assert 'Error: netID already exists in the table.' in response['body']

def test_successful_1(dynamodb_mock):
    response = lambda_handler({
        'first_name': 'Ben',
        'last_name': 'Jamin',
        'email' : 'ben.jamin@uconn.edu',
        'role' : 'admin',
        'netID' : 'bnj12007'
    }, None)
    assert response['statusCode'] == 200
    assert 'User created successfully.' in response['body']

def test_successful_2(dynamodb_mock):
    response = lambda_handler({
        'first_name': 'Frank',
        'last_name': 'Lin',
        'email' : 'frank.linn@uconn.edu',
        'role' : 'professor',
        'netID' : 'fkl12007'
    }, None)
    assert response['statusCode'] == 200
    assert 'User created successfully.' in response['body']   



if __name__ == "__main__":
    pytest.main()