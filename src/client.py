from src.action import Action

class Client:
    def __init__(self, actions: dict[str, Action]) -> None:
        pass

    def run(self) -> int:
        user_input = input('$ ')

        while not user_input == 'exit':
            user_input = input('$ ')

        return 0
