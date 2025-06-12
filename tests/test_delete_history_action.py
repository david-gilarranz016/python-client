from src.delete_history_action import DeleteHistoryAction
from src.action import Action
from src.history_service import HistoryService

import pytest
import os
from pyfakefs.fake_filesystem import FakeFilesystem

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
    assert issubclass(DeleteHistoryAction, Action)

def test_deletes_command_history(history_service: HistoryService, fs: FakeFilesystem) -> None:
    # Save commands
    saved_history = [ 'id', 'groups', 'docker ps -a' ]
    for cmd in saved_history:
        HistoryService().add_command(cmd)

    # Run the action
    action = DeleteHistoryAction()
    action.run({})

    # Expect the command history to be empty
    assert HistoryService().get_history() == []

def test_deletes_history_file(history_service: HistoryService, fs: FakeFilesystem) -> None:
    # Save commands
    saved_history = [ 'id', 'groups', 'docker ps -a' ]
    for cmd in saved_history:
        HistoryService().add_command(cmd)

    # Run the action
    action = DeleteHistoryAction()
    action.run({})

    # Expect the history file to have been deleted
    assert not os.path.exists('./.webshell_history')

################################################################################
#                                                                              #
# Helper functions and classes                                                 #
#                                                                              #
################################################################################

def reset_history_service() -> None:
    # Destroy the created instance to reset state
    delattr(HistoryService, 'instance')
