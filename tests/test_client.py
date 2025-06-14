from src.client import Client

import pytest
from unittest.mock import MagicMock
from pytest_mock import MockFixture
from multiprocessing import Process

################################################################################
#                                                                              #
# Pytest Fixtures -> used to arrange tests                                     #
#                                                                              #
################################################################################

@pytest.fixture
def client() -> Client:
    # Create a series of MagicMock objects for each action
    keys = [
        'execute_command',
        'upload_file',
        'download_file',
        'show_history',
        'delete_history'
    ]
    actions = {}
    for key in keys:
        actions[key] = MagicMock()

    yield Client(actions)

################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_when_exit_command_is_inputted_loop_stops(client: Client, mocker: MockFixture) -> None:
    # Send the exit command and run the client
    mock_input(['exit'], mocker)
    status = client.run()

    # Expect the method to exit with code 0
    assert status ==  0

def test_keeps_running_until_exit_command_is_received(client: Client, mocker: MockFixture) -> None:
    # Run the client with a 1ms timeout
    mock_input(['id'] * 1000000, mocker)
    test_process = Process(target=client.run)
    test_process.start()
    test_process.join(0.01)

    # Expect the thread to keep running
    assert test_process.is_alive()

    # Kill the test process
    test_process.terminate()

def test_calls_execute_command_action_when_receives_a_command(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['id', 'whoami']
    mock_input(commands, mocker, append_exit=True)

    # Run the client
    client.run()

    # Expect the execute_command action to have been called once with each command
    for cmd in commands:
        client._Client__actions['execute_command'].run.assert_any_call({ 'cmd': cmd })


################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################

def run_execute_command_test_scenario(cmd: list[str], client: Client, mocker: MockFixture) -> None:
    pass

################################################################################
#                                                                              #
# Helper functions                                                             #
#                                                                              #
################################################################################

def mock_input(user_inputs: list[str], mocker: MockFixture, append_exit = False) -> None:
    # Mock the built-in input function to return the appropriate values on successive calls
    mocked_input = mocker.patch('builtins.input')
    if append_exit:
        mocked_input.side_effect = user_inputs + ['exit']
    else:
        mocked_input.side_effect = user_inputs
