from client.singleton import Singleton

import os

class HistoryService(Singleton):

    def __init__(self) -> None:
        # Load history from disk
        try:
            with open('./.webshell_history', 'r') as f:
                history = f.readlines()
                self.__history = [ cmd.strip() for cmd in history ]
        except FileNotFoundError:
            self.__history = []

    def get_history(self) -> list[str]:
        return self.__history

    def add_command(self, cmd: str) -> None:
        # Add the command to the saved history
        self.__history.append(cmd)

        # Save the command to disk
        with open('./.webshell_history', 'a') as f:
            f.write(f'{cmd}\n')

    def search_command(self, cmd: str) -> list[str]:
        return [ c for c in self.__history if c.startswith(cmd) ] 

    def delete_history(self) -> None:
        # Empty the saved history
        self.__history = []

        # Delete the history file
        os.remove('./.webshell_history')
