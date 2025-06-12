from src.show_history_action import ShowHistoryAction
from src.action import Action
from src.history_service import HistoryService

import pytest
import pyfakefs

################################################################################
#                                                                              #
# Fixtures -> used for setup and teardown                                      #
#                                                                              #
################################################################################

@pytest.fixture
def history_service() -> HistoryService:
    # Return a history service instance
    yield HistoryService()

    # Reset the history service
    reset_history_service()

################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_is_an_action() -> None:
    assert issubclass(ShowHistoryAction, Action)

def test_returns_saved_history(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    saved_history = [ 'pwd', 'id', 'ls -l /home' ]
    run_returns_saved_history_test_scenario(saved_history, history_service)

def test_returns_different_saved_history(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    saved_history = [ 'id', 'groups', 'docker ps -a' ]
    run_returns_saved_history_test_scenario(saved_history, history_service)

def test_returns_last_instance_of_executed_command_when_supplied_the_search_parameter(
        history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    target = 'ls'
    saved_history = [ 'pwd', 'id', 'ls -l /home', 'cd /home/web-admin', 'ls -a' ]
    run_search_history_test_scenario(saved_history, target, history_service)

def test_returns_last_instance_of_executed_command_when_supplied_different_search_parameter(
        history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    target = 'cd'
    saved_history = [ 'pwd', 'id', 'ls -l /home', 'cd /home/web-admin', 'ls -a', 'cd .ssh' ]
    run_search_history_test_scenario(saved_history, target, history_service)



################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################

def run_returns_saved_history_test_scenario(saved_history: list[str], history_service: HistoryService) -> None:
    # Save the list of commands
    for cmd in saved_history:
        history_service.add_command(cmd)

    # Run the action
    action = ShowHistoryAction()
    result = action.run({})

    # Expect the result to be the newline separated list of saved commands
    expected_result = '\n'.join(saved_history)
    assert result == expected_result

def run_search_history_test_scenario(saved_history: list[str], cmd: str, history_service: HistoryService) -> None:
    # Save the list of commands
    for cmd in saved_history:
        history_service.add_command(cmd)

    # Run the action
    action = ShowHistoryAction()
    result = action.run({ 'search': cmd })

    # Expet the last occurrence of cmd to be returned
    expected_result = [ c for c in saved_history if c.startswith(cmd) ][-1]
    assert result == expected_result

################################################################################
#                                                                              #
# Helper functions and classes                                                 #
#                                                                              #
################################################################################

def reset_history_service() -> None:
    # Destroy the created instance to reset state
    delattr(HistoryService, 'instance')
