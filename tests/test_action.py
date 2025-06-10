from abc import ABC
from src.action import Action

def test_is_abstract_class():
    assert issubclass(Action, ABC)

def test_has_run_method():
    assert hasattr(Action, 'run') and callable(getattr(Action, 'run'))
