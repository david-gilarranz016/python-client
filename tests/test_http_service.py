from src.http_service import HTTPService
from src.singleton import Singleton

import pytest
import secrets
import binascii

################################################################################
#                                                                              #
# Pytest Fixtures -> used to arrange tests                                     #
#                                                                              #
################################################################################

@pytest.fixture
def http_service() -> HTTPService:
    # Initialize variables
    key = secrets.token_bytes(32)
    iv = secrets.token_bytes(32)
    nonce = binascii.hexlify(secrets.token_bytes(16))

    # Create and yield the instance
    http_service = HTTPService()
    http_service.initialize(key, iv, nonce)
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


