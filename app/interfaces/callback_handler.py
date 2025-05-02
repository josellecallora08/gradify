from abc import ABC, abstractmethod
from typing import Dict

class CallbackHandler(ABC):
    @abstractmethod
    async def handler(self, payload: Dict[str, str]) -> None:
        pass
