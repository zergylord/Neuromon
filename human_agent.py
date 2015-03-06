import random
import sys
import copy
from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.types import Observation

from random import Random

class skeleton_agent(Agent):
	def agent_init(self,taskSpec):
                pass
		
	def agent_start(self,observation):
		#Generate random action, 0 or 1
		thisIntAction= np.random.randint(0,2,6)
                returnAction=Action()
		returnAction.intArray=[thisIntAction]
		return returnAction
	
	def agent_step(self,reward, observation):
		#Generate random action, 0 or 1
		thisIntAction= np.random.randint(0,2,6)
                returnAction=Action()
		returnAction.intArray=[thisIntAction]
		return returnAction
	
	def agent_end(self,reward):
		pass
	
	def agent_cleanup(self):
		pass
	
	def agent_message(self,inMessage):
		if inMessage=="what is your name?":
			return "my name is skeleton_agent, Python edition!";
		else:
			return "I don't know how to respond to your message";


if __name__=="__main__":
	AgentLoader.loadAgent(skeleton_agent())
