from abc import ABC, abstractmethod
from models.schemas import AgentResult
from typing import Dict, Any

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any], memory) -> AgentResult:
        pass