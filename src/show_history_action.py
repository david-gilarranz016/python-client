from src.action import Action
from src.history_service import HistoryService

class ShowHistoryAction(Action):
    def run(self, args: dict[str, str]) -> str:
        # Get a history service instance
        history_service = HistoryService()

        # Search a command or return the full history
        output = ''
        if 'search' in args.keys():
            output = history_service.search_command(args['search'])[-1]
        else:
            output = '\n'.join(HistoryService().get_history())

        return output
