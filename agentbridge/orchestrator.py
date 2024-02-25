import random
class Orchestrator:
    def __init__(self, agent_pool, scheduling='sequential', max_calls=None, 
                 include_prior_history=None, start_agent_name=None, num_rounds=1):
        self.agent_pool = agent_pool
        self.scheduling = scheduling  
        self.max_calls = max_calls
        self.calls_processed = 0
        self.global_interaction_history = []
        self.history_inclusion_type = include_prior_history  
        if start_agent_name and start_agent_name in agent_pool.agent_names:
            self.current_agent_index = agent_pool.agent_names.index(start_agent_name)
        else:
            self.current_agent_index = 0
        self.num_rounds = num_rounds

    def format_history(self, include_input=False):
        if include_input:
            history_str = ". ".join([f"Query: {interaction['input']}. Response: {interaction['output']}" 
                                     for interaction in self.global_interaction_history])
        else:
            history_str = ". ".join([f"{interaction['output']}" 
                                     for interaction in self.global_interaction_history])
        return history_str

    def process_task(self, user_task):
        responses = []
        last_response = user_task  # Initial task for the first agent

        if self.scheduling == 'sequential':
            agent_sequence = self.agent_pool.agent_names
        elif self.scheduling == 'round_robin':
            agent_sequence = self.agent_pool.agent_names[self.current_agent_index:] + self.agent_pool.agent_names[:self.current_agent_index]
            agent_sequence *= self.num_rounds
        elif self.scheduling == 'random':
            agent_sequence = random.sample(self.agent_pool.agent_names, len(self.agent_pool.agent_names))
            agent_sequence *= self.num_rounds
        elif self.scheduling =='broadcast':
            agent_sequence = self.agent_pool.agent_names

        else:
            raise ValueError(f"Unknown scheduling method: {self.scheduling}")

        for agent_name in agent_sequence:
            agent = self.agent_pool.get_agent(agent_name)
            if self.history_inclusion_type == 'global':
                task_for_agent = f"{agent.description}. Context: {self.format_history(include_input=True)}. Task: {user_task}"
            elif self.history_inclusion_type == 'prev_agent_output':
                task_for_agent = f"{agent.description}. Context: {last_response} {user_task}" 
            elif self.history_inclusion_type == 'prev_agent_input_output' and len(self.global_interaction_history) > 0:
                last_interaction = self.global_interaction_history[-1]
                task_for_agent = f"{agent.description}. Context: {last_interaction['input']} Response: {last_interaction['output']} Task: {user_task}" 
            else: 
                task_for_agent = f"{agent.description} Task: {user_task}" 
            # print("Task for agent:", task_for_agent)
            response = self._process_with_agent(agent_name, task_for_agent)
            responses.append((agent_name, response))
            last_response = response  # Update last_response for the next iteration

            self._log_interaction(user_task, response, agent_name)
            if "END" in response:
                print(f"Terminating early: 'END' found in response from {agent_name}.")
                break  # Exit the loop early

        return responses

    def _process_with_agent(self, agent_name, user_task):
        if self.max_calls is not None and self.calls_processed >= self.max_calls:
            return "Maximum call limit reached."
        
        agent = self.agent_pool.agents[agent_name]
        response = agent.process_task(user_task)
        return response

    def _log_interaction(self, user_task, response, agent_name):
        self.global_interaction_history.append({
            "input": user_task,
            "output": response,
            "assigned_to": agent_name
        })
        self.calls_processed += 1

    def get_history(self):
        """Returns the global interaction history."""
        return self.global_interaction_history
