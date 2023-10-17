import numpy as np

## This represents the boss[rule-based] RL agent in the hierarchical open reinforcement learning
## framework between the boss RL agent as well as the RL agent for the movable and immovable constraints
## The boss RL agent (representing the league scheduler) makes random requests based on the possible
## list of movable and immovable constraints. The boss RL agent also determines the target immovable and movable
## CSP values in which they are then passed on to the RL agents for the immovable and movable constraints
## It is the role of the immovable and movable constraints RL agents to learn the framework as well as the interaction
## with the RL boss agent to create satisfying baseball season schedule. 
class RLAgentBoss:
    ## This class represents the Boss RL agent in the process
    def __init__(self, target_immovable_csp, target_movable_csp, weight_immovable_csp, weight_movable_csp,
                 immovable_constraints_request, movable_constraints_request, num_immovable_constraints_to_satisfy,
                 num_movable_constraints_to_satisfy):
        self.target_immovable_csp = target_immovable_csp
        self.target_movable_csp = target_movable_csp
        self.weight_immovable_csp = weight_immovable_csp
        self.weight_movable_csp = weight_movable_csp
        self.immovable_constraints_request = immovable_constraints_request
        self.movable_constraints_request = movable_constraints_request
        self.num_immovable_constraints_to_satisfy = num_immovable_constraints_to_satisfy
        self.num_movable_constraints_to_satisfy = num_movable_constraints_to_satisfy
    
    ## make a request of immovable constraints to satisfy
    ## we will use this to test various combinations of constraints for the Deep Q Learning
    ## process for the immovable RL agent. 
    def makeImmovableConstraintRequests(self,immovable_constraints_list, num_immovable_constraints):
        ## the league scheduler first determine how many of the immovable constraints to 
        ## satisfy
        max_constraints = len(immovable_constraints_list)
        #num_immovable_constraints_to_satisfy = np.random.randint(1,max_constraints)

        ## out of a possible list of immovable constraints to satisfy, the league scheduler
        ## chooses randomly num_immovable_constraints_to_satisfy immovable constraints
        ## to simulate the real-time scheduling demands as well as league scheduler's random requests
        constraints_to_satisfy_immovable = np.random.choice(immovable_constraints_list,
                                                            num_immovable_constraints,
                                                            replace = False)
        return list(constraints_to_satisfy_immovable)

    ## make a request of movable constraints to satisfy as well as the extent of which
    ## they can be modified
    def makeMovableConstraintRequests(self,movable_constraints_list, num_movable_constraints):
      ## the league scheduler first determine how many of the immovable constraints to 
      ## satisfy
      max_constraints = len(movable_constraints_list)

      #num_movable_constraints_to_satisfy = np.random.randint(1,max_constraints)

      ## out of a possible list of immovable constraints to satisfy, the league scheduler
      ## chooses randomly num_immovable_constraints_to_satisfy immovable constraints
      ## to simulate the real-time scheduling demands as well as league scheduler's random requests
      constraints_to_satisfy_immovable = np.random.choice(movable_constraints_list,
                                                          num_movable_constraints
                                                          ,replace = False)
      return list(constraints_to_satisfy_immovable)

    ## Based on the immovable_csp_value acheived by the trained RL agent for the immovable
    ## constraints and movable_csp_value achieved the trained RL agent for the movable 
    ## constraints when the target CSP values are met, we use that formula to calculate the
    ## schedule score to represent the agents' performances. 
    def calculateScheduleScore(self,immovable_csp_value,movable_csp_value):
        return (self.weight_immovable_csp * immovable_csp_value 
                + self.weight_movable_csp * movable_csp_value)