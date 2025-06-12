from src.show_history_action import ShowHistoryAction
from src.action import Action

def test_is_an_action() -> None:
    assert issubclass(ShowHistoryAction, Action)
