import torch.nn as nn
"""
This is the Deep Q Network that implements the DQN for the Baseball 
# Scheduling for the High A Central division and is able to adapt this to 
# both the RL agent for the movable constraints and that of the immovable 
# constraints. Note that we will use this formulation for both the target
# network and the predictive network for our problem

"""
class DQN(nn.Module):
  """
  This function initializes the Deep Q Network through taking in
  the shape of the input state (input_shape), the number of actions
  in the output layer (n_actions), and whether he initialization is
  used (he_initialization)
  """
  def __init__(self, input_shape, n_actions, he_initialization):
    super(DQN, self).__init__()

    """
        Our Deep Q Networks consists of only fully connected layers
        with three hidden layers of 512 nodes, 256 nodes, and 128 nodes
        with ReLU activation functions in between
    """
    self.fc = nn.Sequential(
        nn.Linear(input_shape[0], 512),
        nn.ReLU(),
        nn.Linear(512, 256),
        nn.ReLU(),
        nn.Linear(256, 128),
        nn.ReLU(),
        nn.Linear(128, n_actions)
    )

    """
        If he initialization is set to true,
        we perform He Initialization of the weights of 
        each of the layers that are of the form nn.Linear
    """
    if he_initialization:
        for layer in self.fc:
            if isinstance(layer, nn.Linear):
                nn.init.kaiming_normal_(layer.weight)

  """
    This function computes the forward propagation of the Deep Q Network
  """
  def forward(self, x):
    return self.fc(x)