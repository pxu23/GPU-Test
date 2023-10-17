from DeepQNetwork.experience import Experience
import numpy as np
import torch

## Here we define the agent for the DQN (will adapt it to the 
## immovable RL agent and the movable RL agent)
class ImmovableRLAgentDQN:
  def __init__(self,env,exp_buffer):
    self.env = env
    self.exp_buffer = exp_buffer
    self._reset()

  ## reset the environment (AI gym) and the total reward
  ## received by the agent becomes 0
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

      # print('action chosen in step is ',action)
      new_state,reward,is_done,_ = self.env.step(action)
      self.total_reward += reward
      
      exp = Experience(self.state,action,reward,is_done,new_state)
      self.exp_buffer.append(exp)

      ## Agent moves to the new state
      self.state = new_state

      ## intermediate CSP >= target immovable CSP so done
      if is_done:
        ## get the total reward received by the agent
        done_reward = self.total_reward
        self._reset() 
      return done_reward