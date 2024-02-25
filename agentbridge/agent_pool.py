from .agents import BaseAgent
class AgentPool:
    def __init__(self):
        self.agents = {}
        self.agent_names = []

    def register_agent(self, agent: BaseAgent):
        self.agents[agent.name] = agent
        self.agent_names.append(agent.name)

    def get_agent(self, name: str):
        return self.agents.get(name)
