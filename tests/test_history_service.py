from src.history_service import HistoryService
from src.singleton import Singleton

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

def test_is_singleton() -> None:
    assert issubclass(HistoryService, Singleton)

def test_loads_history_from_disk(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    saved_history = [ 'whoami', 'id', 'pwd', 'ls -l' ]
    run_loads_history_test_scenario(saved_history, history_service)
    
def test_loads_different_history_from_disk(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    saved_history = [ 'ls -la', 'rm .bash_history', 'groups' ]
    run_loads_history_test_scenario(saved_history, history_service)

def test_saves_command_to_disk(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    cmd = 'pwd'
    run_saves_command_test_scenario(cmd, history_service)
    
def test_saves_different_command_to_disk(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    cmd = 'pwd'
    run_saves_command_test_scenario(cmd, history_service)

################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################

def run_loads_history_test_scenario(saved_history: list[str], history_service: HistoryService) -> None:
    with open('./.webshell_history', 'w') as f:
        f.writelines(map(lambda cmd: cmd + '\n', saved_history))
    
    # Request the history and expect the file to have been read
    history = history_service.get_history()

    # Expect both lists to be equal
    assert history == saved_history

def run_saves_command_test_scenario(command: str, history_service: HistoryService) -> None:
    # Use the history service to save the command
    history_service.add_command(command)

    # Expect the command to be saved
    with open('./.webshell_history', 'r') as f:
        saved_history = f.readlines()
        assert saved_history[len(saved_history) - 1] == f'{command}\n'

################################################################################
#                                                                              #
# Helper functions and classes                                                 #
#                                                                              #
################################################################################

def reset_history_service() -> None:
    # Destroy the created instance to reset state
    delattr(HistoryService, 'instance')
