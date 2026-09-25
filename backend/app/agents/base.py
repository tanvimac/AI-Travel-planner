"""Base class for all agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict

class Agent(ABC):
    """Abstract base class for agents.

    Sub‑classes should implement the ``run`` method which receives a mutable ``context`` dict.
    The method can modify the context in‑place and return any result if desired.
    """

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Any:
        """Execute the agent logic.

        Args:
            context: Shared mutable dictionary that holds input and output from other agents.
        """
        raise NotImplementedError
