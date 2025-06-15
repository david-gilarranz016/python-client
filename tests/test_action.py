from abc import ABC
from client.action import Action

################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_is_abstract_class() -> None:
    assert issubclass(Action, ABC)

def test_has_run_method() -> None:
    assert hasattr(Action, 'run') and callable(getattr(Action, 'run'))

def test_run_method_is_abstract() -> None:
    assert 'run' in Action.__abstractmethods__
