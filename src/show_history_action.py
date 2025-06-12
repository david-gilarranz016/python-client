from src.action import Action
from src.history_service import HistoryService

class ShowHistoryAction(Action):
    def run(self, args: dict[str, str]) -> str:
        return '\n'.join(HistoryService().get_history())
