from client.action import Action
from client.show_help_action import ShowHelpAction

import pytest
import textwrap
from pytest_mock import MockFixture

################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_is_an_action() -> None:
    assert issubclass(ShowHelpAction, Action)

def test_returns_help_message(mocker: MockFixture) -> None:
    help_menu = """
    Client for interacting with the remote webshell. The following actions are available:

    - <cmd>              : run the desired shell command on the target.
    - exit               : quit the shell.
    - !get <filename>    : download a text file.
    - !binget <filename> : download a binary file.
    - !put <filename>    : upload a text file.
    - !binput <filename> : upload a binary file.
    - !history           : view a list of all previously executed commands.
    - !delete            : clear the command history.
    - !<cmd>             : repeat the last command that starts with the provided string.
    - !help              : show this help menu.

    """

    # Run the Action and expect the help menu to have been printed
    output = ShowHelpAction().run({})
    assert output == textwrap.dedent(help_menu)

