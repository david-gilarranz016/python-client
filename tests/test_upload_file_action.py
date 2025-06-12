from src.action import Action
from src.upload_file_action import UploadFileAction
from src.http_service import HTTPService

import pytest
import pytest_mock
from pyfakefs.fake_filesystem import FakeFilesystem
import base64
from unittest.mock import MagicMock


################################################################################
#                                                                              #
# Fixtures -> used for setup and teardown                                      #
#                                                                              #
################################################################################

@pytest.fixture
def http_service(mocker: pytest_mock.MockFixture) -> MagicMock:
    # Change the HTTPService instance for a mocked version
    mocked_service = MagicMock()
    setattr(HTTPService, 'instance', mocked_service)

    yield mocked_service

    delattr(HTTPService, 'instance')

################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_is_action() -> None:
    assert issubclass(UploadFileAction, Action)

def test_uploads_base64_encoded_text_file(http_service: MagicMock, fs: FakeFilesystem) -> None:
    filename = 'test.txt'
    content = 'Sample content'
    binary = False
    run_uploads_base64_encoded_file_scenario(filename, content, binary, http_service)

def test_uploads_different_base64_encoded_text_file(http_service: MagicMock, fs: FakeFilesystem) -> None:
    filename = 'different_file.txt'
    content = 'Different content'
    binary = False
    run_uploads_base64_encoded_file_scenario(filename, content, binary, http_service)

def test_uploads_base64_encoded_binary_file(http_service: MagicMock, fs: FakeFilesystem) -> None:
    filename = 'test.bin'
    content = b'Sample binary content'
    binary = True
    run_uploads_base64_encoded_file_scenario(filename, content, binary, http_service)

def test_uploads_different_base64_encoded_binary_file(http_service: MagicMock, fs: FakeFilesystem) -> None:
    filename = 'different_file.bin'
    content = b'Different binary content'
    binary = True
    run_uploads_base64_encoded_file_scenario(filename, content, binary, http_service)

################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################

def run_uploads_base64_encoded_file_scenario(filename: str, contents: str | bytes, binary: bool, http_service: MagicMock) -> None:
    # Create the file
    create_file(filename, contents, binary)

    # Get the base64-encoded contents
    raw_contents = contents if binary else contents.encode()
    base64_contents = base64.b64encode(raw_contents).decode()
    request = {
        'action': 'upload_file',
        'args': {
            'filename': filename,
            'content': base64_contents,
            'binary': binary
        }
    }

    # Run the action
    action = UploadFileAction()
    action.run({ 'filename': filename, 'binary': binary })

    # Expect the http_service to be called with the appropriate parameters
    http_service.send_request.assert_called_once_with(request)

################################################################################
#                                                                              #
# Helper functions                                                             #
#                                                                              #
################################################################################

def create_file(filename: str, content: str | bytes, binary: bool) -> None:
    mode = 'wb' if binary else 'w'
    with open(filename, mode) as f:
        f.write(content)
