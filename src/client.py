from src.action import Action

class Client:
    def __init__(self, actions: dict[str, Action]) -> None:
        self.__actions = actions

    def run(self) -> int:
        user_input = input('$ ')

        while not user_input == 'exit':
            # Call the appropriate action
            action = None
            args = {}

            # Select the appropriate action
            if user_input.startswith('!put'):
                action = 'upload_file'
                args = { 'filename': user_input.split(' ', 1)[1], 'binary': False }
            elif user_input.startswith('!binput'):
                action = 'upload_file'
                args = { 'filename': user_input.split(' ', 1)[1], 'binary': True}
            else:
                action = 'execute_command'
                args = { 'cmd': user_input }

            # Run the action
            output = self.__actions[action].run(args)
            print(output)

            user_input = input('$ ')

        return 0
