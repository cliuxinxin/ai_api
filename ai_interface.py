from abc import ABC, abstractmethod

class AIInterface(ABC):
    @abstractmethod
    def get_answer(self, question: str) -> str:
        pass
