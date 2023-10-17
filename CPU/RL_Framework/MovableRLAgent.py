from DeepQNetwork.experience import Experience
import numpy as np
import torch
import collections
from collections import namedtuple
import time

# create a named tuple to store the agent's past experience
Experience = namedtuple('Experience',
                         field_names = ['state','action','reward','done','new_state'])
                         
# Here we define the agent for the movable RL agent DQN
class MovableRLAgentDQN:
  def __init__(self,env,exp_buffer):
    self.env = env
    self.exp_buffer = exp_buffer
    self._reset()

  # the environment (AI gym) resets itself through calling
  # its reset function. The total reward of the agent becomes 0
  # as well
  def _reset(self):
    self.state = self.env.reset()
    self.total_reward = 0.0

  ## Used to build the predictive network
  def play_step(self,net,epsilon,device = "cpu"):
    done_reward = None
    np.random.seed(20)
    if np.random.random() < epsilon:
      action = self.env.action_space.sample()
    else:
      state_a = np.array([self.state],copy = False)
      state_v = torch.tensor(state_a,dtype = torch.float).to(device)
      q_vals_v = net(state_v)
      _,act_v = torch.max(q_vals_v,dim = 0)
      action = int(act_v.item())

      #print('action chosen in step is ',action)
      #print(f'step is {self.env.step(action)}')
      step_start_time = time.time()
      new_state,reward,is_done,_ = self.env.step(action)
      step_end_time = time.time()
      print(f'Total time for the RL_M step is {step_end_time - step_start_time}')
      self.total_reward += reward
      
      exp = Experience(self.state,action,reward,is_done,new_state)
      self.exp_buffer.append(exp)

      # Agent moves to the new state
      self.state = new_state

      # intermediate CSP >= target immovable CSP so done
      if is_done:
        # get the total reward received by the agent
        done_reward = self.total_reward
        self._reset() 
      return done_reward