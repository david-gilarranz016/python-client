from client.client import Client

import pytest
import textwrap
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
        'delete_history',
        'show_help'
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

def test_prints_command_output(client: Client, mocker: MockFixture) -> None:
    # Craft a list of input commands and their outputs
    mock_input(['pwd', 'whoami'], mocker, append_exit=True)
    outputs = [ '/var/www/html', 'www-data' ]
    client._Client__actions['execute_command'].run.side_effect = outputs

    # Mock the print() function
    mock_print = mocker.patch('builtins.print')

    # Run the client
    client.run()

    # Expect the print command to have been called with each output
    for output in outputs:
        mock_print.assert_any_call(output)

def test_calls_upload_file_action_for_text_files(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['!put test.txt', '!put "/home/tester/secret payload.txt"']
    mock_input(commands, mocker, append_exit=True)

    # Run the client
    client.run()

    # Expect the execute_command action to have been called once with each command
    for cmd in commands:
        request = {
            'filename': cmd.split(' ', 1)[1],
            'binary': False
        }
        client._Client__actions['upload_file'].run.assert_any_call(request)
        
def test_calls_upload_file_action_for_binary_files(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['!binput exploit.bin', '!binput "src/different exploit.bin"']
    mock_input(commands, mocker, append_exit=True)

    # Run the client
    client.run()

    # Expect the execute_command action to have been called once with each command
    for cmd in commands:
        request = {
            'filename': cmd.split(' ', 1)[1],
            'binary': True
        }
        client._Client__actions['upload_file'].run.assert_any_call(request)

def test_calls_download_file_action_for_text_files(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['!get php.ini', '!get "/home/www-data/config backup.txt"']
    mock_input(commands, mocker, append_exit=True)

    # Run the client
    client.run()

    # Expect the execute_command action to have been called once with each command
    for cmd in commands:
        request = {
            'filename': cmd.split(' ', 1)[1],
            'binary': False
        }
        client._Client__actions['download_file'].run.assert_any_call(request)
        
def test_calls_download_file_action_for_binary_files(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['!binget backup.tar.gz', '!binget "/home/www-admin/privileged program.bin"']
    mock_input(commands, mocker, append_exit=True)

    # Run the client
    client.run()

    # Expect the execute_command action to have been called once with each command
    for cmd in commands:
        request = {
            'filename': cmd.split(' ', 1)[1],
            'binary': True
        }
        client._Client__actions['download_file'].run.assert_any_call(request)

def test_calls_delete_history_action(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['!delete']
    mock_input(commands, mocker, append_exit=True)

    # Run the client
    client.run()

    # Expect the execute_command action to have been called once with each command
    client._Client__actions['delete_history'].run.assert_called_once_with({})

def test_calls_show_history_action(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['!history']
    mock_input(commands, mocker, append_exit=True)

    # Run the client
    client.run()

    # Expect the execute_command action to have been called once with each command
    client._Client__actions['show_history'].run.assert_called_once_with({})

def test_can_repeat_last_call_to_command(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['whoami', '!who']
    mock_input(commands, mocker, append_exit=True)
    client._Client__actions['show_history'].run.return_value = commands[0]

    # Run the client
    client.run()

    # Expect the show_history action to have been used to query for the command and the
    # execute_command action to run it
    client._Client__actions['show_history'].run.assert_any_call({ 'search': 'who' })
    client._Client__actions['execute_command'].run.assert_any_call({ 'cmd': 'whoami' })

def test_can_show_a_help_menu(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['!help']
    mock_input(commands, mocker, append_exit=True)

    # Run the client
    client.run()

    # Expect the show_help action to have been called
    client._Client__actions['show_help'].run.assert_any_call({})

def test_if_an_error_occurs_an_error_message_is_shown(client: Client, mocker: MockFixture) -> None:
    # Craft the list of expected commands
    commands = ['cd /etc/passwd']
    mock_input(commands, mocker, append_exit=True)

    # Mock the print() function
    mock_print = mocker.patch('builtins.print')

    # Run the client
    client._Client__actions['execute_command'].run.side_effect = Exception('Test error')
    client.run()

    # Expect the error message to be shown
    mock_print.assert_any_call('Error: the requested action could not be performed')

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
