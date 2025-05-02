from abc import ABC, abstractmethod

class ILLM(ABC):
    @abstractmethod
    async def chat(self, prompt: str):
        pass
