from abc import ABC, abstractmethod
from typing import Any

class Action(ABC):
    @abstractmethod
    def run(self, args: dict[str, Any]) -> str:
        pass
