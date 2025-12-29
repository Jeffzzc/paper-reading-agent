from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    @abstractmethod
    async def run(self, input_data: Any) -> Any:
        pass
