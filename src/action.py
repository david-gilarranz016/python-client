from abc import ABC

class Action(ABC):
    def run(self, args: dict[str, str]) -> None:
        pass
