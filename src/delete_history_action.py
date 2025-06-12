from src.action import Action
from src.history_service import HistoryService
from typing import Any

class DeleteHistoryAction(Action):
    def run(self, args: dict[str, Any]) -> str:
        # Delete the history
        HistoryService().delete_history()

        # Return empty string
        return ''
