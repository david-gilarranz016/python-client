from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def run(self, args: dict[str, str]) -> str:
        pass
