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

def test_uploads_base64_encoded_file(http_service: MagicMock, fs: FakeFilesystem) -> None:
    filename = 'test.txt'
    content = 'Sample content'
    run_uploads_base64_encoded_file_scenario(filename, content, http_service)

def test_uploads_different_base64_encoded_file(http_service: MagicMock, fs: FakeFilesystem) -> None:
    filename = 'different_file.txt'
    content = 'Different content'
    run_uploads_base64_encoded_file_scenario(filename, content, http_service)

################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################

def run_uploads_base64_encoded_file_scenario(filename: str, contents: str, http_service: MagicMock) -> None:
    # Create the file
    create_file(filename, contents)

    # Get the base64-encoded contents
    base64_contents = base64.b64encode(contents.encode()).decode()
    request = {
        'action': 'upload_file',
        'args': {
            'filename': filename,
            'content': base64_contents
        }
    }

    # Run the action
    action = UploadFileAction()
    action.run({ 'filename': filename })

    # Expect the http_service to be called with the appropriate parameters
    http_service.send_request.assert_called_once_with(request)

################################################################################
#                                                                              #
# Helper functions                                                             #
#                                                                              #
################################################################################

def create_file(filename: str, content: str) -> None:
    with open(filename, 'w') as f:
        f.writelines(content)
