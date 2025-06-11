from src.http_service import HTTPService
from src.singleton import Singleton
from src.cypher import AESCypher
from typing import Any
from pytest_mock import MockFixture

import pytest
import secrets
import binascii
import requests
import json

################################################################################
#                                                                              #
# Pytest Fixtures -> used to arrange tests                                     #
#                                                                              #
################################################################################

@pytest.fixture
def http_service() -> HTTPService:
    # Initialize variables
    url = 'https://example.com/webshell.php'
    key = secrets.token_bytes(32)
    nonce = binascii.hexlify(secrets.token_bytes(16)).decode()

    # Create and yield the instance
    http_service = HTTPService()
    http_service.initialize(url, key, nonce)
    yield http_service
    
    # Destroy the created instance to reset state
    delattr(HTTPService, 'instance')

################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_http_service_is_singleton(http_service: HTTPService) -> None:
    # Expect the instance to be a Singleton
    assert isinstance(http_service, Singleton)

def test_sends_encrypted_request(mocker: MockFixture) -> None:
    request = { 'action': 'execute_command', 'args': { 'cmd': 'ls -l' } }
    run_test_request_args_scenario(request, mocker)

def test_sends_encrypted_request_using_supplied_dict(mocker: MockFixture) -> None:
    request = { 'action': 'download_file', 'args': { 'filename': 'test.txt' } }
    run_test_request_args_scenario(request, mocker)

################################################################################
#                                                                              #
# Test scenarios to reduce test-case code duplication                          #
#                                                                              #
################################################################################

def run_test_request_args_scenario(request: dict[str, Any], mocker: MockFixture) -> None:
    # Create a mocked 'Session' object and mock requests.session to return it
    mock_session = mocker.MagicMock()
    mocker.patch('requests.session')
    requests.session.return_value = mock_session

    # Initialize variables
    url = 'https://example.com/webshell.php'
    key = secrets.token_bytes(32)
    nonce = binascii.hexlify(secrets.token_bytes(16)).decode()

    # Create and initialize the HTTPService
    http_service = HTTPService()
    http_service.initialize(url, key, nonce)

    # Use the HTTPService to send a request
    http_service.send_request(request)

    # Verify the HTTPService used the session to send the request
    mock_session.post.assert_called_once()
    args, kwargs = mock_session.post.call_args

    # Verify the request was sent to the correct URL
    assert len(args) == 1 and args[0] == url

    # Verify the payload is as expected
    cypher = http_service._HTTPService__cypher
    raw_body = cypher.decrypt(kwargs['json']['body'], kwargs['json']['iv'])
    body = json.loads(raw_body)

    assert body['action'] == request['action'] and body['args'] == request['args'] and body['nonce'] == nonce

    # Destroy the created instance to reset state
    delattr(HTTPService, 'instance')

################################################################################
#                                                                              #
# Helper functions and classes                                                 #
#                                                                              #
################################################################################
