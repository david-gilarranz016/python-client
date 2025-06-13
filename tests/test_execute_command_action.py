from src.action import Action
from src.execute_command_action import ExecuteCommandAction
from src.history_service import HistoryService
from src.http_service import HTTPService

import pytest
from unittest.mock import MagicMock

################################################################################
#                                                                              #
# Fixtures -> used for setup and teardown                                      #
#                                                                              #
################################################################################

@pytest.fixture
def http_service() -> MagicMock:
    # Mock HTTPService to return a mock instance
    http_service = MagicMock()
    setattr(HTTPService, 'instance', http_service)

    yield http_service

    # Revert mock
    delattr(HTTPService, 'instance')

@pytest.fixture
def history_service() -> MagicMock:
    # Mock history_service to return a mock instance
    history_service = MagicMock()
    setattr(HistoryService, 'instance', history_service)

    yield history_service 

    # Revert mock
    delattr(HistoryService, 'instance')


################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_is_action() -> None:
    assert issubclass(ExecuteCommandAction, Action)

def test_uses_http_service_to_request_command(http_service: MagicMock, history_service: MagicMock) -> None:
    cmd = 'id'
    run_sends_command_test_scenario(cmd, http_service)

def test_uses_http_service_to_request_different_command(http_service: MagicMock, history_service: MagicMock) -> None:
    cmd = 'pwd'
    run_sends_command_test_scenario(cmd, http_service)

def test_returns_command_output(http_service: MagicMock, history_service: MagicMock) -> None:
    output = 'uid=1000(web-admin) gid=1000(web-admin) groups=1000(web-admin),962(docker)'
    run_returns_command_output_test_scenario(output, http_service)

def test_returns_different_command_output(http_service: MagicMock, history_service: MagicMock) -> None:
    output = '/var/www/html'
    run_returns_command_output_test_scenario(output, http_service)

def test_logs_requested_command(http_service: MagicMock, history_service: MagicMock) -> None:
    cmd = 'id'
    run_logs_command_test_scenario(cmd, history_service)

def test_logs_different_requested_command(http_service: MagicMock, history_service: MagicMock) -> None:
    cmd = 'pwd'
    run_logs_command_test_scenario(cmd, history_service)


################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################

def run_sends_command_test_scenario(cmd: str, http_service: MagicMock) -> None:
    # Craft the expected request
    request = {
        'action': 'execute_command',
        'args': {
            'cmd': cmd
        }
    }

    # Run the action
    action = ExecuteCommandAction()
    action.run({ 'cmd': cmd })

    # Expect the HTTPService to have been requested the request
    http_service.send_request.assert_called_once_with(request)

def run_returns_command_output_test_scenario(output: str, http_service: MagicMock) -> None:
    # Set the return value for the request
    http_service.send_request.return_value = { 'output': output }
        
    # Run the action
    action = ExecuteCommandAction()
    response = action.run({ 'cmd': 'id' })

    # Expext the response to be the supplied output
    assert response == output

def run_logs_command_test_scenario(cmd: str, history_service: MagicMock) -> None:
    # Run the action
    action = ExecuteCommandAction()
    response = action.run({ 'cmd': cmd })

    # Expext the history service to have been requested to log the command
    history_service.add_command.assert_called_once_with(cmd)


################################################################################
#                                                                              #
# Helper functions                                                             #
#                                                                              #
################################################################################

