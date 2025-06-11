from src.singleton import Singleton
from typing import Callable

import pytest

################################################################################
#                                                                              #
# Pytest fixtures. Used for arranging code before tests.                       #
#                                                                              #
################################################################################

@pytest.fixture
def singleton_factory() -> Callable[[], Singleton]:
    # Create a Singleton class for testing the metaclass
    class TestSingleton(Singleton):
        pass
    
    # Define a factory function to create singleton instances
    def _singleton_factory():
        return TestSingleton()

    # Return the singleton factory
    yield _singleton_factory


################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_returns_the_same_object(singleton_factory: Callable[[], Singleton]) -> None:
    # Get two different singleton instances
    instance1 = singleton_factory()
    instance2 = singleton_factory()

    # Expect both instances to be the same object
    assert instance1 is instance2
