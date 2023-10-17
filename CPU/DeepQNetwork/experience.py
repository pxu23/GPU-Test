import numpy as np
import collections
from collections import namedtuple

"""
    Experience is a named tuple that stores an agent's past experience in the form of
    (state, action, reward, done, new_state) tuples.
"""
Experience = namedtuple('Experience',
                         field_names=['state','action','reward','done','new_state'])

"""
    This class represents the experince replay buffer that stores the experiences the agent
    acquires. The agent randomly samples batches of experience from this experience replay buffer
    for training. 
"""
class ExperienceReplay:

    """
        We initialize the ExperienceReplay class with a buffer to store experiences.
        The buffer is a deque with maximum length `capacity`
    """
    def __init__(self, capacity):
        self.buffer = collections.deque(maxlen=capacity)

    """
        Returns the number of experiences stored in the experience replay buffer
    """
    def __len__(self):
        return len(self.buffer)
    
    """
        Adds a new experience to the experience replay buffer
    """
    def append(self,experience):
        self.buffer.append(experience)

    """
        Samples a subset of experience without replacement
        during training with size equal to `batch_size`.
        
    """
    def sample(self, batch_size):
        # sets a random seed to ensure reproducibility
        np.random.seed(20)

        indices = np.random.choice(len(self.buffer),
                                     batch_size, replace=False)
        states, actions, rewards, dones, next_states = zip(*[self.buffer[idx] for idx in indices])
        return (np.array(states), np.array(actions), np.array(rewards, dtype=np.float32),
                np.array(dones, dtype=np.uint8), np.array(next_states))