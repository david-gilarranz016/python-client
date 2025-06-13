from src.action import Action
from src.execute_command_action import ExecuteCommandAction
from src.history_service import HistoryService
from src.http_service import HTTPService

import pytest

################################################################################
#                                                                              #
# Fixtures -> used for setup and teardown                                      #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_is_action() -> None:
    assert issubclass(ExecuteCommandAction, Action)


################################################################################
#                                                                              #
# Test scenarios to avoid test-case code duplication                           #
#                                                                              #
################################################################################


################################################################################
#                                                                              #
# Helper functions                                                             #
#                                                                              #
################################################################################

