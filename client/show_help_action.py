from client.action import Action
from typing import Any

import textwrap

class ShowHelpAction(Action):
    def run(self, args: dict[str, Any]) -> str:
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
        return textwrap.dedent(help_menu)
