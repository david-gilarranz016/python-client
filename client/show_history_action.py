from client.action import Action
from client.history_service import HistoryService
from typing import Any

class ShowHistoryAction(Action):
    def run(self, args: dict[str, Any]) -> str:
        # Get a history service instance
        history_service = HistoryService()

        # Search a command or return the full history
        output = ''
        if 'search' in args.keys():
            output = history_service.search_command(args['search'])[-1]
        else:
            output = '\n'.join(HistoryService().get_history())

        return output
