from abc import ABC, abstractmethod

class DocumentLoader(ABC):
    @abstractmethod
    def load(self, document):
        pass