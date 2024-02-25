import unittest
from unittest.mock import MagicMock 
import random 
from agentbridge.orchestrator import Orchestrator
from agentbridge.agent_pool import AgentPool
from agentbridge.agents import BaseAgent  

import unittest
from unittest.mock import MagicMock

class TestOrchestrator(unittest.TestCase):

    def setUp(self):
        self.agent1 = MagicMock(spec=BaseAgent, name="Agent1", description="Description1")
        self.agent2 = MagicMock(spec=BaseAgent, name="Agent2", description="Description2")
        
        self.agent1.name = "Agent1"
        self.agent2.name = "Agent2"
        self.agent1.description = "Description1"
        self.agent2.description = "Description2"
        
        self.agent1.process_task.reset_mock(side_effect=True)
        self.agent1.process_task.side_effect = ["Response from Agent1", "Another Response from Agent1"]
        self.agent2.process_task.reset_mock(side_effect=True)
        self.agent2.process_task.side_effect = ["Response from Agent2", "Another Response from Agent2"]
        
        self.agent_pool = AgentPool()
        self.agent_pool.register_agent(self.agent1)
        self.agent_pool.register_agent(self.agent2)

    def test_history_inclusion_prev_agent_input_output(self):
        orchestrator = Orchestrator(self.agent_pool, scheduling='sequential', include_prior_history='prev_agent_input_output')
        responses = orchestrator.process_task("Initial Task")

        expected_task_for_agent2 = "Description2. Context: Initial Task Response: Response from Agent1 Task: Initial Task"  
        self.agent2.process_task.assert_called_once_with(expected_task_for_agent2)

        self.agent2.process_task.assert_called_once_with(expected_task_for_agent2)

    def test_scheduling_sequential(self):
        orchestrator = Orchestrator(self.agent_pool, scheduling='sequential')
        orchestrator.process_task("Task for sequential scheduling")
        self.agent1.process_task.assert_called_once_with("Description1 Task: Task for sequential scheduling")
        self.agent2.process_task.assert_called_once_with("Description2 Task: Task for sequential scheduling")

    def test_scheduling_round_robin(self):
        num_rounds = 2
        orchestrator = Orchestrator(self.agent_pool, scheduling='round_robin', num_rounds=num_rounds)
        
        called_agent_names = []
        def track_agent_call(agent_name, task): 
            called_agent_names.append(agent_name)
            return f"Response from {agent_name}" 
        orchestrator._process_with_agent = track_agent_call
        orchestrator.process_task("Task for round robin 1")
        orchestrator.process_task("Task for round robin 2")

        expected_sequence = []
        for _ in range(num_rounds * 2): 
            expected_sequence += self.agent_pool.agent_names 

        self.assertEqual(called_agent_names, expected_sequence)


    def test_scheduling_random(self):
        orchestrator = Orchestrator(self.agent_pool, scheduling='random', num_rounds=1)
        orchestrator.process_task("Task for random scheduling")
        self.assertEqual(self.agent1.process_task.call_count, 1)
        self.assertEqual(self.agent2.process_task.call_count, 1)


    def test_max_calls_limit(self):
        orchestrator = Orchestrator(self.agent_pool, scheduling='sequential', max_calls=1)
        orchestrator.process_task("Task with max calls limit")
        self.agent1.process_task.assert_called_once()
        self.agent2.process_task.assert_not_called()

if __name__ == '__main__':
    unittest.main()