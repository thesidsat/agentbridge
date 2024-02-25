# agentbridge

Orchestrate LLMs in a multi-agent system using LangChain and/or Llama Index.  Manage agent interactions, task routing, and knowledge sharing.

## Installation

```
pip install agentbridge
```

## Features
- Flexible LLM Integration: Work with a variety of language models seamlessly.
    - LangChain objects supporting the invoke() method.
    - Llama Index objects supporting chat(), query() or complete() methods.

- Powerful Orchestration: Coordinate multiple LLMs using customizable scheduling strategies (sequential, round-robin, etc.)
- Contextual Awareness: Maintain historical context across agent interactions 
- LangChain and Llama Index Support

## Usage Example:
```
    from agentbridge.agents import LangChainAgent, LlamaIndexAgent
    from agentbridge.agent_pool import AgentPool
    from agentbridge.orchestrator import Orchestrator
    from langchain_openai import ChatOpenAI 
    from langchain_core.prompts import ChatPromptTemplate
    from llama_index.llms.ollama import Ollama 

    llm_mistral = Ollama(model="mistral", request_timeout=100.0)
    llm_openai = ChatOpenAI(openai_api_key="")


    # Create prompt templates 
    prompt = ChatPromptTemplate.from_messages([("user", "{input}")])
    closedsource = prompt | llm_openai
    judge = prompt | llm_openai


    # Initialize AgentPool and register agents
    agent_pool = AgentPool()
    agent_pool.register_agent(LlamaIndexAgent(name="OpenSource", description="You are an expert debator and you present only the side for open source AI as the future", agent = llm_mistral, mode='complete'))
    agent_pool.register_agent(LangChainAgent(name="ClosedSource",description= "You are an expert debator and you present only the side for closed source AI as the future", agent = closedsource))
    agent_pool.register_agent(LangChainAgent(name="Judge", description="You judge the debate on the merits of each argument and select a winner for each discussion", agent= judge))

    # Initialize Manager with specific configurations
    orchestrate = Orchestrator(agent_pool, scheduling='sequential', num_rounds=1, max_calls=10, include_prior_history="global", start_agent_name='OpenSource')

    # Process task
    responses = orchestrate.process_task("We are here to judge the merits and demerits of closed vs open soure AI")
    for agent_name, response in responses:
        print("\n")
        print(f"Response from {agent_name}: {response}")
```