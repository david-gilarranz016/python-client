from src.action import Action
from src.download_file_action import DownloadFileAction
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
    assert issubclass(DownloadFileAction, Action)

def test_requests_a_file_to_be_downloaded(http_service: MagicMock, fs: FakeFilesystem) -> None:
    filename = 'test.txt'
    run_requests_file_test_scenario(filename, http_service)

def test_requests_a_different_file_to_be_downloaded(http_service: MagicMock, fs: FakeFilesystem) -> None:
    filename = 'different_file.txt'
    run_requests_file_test_scenario(filename, http_service)

################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################

def run_requests_file_test_scenario(filename: str, http_service: MagicMock) -> None:
    # Create request
    request = {
        'action': 'download_file',
        'args': {
            'filename': filename
        }
    }
    
    # Run the action
    action = DownloadFileAction()
    action.run({ 'filename': filename })

    # Expect the request to have been made
    http_service.send_request.assert_called_once_with(request)

################################################################################
#                                                                              #
# Helper functions                                                             #
#                                                                              #
################################################################################

