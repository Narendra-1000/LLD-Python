from typing import Collection, Dict, Optional

from ..model.agent import Agent


class AgentRepository:
    def __init__(self) -> None:
        self._agents: Dict[str, Agent] = {}

    def save(self, agent: Agent) -> None:
        self._agents[agent.id] = agent

    def get_by_id(self, id: str) -> Optional[Agent]:
        return self._agents.get(id)

    def get_all(self) -> Collection[Agent]:
        return self._agents.values()
