class BaseAgent:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def process_task(self, task):
        pass 

class LangChainAgent(BaseAgent):
    def __init__(self, name, description, agent):
        super().__init__(name, description)
        self.chain = agent
    def process_task(self, task):
        return self.chain.invoke({"input": task})

class LlamaIndexAgent(BaseAgent):
    def __init__(self, name, description, agent, mode='chat'):  # agent will be the LlamaIndex
        super().__init__(name, description)
        self.agent = agent 
        self.mode = mode

    def process_task(self, task):
        if self.mode == 'chat':
            return self.agent.chat(task)
        elif self.mode == 'query':
            query_engine = self.agent.as_query_engine()
            return query_engine.query(task) 
        elif self.mode == 'complete':
            response = self.agent.complete(task)  
            return response.text
        else:
            raise ValueError(f"Invalid mode: {self.mode}")
