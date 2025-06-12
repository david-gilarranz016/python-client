from src.history_service import HistoryService
from src.singleton import Singleton

################################################################################
#                                                                              #
# Test cases                                                                    #
#                                                                              #
################################################################################

def test_is_singleton() -> None:
    assert issubclass(HistoryService, Singleton)

