from client.action import Action
from client.http_service import HTTPService
from client.history_service import HistoryService
from typing import Any

class ExecuteCommandAction(Action):
    def run(self, args: dict[str, Any]) -> str:
        # Craft the request and log the command
        request = {
            'action': 'execute_command',
            'args': {
                'cmd': args['cmd']
            }
        }
        HistoryService().add_command(args['cmd'])

        # Send the request and return the response
        response = HTTPService().send_request(request)
        return response['output']
