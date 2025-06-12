from src.action import Action
from src.history_service import HistoryService

class DeleteHistoryAction(Action):
    def run(self, args: dict[str, str]) -> str:
        # Delete the history
        HistoryService().delete_history()

        # Return empty string
        return ''
