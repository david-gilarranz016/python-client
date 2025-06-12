from src.singleton import Singleton

class HistoryService(Singleton):
    def get_history(self) -> list[str]:
        # Load history file
        history = []
        with open('./.webshell_history', 'r') as f:
            history = f.readlines()
            history = list(map(lambda cmd: cmd.strip(), history))

        return history

    def add_command(self, cmd: str) -> None:
        # Save the command to disk
        with open('./.webshell_history', 'a') as f:
            f.write(f'{cmd}\n')
