from abc import ABC
from src.action import Action

def test_is_abstract_class():
    # Get an action
    assert issubclass(Action, ABC)
