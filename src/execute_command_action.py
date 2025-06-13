from src.action import Action
from src.http_service import HTTPService
from typing import Any

class ExecuteCommandAction(Action):
    def run(self, args: dict[str, Any]) -> str:
        # Send the request
        request = {
            'action': 'execute_command',
            'args': {
                'cmd': args['cmd']
            }
        }
        response = HTTPService().send_request(request)

        return response['output']
