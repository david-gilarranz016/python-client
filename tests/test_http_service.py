from src.http_service import HTTPService
from src.singleton import Singleton
from src.cypher import AESCypher
from typing import Any, Callable
from pytest_mock import MockFixture
from unittest.mock import MagicMock

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
    # Initialize the HTTPService instance with the default values and yield it
    initialize_http_service()
    yield HTTPService()

    # Restore the HTTPService instance to an uninitialized state
    reset_http_service()

@pytest.fixture
def mock_session(mocker: MockFixture) -> MagicMock:
    # Mock the requests module to use a mocked Session for our tests
    mock_session = mocker.MagicMock()
    mocker.patch('requests.session')
    requests.session.return_value = mock_session

    yield mock_session

################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_http_service_is_singleton(http_service: HTTPService) -> None:
    # Expect the instance to be a Singleton
    assert isinstance(http_service, Singleton)

def test_sends_encrypted_request(mock_session: MagicMock) -> None:
    request = { 'action': 'execute_command', 'args': { 'cmd': 'ls -l' } }
    run_test_request_args_scenario(request, mock_session)

def test_sends_encrypted_request_using_supplied_dict(mock_session: MagicMock) -> None:
    request = { 'action': 'download_file', 'args': { 'filename': 'test.txt' } }
    run_test_request_args_scenario(request, mock_session)

################################################################################
#                                                                              #
# Test scenarios to reduce test-case code duplication                          #
#                                                                              #
################################################################################

def run_test_request_args_scenario(request: dict[str, Any], mock_session: MagicMock) -> None:
    # Initialize http service
    url = 'https://example.com/webshell.php'
    nonce = binascii.hexlify(secrets.token_bytes(16)).decode()
    initialize_http_service(url = url, nonce = nonce)

    # Use the HTTPService to send a request
    http_service = HTTPService()
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

    reset_http_service()

################################################################################
#                                                                              #
# Helper functions and classes                                                 #
#                                                                              #
################################################################################

def initialize_http_service(
    url: str = 'https://example.com/webshell.php',
    key: bytes = secrets.token_bytes(32),
    nonce: str = binascii.hexlify(secrets.token_bytes(16)).decode()
) -> None:
    http_service = HTTPService()
    http_service.initialize(url, key, nonce)

def reset_http_service() -> None:
    # Destroy the created instance to reset state
    delattr(HTTPService, 'instance')

