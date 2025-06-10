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

def test_uses_supplied_key_and_iv_to_decode_encrypted_messages(mocker: MockFixture) -> None:
    message = 'Test message'
    run_decryption_test_scenario(message, mocker)
    
def test_uses_supplied_key_and_iv_to_decode_a_different_encrypted_messages(mocker: MockFixture) -> None:
    message = 'Different test message'
    run_decryption_test_scenario(message, mocker)

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

def run_decryption_test_scenario(plaintext: str, mocker: MockFixture) -> None:
    # Encrypt the message
    key = secrets.token_bytes(32)
    cypher = AESCypher(key)
    encrypted_message = cypher.encrypt(plaintext)

    # Decrypt the message
    cyphertext = base64.b64decode(encrypted_message['body'])
    iv = base64.b64decode(encrypted_message['iv'])
    decrypted_message = decrypt(cyphertext, key, iv)

    # Expect the decrypted message to match the one returned by the cypher
    assert cypher.decrypt(encrypted_message['body'], encrypted_message['iv']) == decrypted_message
    

###################################################################################
#                                                                                 #
# Helper functions for test scenarios                                             #
#                                                                                 #
###################################################################################

# Helper function to encrypt text
def encrypt(plaintext: str, key: bytes, iv: bytes) -> str:
    padded_plaintext = pad(plaintext).encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(padded_plaintext)).decode()

def pad(plaintext: str) -> str:
    # Adds PKCS#7 padding -> k - (l mod k) octects with value k - (l mod k)
    return plaintext + (16 - len(plaintext) % 16) * chr(16 - len(plaintext) % 16)

def decrypt(cyphertext: bytes, key: bytes, iv: bytes) -> str:
    cypher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = cypher.decrypt(cyphertext).decode()
    return unpad(padded_plaintext)

def unpad(plaintext: str) -> str:
    # Strip the padding -> Since the padding value is the number of padded bytes,
    # use its value to end the returned slice
    return plaintext[:-ord(plaintext[len(plaintext) - 1:])]
