from pytest_mock import MockFixture
import secrets
import base64
import pytest

from src.cypher import AESCypher
from Crypto.Cipher import AES

###################################################################################
#                                                                                 #
# Test Cases                                                                      #
#                                                                                 #
###################################################################################

def test_uses_supplied_key_to_encrypt_messages(mocker: MockFixture) -> None:
    message = 'Secret message'
    run_encryption_test_scenario(message, mocker)

def test_uses_supplied_key_to_encrypt_different_message(mocker: MockFixture) -> None:
    message = 'Completely different test message'
    run_encryption_test_scenario(message, mocker)

###################################################################################
#                                                                                 #
# Test scenarios to avoid test-case code duplication                              #
#                                                                                 #
###################################################################################

def run_encryption_test_scenario(plaintext: str, mocker: MockFixture) -> None:
    # Initialize variables 
    key = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    base64_encoded_iv = base64.b64encode(iv).decode()
    encrypted_message = encrypt(plaintext, key, iv)

    # Mock secrets.token_bytes to return the same iv
    mocker.patch('secrets.token_bytes')
    secrets.token_bytes.return_value = iv

    # Create a cypher and use it to encrypt the message
    cypher = AESCypher(key)
    output = cypher.encrypt(plaintext)

    # Expect the cypher to produce the same encrypted message and return the same iv
    assert output['body'] == encrypted_message and output['iv'] == base64_encoded_iv

###################################################################################
#                                                                                 #
# Helper functions for test scenarios                                             #
#                                                                                 #
###################################################################################

# Helper function to encrypt text
def encrypt(plaintext: str, key: bytes, iv: bytes) -> str:
    body = pad(plaintext).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(body)).decode()

def pad(plaintext: str) -> str:
    # Adds PKCS#7 padding -> k - (l mod k) octects with value k - (l mod k)
    return plaintext + (16 - len(plaintext) % 16) * chr(16 - len(plaintext) % 16)
