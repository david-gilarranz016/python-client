from src.history_service import HistoryService
from src.singleton import Singleton

import pytest
import pyfakefs
import os

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

def test_loads_history_from_disk(fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    saved_history = [ 'whoami', 'id', 'pwd', 'ls -l' ]
    run_loads_history_test_scenario(saved_history)
    
def test_loads_different_history_from_disk(fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    saved_history = [ 'ls -la', 'rm .bash_history', 'groups' ]
    run_loads_history_test_scenario(saved_history)

def test_saves_command_to_disk(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    cmd = 'pwd'
    run_saves_command_test_scenario(cmd, history_service)
    
def test_saves_different_command_to_disk(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    cmd = 'id'
    run_saves_command_test_scenario(cmd, history_service)

def test_returns_saved_commands_when_requesting_history(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    # Save a few commands
    cmds = [ 'cat /etc/passwd', 'cd /home/web-admin', 'ls -l' ]
    for cmd in cmds:
        history_service.add_command(cmd)

    # Retrieve the command history and expect it to contain the saved commands
    history = history_service.get_history()
    assert history == cmds

def test_search_history_filters_output_to_commands_matching_query(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    cmds = [ 'cat /etc/passwd', 'cd /home/web-admin', 'ls -l', 'cat flag.txt' ]
    search_cmd = 'cat' 
    run_search_history_test_scenario(history_service, cmds, search_cmd)

def test_search_history_filters_output_to_commands_matching_different_query(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    cmds = [ 'cat /etc/passwd', 'cd /home/web-admin', 'ls -l', 'cat flag.txt' ]
    search_cmd = 'ls' 
    run_search_history_test_scenario(history_service, cmds, search_cmd)

def test_delete_history_empties_the_command_history(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    # Add a series of commands
    cmds = [ 'cat /etc/passwd', 'cd /home/web-admin', 'ls -l' ]
    for cmd in cmds:
        history_service.add_command(cmd)

    # Delete the history and expect it to be empty
    history_service.delete_history()
    assert history_service.get_history() == []

def test_delete_history_deletes_the_history_file(history_service: HistoryService, fs: pyfakefs.fake_filesystem.FakeFilesystem) -> None:
    # Add a series of commands
    cmds = [ 'cat /etc/passwd', 'cd /home/web-admin', 'ls -l' ]
    for cmd in cmds:
        history_service.add_command(cmd)

    # Delete the history and expect the file to have been removed
    history_service.delete_history()
    
    assert os.path.exists('./.webshell_history') == False

################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################

def run_loads_history_test_scenario(saved_history: list[str]) -> None:
    with open('./.webshell_history', 'w') as f:
        f.writelines(map(lambda cmd: cmd + '\n', saved_history))
    
    # Request the history and expect the file to have been read
    history_service = HistoryService()
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

def run_search_history_test_scenario(history_service: HistoryService, commands: list[str], search_target: str) -> None:
    # Save a list of commands
    for cmd in commands:
        history_service.add_command(cmd)

    # Search the command
    expected_result = [ cmd for cmd in commands if cmd.startswith(search_target) ]
    result = history_service.search_command(search_target)

    assert result == expected_result

################################################################################
#                                                                              #
# Helper functions and classes                                                 #
#                                                                              #
################################################################################

def reset_history_service() -> None:
    # Destroy the created instance to reset state
    delattr(HistoryService, 'instance')
