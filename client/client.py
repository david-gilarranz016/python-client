from client.action import Action

import textwrap

class Client:
    def __init__(self, actions: dict[str, Action]) -> None:
        self.__actions = actions

    def run(self) -> int:
        user_input = input('$ ')

        while not user_input == 'exit':
            # Call the appropriate action
            action = ''
            args = {}

            # Select the appropriate action
            if user_input == '!help':
                action = 'show_help'
                args = {}
            elif user_input.startswith('!put'):
                action = 'upload_file'
                args = { 'filename': user_input.split(' ', 1)[1], 'binary': False }
            elif user_input.startswith('!binput'):
                action = 'upload_file'
                args = { 'filename': user_input.split(' ', 1)[1], 'binary': True}
            elif user_input.startswith('!get'):
                action = 'download_file'
                args = { 'filename': user_input.split(' ', 1)[1], 'binary': False }
            elif user_input.startswith('!binget'):
                action = 'download_file'
                args = { 'filename': user_input.split(' ', 1)[1], 'binary': True}
            elif user_input == '!history':
                action = 'show_history'
                args = {}
            elif user_input == '!delete':
                action = 'delete_history'
                args = {}
            elif user_input.startswith('!'):
                previous_command = self.__actions['show_history'].run({ 'search': user_input.lstrip('!') })
                action = 'execute_command'
                args = { 'cmd': previous_command }
            else:
                action = 'execute_command'
                args = { 'cmd': user_input }

            # Run the action
            try:
                output = self.__actions[action].run(args)
                print(output.replace('\\n', '\n'))
            except:
                print('Error: the requested action could not be performed')

            user_input = input('$ ')

        return 0
