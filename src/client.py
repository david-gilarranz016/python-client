from src.action import Action

class Client:
    def __init__(self, actions: dict[str, Action]) -> None:
        self.__actions = actions

    def run(self) -> int:
        user_input = input('$ ')

        while not user_input == 'exit':
            # Call the appropriate action
            self.__actions['execute_command'].run({ 'cmd': user_input })

            user_input = input('$ ')

        return 0
