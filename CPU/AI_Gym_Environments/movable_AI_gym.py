import gym
from gym import spaces
import numpy as np

from High_A_Central_Constraints.constraint_operation_toolbox import addConstraint,modifyConstraint,deleteConstraint,substituteConstraint

# This is the RL Agent for the movable constraints (note that this currently follow
# a random policy). This RL agent interacts with the RL boss agent to create optimal
# sports schedules. Even though the actions include add, remove, and substitute, for
# our purpose, we decided to stick with add and remove for simplicity unless Dr. Clark
# says otherwise.

class MovableRLEnv(gym.Env):

  # Here we intialize the AI Gym environment for the RL agent for the movable constraints
  # we pass in the parameters representing the number of movable constraints under
  # consideration (numMovableConstraints),target movable CSP set by the boss agent
  # as well as the constraint library in which we add, remove constraints and solve
  # the problem to produce optimal sports schedules
  # the constraints_to_satisfy represents the list of constraints to satisfy
  # per the league scheduler's random requests
  # gamma represents the discount rate between 0 to 1
  def __init__(self,numMovableConstraints, movable_constraints_to_satisfy,
               target_movable_csp,constraint_library,gamma,immovable_constraints_satisfied):
    super(MovableRLEnv,self).__init__()

    # initializes the instance variables for the number of movable constraints
    # under consideration, as well as the the targeted movable CSP values
    # we use a num_movable_constraints_satisfied variable to track how many
    # movable constraints were added and satisfied so far, as we step through
    # the AI gym environment
    self.num_movable_constraints_to_satisfy = len(movable_constraints_to_satisfy)

    self.num_movable_constraints_satisfied = 0
    self.num_movable_constraints_not_satisfied = self.num_movable_constraints_to_satisfy - self.num_movable_constraints_satisfied

    self.target_movable_csp = target_movable_csp

    # is at least one constraint modified or substituted or both
    # (even if that constraint is deleted)?
    self.at_least_one_constraint_mod_sub = False

    # The states are in the form i where i is the number of movable constraints
    # added and satisfied. For i from numMovableConstraints to 2 * numMovableConstraints
    # exclusive, this represents i - numMovableConstraints added and satisfied where
    # at least one constraint is being substituted.

    self.states = [i for i in range(2 * (numMovableConstraints + 1))]
    #self.observation_space = spaces.Box(low=np.array([0, 0]), high=np.array([self.num_movable_constraints, 1]),
    #                                    dtype=np.uint8)

    # 0 represents add, 1 represents remove for the basic actions
    # 2 represents substitute, 3 represents modify, and 4 represents both modify then substitute for the corrective actions

    self.action_space = gym.spaces.Discrete(5, seed=20)
    # learn the best type of constraints to add, modify, substitute, delete
    #self.action_space = spaces.Box(low = np.array([0, 1, 1]), high = np.array([1, self.num_movable_constraints_satisfied,
    #                                                                          self.num_movable_constraints_not_satisfied]),
    #                               dtype = np.uint8)

    # Initially, no constraints are added and satisfied, so the initial state of the
    # Markov Decision Process is 0 (no constraint is added and satisfied and there
    # have been no substitution)
    #self.curr_state = np.array([0,0])
    self.curr_state = 0

    # the constraint ids that we are working to satisfy (different from the list of
    # constraint ids already added and satisfied)
    self.movable_constraints_to_satisfy = movable_constraints_to_satisfy

    # This list represents the ids of the movable constraints being added and satisfied
    self.satisfied_movable_constraints = []

    
    # The constraint library that the RL agent for the movable constraints is
    # working with (a place where movable constraints are added, removed, and
    # if needed, substituted)
    self.library = constraint_library

    # We will define the rewards in the step function of the AI gym environment
    # to fit with our implementation of the DQN
    # Here we define the cumulative discounted reward
    self.cumulative_reward = 0

    # gamma value
    self.gamma = gamma

    # immovable constraints satisfied
    self.immovable_constraints_satisfied = immovable_constraints_satisfied

    # all the constraints that are satisfied (including the immovable constraints)
    self.satisfied_constraints = (self.satisfied_movable_constraints +
                                self.immovable_constraints_satisfied)

    # add the satisfied movable constraints to the solver of the
    # constraint library
    for constr in self.immovable_constraints_satisfied:
      addConstraint(self.library,constr)

    # the timestep for the calculation of the cumulative discounted reward (initially 0)
    self.curr_timestep = 0

  # Note here we have added a constraint but that constraint is not satisfied, so we need
  # to perform a corrective action (namely in this case it's delete)
  def deleteCorrectiveAction(self, unsatisfied_constraint_to_correct):
    # delete it from the Gurobi constraint library solver
    deleteConstraint(self.library, unsatisfied_constraint_to_correct)
    self.library.solve()

    # number of movable constraints satisfied as well
    # as the list of satisfied movable constraints remain unchanged

    reward = 0  # get no reward
    next_state = self.curr_state
    done = self.getCSP() >= self.target_movable_csp
    self.cumulative_reward += (self.gamma ** self.curr_timestep * reward)
    self.curr_timestep += 1
    return next_state, reward, done, {}
        
  def substituteCorrectiveAction(self, unsatisfied_constraint_to_correct):
    # Here we substitute for a different constraints

    # possible constraints to substitute
    possible_new_constraints = [constr for constr in self.movable_constraints_to_satisfy
                                      if constr != unsatisfied_constraint_to_correct
                                      and constr not in self.satisfied_movable_constraints]
    # to substitute for a new one, we need to delete the old one first
    old_constraint_to_remove = unsatisfied_constraint_to_correct

    # no possible new constraints to substitute for the old one
    if len(possible_new_constraints) == 0:
      # just delete the unsatisfied one
      deleteConstraint(self.library,unsatisfied_constraint_to_correct)
      self.library.solve()

      reward = 0
      next_state = self.curr_state
      done = self.getCSP() >= self.target_movable_csp
      self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
      self.curr_timestep += 1
      return next_state,reward,done,"add"

    np.random.seed(10)
    new_constraint_to_add = np.random.choice(possible_new_constraints)
    substituteConstraint(self.library,unsatisfied_constraint_to_correct,new_constraint_to_add)
    self.library.solve()

    # the newly substituted constraint added and satisfied
    if self.library.isOptimal:
      reward = 0.5  # 0.5 reward since we substituted a constraints but still one more constraint added and satisfied
      if self.at_least_one_constraint_mod_sub == False:
          self.at_least_one_constraint_mod_sub= True
          next_state = self.curr_state + 1 + self.num_movable_constraints_to_satisfy + 1
          self.num_movable_constraints_satisfied += 1
          self.satisfied_movable_constraints.append(new_constraint_to_add)
          self.curr_state = next_state
          done = self.getCSP() >= self.target_movable_csp
          self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
          self.curr_timestep += 1
      else:
          next_state = self.curr_state + 1
          self.num_movable_constraints_satisfied += 1
          self.satisfied_movable_constraints.append(new_constraint_to_add)
          self.curr_state = next_state
          done = self.getCSP() >= self.target_movable_csp
          self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
          self.curr_timestep += 1
      return (next_state,reward,done,"add")
    else: # newly substituted constraint added but not satisfied
            # just delete that newly added constraint from the solver of the
            # constraint library
          deleteConstraint(self.library,new_constraint_to_add)
          self.library.solve()
            
          # the number of satisfied constraints and the status of whether at
          # least one of the satisfied constraints is substituted does not change
          # so we do not change the self.num_movable_constraints_satisfied and
          # the self.satisfied_movable_constraints
          next_state = self.curr_state
          reward = 0 # get no reward
          done = self.getCSP() >= self.target_movable_csp
          self.cumulative_reward = self.cumulative_reward + self.gamma ** (self.curr_timestep)* reward
          self.curr_timestep += 1
          return (next_state,reward,done,{})

  def modifyCorrectiveAction(self,unsatisfied_constraint_to_correct):
    ## Here we modify corrective action for a different constraint
          modifyConstraint(self.library,unsatisfied_constraint_to_correct)
          self.library.solve()

          ## the newly substituted constraint added and satisfied
          if self.library.isOptimal:
            reward = 0.5 ## 0.5 reward since we substituted a constraints
                          ## but still one more constraint added and satisfied
            if self.at_least_one_constraint_mod_sub == False:
              self.at_least_one_constraint_mod_sub= True
              next_state = self.curr_state + 1 + self.num_movable_constraints_to_satisfy + 1
              self.num_movable_constraints_satisfied += 1
              self.satisfied_movable_constraints.append(unsatisfied_constraint_to_correct)
              self.curr_state = next_state
              done = self.getCSP() >= self.target_movable_csp
              self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
              self.curr_timestep += 1
            else:
              next_state = self.curr_state + 1
              self.num_movable_constraints_satisfied += 1
              self.satisfied_movable_constraints.append(unsatisfied_constraint_to_correct)
              self.curr_state = next_state
              done = self.getCSP() >= self.target_movable_csp
              self.cumulative_reward += (self.gamma ** (self.curr_timestep) * reward)
              self.curr_timestep += 1
            return (next_state,reward,done,"add")
          else: ## newly substituted constraint added but not satisfied
            ## just delete that newly added constraint from the solver of the
            ## constraint library
            deleteConstraint(self.library,unsatisfied_constraint_to_correct)
            self.library.solve()
            
            ## the number of satisfied constraints and the status of whether at 
            ## least one of the satisfied constraints is substituted does not change
            ## so we do not change the self.num_movable_constraints_satisfied and
            ## the self.satisfied_movable_constraints
            next_state = self.curr_state
            reward = 0 ## get no reward
            done = self.getCSP() >= self.target_movable_csp
            self.cumulative_reward = self.cumulative_reward + self.gamma ** (self.curr_timestep)* reward
            self.curr_timestep += 1
            return (next_state,reward,done,"add")

  def mod_subCorrectiveAction(self,unsatisfied_constraint_to_correct):
    ## Here we modify corrective action for a different constraint
            modifyConstraint(self.library,unsatisfied_constraint_to_correct)

             ## Here we substitute for a different constraints after modify

            ## possible constraints to substitute
            possible_new_constraints = [constr for constr in self.movable_constraints_to_satisfy
                                        if constr != unsatisfied_constraint_to_correct
                                        and constr not in self.satisfied_movable_constraints]
            ## to substitute for a new one, we need to delete the old one first
            old_constraint_to_remove = unsatisfied_constraint_to_correct

            ## no possible new constraints to substitute for the old one
            if len(possible_new_constraints) == 0:
              ## just delete the unsatisfied one
              deleteConstraint(self.library,unsatisfied_constraint_to_correct)
              self.library.solve()
              reward = 0
              next_state = self.curr_state
              done = self.getCSP() >= self.target_movable_csp
              self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
              self.curr_timestep += 1
              return next_state,reward,done,"add"

            np.random.seed(10)
            new_constraint_to_add = np.random.choice(possible_new_constraints)
            substituteConstraint(self.library,old_constraint_to_remove,new_constraint_to_add)
            self.library.solve()
            
            ## the newly substituted constraint added and satisfied
            if self.library.isOptimal:
              reward = 0.5 ## 0.5 reward since we substituted a constraints
                            ## but still one more constraint added and satisfied
              if self.at_least_one_constraint_mod_sub == False:
                self.at_least_one_constraint_mod_sub= True
                next_state = self.curr_state + 1 + self.num_movable_constraints_to_satisfy + 1
                self.num_movable_constraints_satisfied += 1
                self.satisfied_movable_constraints.append(old_constraint_to_remove)
                self.curr_state = next_state
                done = self.getCSP() >= self.target_movable_csp
                self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
                self.curr_timestep += 1
              else:
                next_state = self.curr_state + 1
                self.num_movable_constraints_satisfied += 1
                self.satisfied_movable_constraints.append(old_constraint_to_remove)
                self.curr_state = next_state
                done = self.getCSP() >= self.target_movable_csp
                self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
                self.curr_timestep += 1
              return (next_state,reward,done,"add")
            else: ## newly substituted constraint added but not satisfied
              ## just delete that newly added constraint from the solver of the
              ## constraint library
              print(f'Subtituted constraint corrective action failed')
              deleteConstraint(self.library,old_constraint_to_remove)
              self.library.solve()

              ## the number of satisfied constraints and the status of whether at 
              ## least one of the satisfied constraints is substituted does not change
              ## so we do not change the self.num_movable_constraints_satisfied and
              ## the self.satisfied_movable_constraints
              next_state = self.curr_state
              reward = 0 ## get no reward
              done = self.getCSP() >= self.target_movable_csp
              self.cumulative_reward = self.cumulative_reward + self.gamma ** (self.curr_timestep)* reward
              self.curr_timestep += 1
              return (next_state,reward,done,"add")

  ## Here we undo the modify action when the constraint after being modified
  ## is not satisfied
  def undoModification(self,constraint_to_modify,prev_values):
    ## only corrective action that makes sense is undo the modification
    
    ## we have different cases for the constraint to modify
    if constraint_to_modify == 'homeOneSideOfASG':
      ## we get the value of 
      ## env.library.allow_home_both_sides_ASG before the modication
      ## deleting the constraint which changes the parameters of the constraint 
      ## back to what it was when the env is initialized
      deleteConstraint(self.library,constraint_to_modify)

      ## the parameters of the constraint_to_modify goes to what it is before
      ## modification
      self.library.allow_home_both_sides_ASG = prev_values
      addConstraint(self.library,constraint_to_modify)
      self.library.solve()

    elif constraint_to_modify == 'NonDivisionalOpponent':
      ## we get the value of 
      ## env.library.upper_non_divisional_games before the modification
      ## deleting the constraint which changes the parameters of the constraint 
      ## back to what it was when the env is initialized
      deleteConstraint(self.library,constraint_to_modify)

      ## the parameters of the constraint_to_modify goes to what it is before
      ## modification
      self.library.upper_non_divisional_games = prev_values
      addConstraint(self.library,constraint_to_modify)
      self.library.solve()
    elif constraint_to_modify == 'EastToWestMaxTwoTravel':
      ## we get the value of 
      ## env.library.max_east_to_west_trips before the modification
      ## deleting the constraint which changes the parameters of the constraint 
      ## back to what it was when the env is initialized
      deleteConstraint(self.library,constraint_to_modify)

      ## the parameters of the constraint_to_modify goes to what it is before
      ## modification
      self.library.max_east_to_west_trips = prev_values
      addConstraint(self.library,constraint_to_modify)
      self.library.solve()
    elif constraint_to_modify == 'WestToEastMaxTwoTravel':
      ## we get the value of 
      ## env.library.max_west_to_east_trips before the modification
      ## deleting the constraint which changes the parameters of the constraint 
      ## back to what it was when the env is initialized
      deleteConstraint(self.library,constraint_to_modify)

      ## the parameters of the constraint_to_modify goes to what it is before
      ## modification
      self.library.max_west_to_east_trips = prev_values
      addConstraint(self.library,constraint_to_modify)
      self.library.solve()
    elif constraint_to_modify == 'PlayNoMoreThanOnceThreeWeeks':
      ## we get the value of 
      ## env.library.max_play_same_opponent before the modification
      ## deleting the constraint which changes the parameters of the constraint 
      ## back to what it was when the env is initialized
      deleteConstraint(self.library,constraint_to_modify)

      ## the parameters of the constraint_to_modify goes to what it is before
      ## modification
      self.library.max_play_same_opponent = prev_values
      addConstraint(self.library,constraint_to_modify)
      self.library.solve()
    elif constraint_to_modify == 'EastTeamsHomeRoadMatchupInDivision':
      ## we get the value of 
      ## env.library.trips_bet_opp_region_spaced before the modification
      ## deleting the constraint which changes the parameters of the constraint 
      ## back to what it was when the env is initialized
      deleteConstraint(self.library,constraint_to_modify)

      ## the parameters of the constraint_to_modify goes to what it is before
      ## modification
      self.library.eastern_one_to_two = prev_values[0]
      self.library.eastern_two_to_two = prev_values[1]
      self.library.eastern_two_to_one = prev_values[2]
      addConstraint(self.library,constraint_to_modify)
      self.library.solve()
    elif constraint_to_modify == 'spacingOppRegionTrips':
       ## we get the value of 
      ## env.library.trips_bet_opp_region_spaced before the modification
      ## deleting the constraint which changes the parameters of the constraint 
      ## back to what it was when the env is initialized
      deleteConstraint(self.library,constraint_to_modify)

      ## the parameters of the constraint_to_modify goes to what it is before
      ## modification
      self.library.trips_bet_opp_region_spaced = prev_values
      addConstraint(self.library,constraint_to_modify)
      self.library.solve()
    
    ## deleting the constraint which changes the parameters of the constraint 
    ## back to what it was when the env is initialized
    deleteConstraint(self.library,constraint_to_modify)

    ## the parameters of the constraint_to_modify changes
    addConstraint(self.library,constraint_to_modify)
    self.library.solve()

  ## get the previous values of the parameters of the constraint before
  ## modification for the sake of undoing the modification
  def getPreviousParameterValues(self,constraint_to_modify):

    if constraint_to_modify == 'homeOneSideOfASG':
      ## we get the value of 
      ## env.library.allow_home_both_sides_ASG before the modication
      return self.library.allow_home_both_sides_ASG
    elif constraint_to_modify == 'NonDivisionalOpponent':
      return self.library.upper_non_divisional_games
    elif constraint_to_modify == 'EastToWestMaxTwoTravel':
      return self.library.max_east_to_west_trips
    elif constraint_to_modify == 'WestToEastMaxTwoTravel':
      return self.library.max_west_to_east_trips
    elif constraint_to_modify == 'PlayNoMoreThanOnceThreeWeeks':
      return self.library.max_play_same_opponent
    elif constraint_to_modify == 'EastTeamsHomeRoadMatchupInDivision':
      return (self.library.eastern_one_to_two,
              self.library.eastern_two_to_two,
              self.library.eastern_two_to_one)
    elif constraint_to_modify == 'spacingOppRegionTrips':
      return self.library.trips_bet_opp_region_spaced

  ## This is the step function of the AI Gym environment for the movable constraints
  ## we take in an action (which is add or remove for simplicity). We write the outputs
  ## to the console to check that the environment is working correctly
  def step_v2(self, action):
    action_type = action[0]
    print(f'Action type is {action_type}')

  ## This is the step function of the AI Gym environment for the movable constraints
  ## we take in an action (which is add or remove for simplicity). We write the outputs
  ## to the console to check that the environment is working correctly
  def step(self,action):
    ## Here the add is chosen
    if action ==  0:
      ## get a list of non satisfied constraints
      non_satisfied_constrants = [constr for constr in self.movable_constraints_to_satisfy
                                  if constr not in self.satisfied_movable_constraints]

      ## maximum number of constraints reached so cannot add one more and we just
      ## return and get zero reward
      if len(non_satisfied_constrants) == 0:
        #print('Maximum number of constraints reached at ',self.num_movable_constraints)
        next_state = self.curr_state
        reward = -2 ## negative reward to discourage such action
        done = self.getCSP() >= self.target_movable_csp
        self.cumulative_reward += (self.gamma ** (self.curr_timestep) * reward)
        self.curr_timestep += 1
        return next_state,reward,done,{}

      ## we choose a random constraint to add from the list of unsatisfied movable constraints
      ## to simulate the randomness of the next state given the current state (the number of movable
      ## constraints added and satisfied) and the action add
      np.random.seed(10)
      movable_constraint_to_add = np.random.choice(non_satisfied_constrants)

      # print(f'To add {movable_constraint_to_add}')
      
      ## we log to the console the movable constraint
      ## we are trying to add. 
      #print(f'the movable constraint to add is {movable_constraint_to_add}')

      ## call the addConstraint taking in the constraint to add
      addConstraint(self.library,movable_constraint_to_add)
      self.library.solve()

      ## constraint added and satisfied
      if self.library.isOptimal:
        #print('constraint added and satisfied')
        next_state = self.curr_state + 1
        reward = +1 ## +1 reward for each additional constraint added and satisfied
        self.curr_state = next_state
        self.num_movable_constraints_satisfied += 1
        self.satisfied_movable_constraints.append(movable_constraint_to_add)
        done = self.getCSP() >= self.target_movable_csp
        self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
        self.curr_timestep += 1
        return next_state,reward,done, {}
      else: ## constraint added but not satisfied
        #print(f'Correction Needed')
        np.random.seed(10)
        corrective_action = np.random.choice(['delete','substitute','modify','modify_sub'])
        #print(f'Corrective action is {corrective_action}')
        if corrective_action == 'delete':
          return self.deleteCorrectiveAction(movable_constraint_to_add)
        elif corrective_action == 'substitute':
          return self.substituteCorrectiveAction(movable_constraint_to_add)
        elif corrective_action == 'modify':
          return self.modifyCorrectiveAction(movable_constraint_to_add)
        elif corrective_action == 'modify_sub':
          return self.mod_subCorrectiveAction(movable_constraint_to_add)
        
    elif action == 1: ## Here, 1 corresponds to remove
      if len(self.satisfied_movable_constraints) == 0:
        ## no constraint added and satisfied so we cannot remove
        # print('No constraint to remove')
        reward = -2 ## negative reward to discourage such action
        next_state = self.curr_state
        done = self.getCSP() >= self.target_movable_csp
        self.cumulative_reward = self.cumulative_reward + self.gamma ** (self.curr_timestep)* reward
        self.curr_timestep += 1
        return next_state,reward,done,action
      

      ## we randomly choose between none (which signifies that we are not removing any constraint)
      ## and the constraint to remove (among the list of constraints under consideration - which is distinct
      ## from the list of satisfied constraints). This means that it might be the case that the constraint we
      ## are trying to remove is not in the list of satisfied constraints, and we will have to print an error message
      np.random.seed(10)
      movable_constraint_to_remove = np.random.choice(self.satisfied_movable_constraints)

      ## we will then call the deleteConstraint passing in the movable_constraint_to_remove and the outputFile
      deleteConstraint(self.library,movable_constraint_to_remove)
      self.library.solve()

      reward = -1 ## -1 since we deleted a constraint
      self.num_movable_constraints_satisfied -= 1

      next_state = self.curr_state - 1

      self.curr_state = next_state
      ## remove that constraint from the list of satisfied constraints
      self.satisfied_movable_constraints.remove(movable_constraint_to_remove)
      done = self.getCSP() >= self.target_movable_csp
      self.cumulative_reward = self.cumulative_reward + self.gamma ** (self.curr_timestep)* reward
      self.curr_timestep += 1
      return next_state,reward,done,action
    elif action == 2:
      non_satisfied_movable_constraints = [constr for constr in self.movable_constraints_to_satisfy if
                                   constr not in self.satisfied_movable_constraints]

      ## corresponds to the substitute action
      if len(non_satisfied_movable_constraints) == 0:
        ## no new unsatisfied constraint to substitute so we cannot substitute
        reward =-2 ## induce negative reward
        next_state = self.curr_state
        done = self.getCSP() >= self.target_movable_csp
        self.cumulative_reward += (self.gamma ** (self.curr_timestep) * reward)
        self.curr_timestep += 1
        return next_state,reward,done,action

      if len(self.satisfied_movable_constraints) == 0:
        reward = -2 ## no satisfied movable constraints to substitute, so negative reward
        next_state = self.curr_state
        done = self.getCSP() >= self.target_movable_csp
        self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
        self.curr_timestep += 1
        return next_state,reward,done,action

      np.random.seed(10)
      old_constraint_to_remove = np.random.choice(self.satisfied_movable_constraints)

      ## remove that old constraint from the list of satisfied constraints
      self.satisfied_movable_constraints.remove(old_constraint_to_remove)

      np.random.seed(10)
      new_constraint_to_add = np.random.choice(non_satisfied_movable_constraints)
      substituteConstraint(self.library,old_constraint_to_remove,new_constraint_to_add)
      self.library.solve()

      ## new constraint added and satisfied and replaced the old constraint to 
      ## be substituted
      if self.library.isOptimal:
        ## the number of movable constraints satisfied does not change
        ## since we just removed a satisfied movable constraint and replaced 
        ## it with the new one
        ## but we add that new constraint to the list of satisfied constraints
        self.satisfied_movable_constraints.append(new_constraint_to_add)

        if self.at_least_one_constraint_mod_sub == False:
          self.at_least_one_constraint_mod_sub = True
          
          ## next_state represent the same number of movable constraints
          ## added and satisfied where at least one of the satisfied constraints
          ## is substituted
          next_state = self.curr_state + self.num_movable_constraints_to_satisfy+1
          self.curr_state = next_state

          ## number of movable constraint satisfied does not change
          reward = 0 ## no reward since there is no additional constraint added and satisfied

          done = self.getCSP() >= self.target_movable_csp
          self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
          self.curr_timestep += 1
          return (next_state,reward,done,action)
        else:
          next_state = self.curr_state
          reward = 0
          done = self.getCSP() >= self.target_movable_csp
          self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
          self.curr_timestep += 1
          return (next_state,reward,done,action)

      else: ## new constraint added but not satisfied
        ## all the backtracking action is to undo the substitution and 
        ## add back the deleted constraint which is already satisfied before
        ## substitute the new (but unsatisfied constraint) with the original one that
        ## the agent intends to replace
        substituteConstraint(self.library,new_constraint_to_add,old_constraint_to_remove)
        next_state = self.curr_state ## no change in the state
        reward = 0 ## no reward since no successful substitution
        done = self.getCSP() >= self.target_movable_csp
        return (next_state,reward,done,action)

    elif action == 3: ## Here we chose modify
      # Here we have no satisfied immovable constraints to modify
      if len(self.satisfied_movable_constraints) == 0:
        reward = -2 ## negative reward to discourage such action
        next_state = self.curr_state
        done = self.getCSP() >= self.target_movable_csp
        return (next_state,reward,done,action)

      np.random.seed(10)
      constraint_to_modify = np.random.choice(self.satisfied_movable_constraints)
      
      prev_value = self.getPreviousParameterValues(constraint_to_modify)
      
      modifyConstraint(self.library,constraint_to_modify)
      self.library.solve()

      ## modified constraint satisfied (at least one modification performed)
      if self.library.isOptimal:
        if self.at_least_one_constraint_mod_sub == False:
          self.at_least_one_constraint_mod_sub = True

          ## does not change the number of constraints added and satisfied
          next_state = self.curr_state + self.num_movable_constraints_to_satisfy + 1
          self.curr_state = next_state
          reward = +0.5 # +0.5 for a successful modification
          done = self.getCSP() >= self.target_movable_csp
          return (next_state,reward,done,action)
        else:
          next_state = self.curr_state ## no change in state since no additional constraint added and satisfied
          reward = +0.5
          done = self.getCSP() >= self.target_movable_csp
          return (next_state,reward,done,action)
        
      else: ## modified constraint is not satisfied, so we need to take corrective action
        ## only corrective action that makes sense is undo the modification

        ## deleting the constraint which changes the parameters of the constraint back to what it was when the env is intialized
        #deleteConstraint(self,constraint_to_modify)

        ## the parameters of the constraint_to_modify changes
        #addConstraint(self,constraint_to_modify)
        self.undoModification(constraint_to_modify,prev_value)

        ## after the modification is undone, there is no reward, and no change in state (because of no successful modifcation)
        next_state = self.curr_state
        reward = 0
        done = self.getCSP() >= self.target_movable_csp
        return (next_state,reward,done,action)

    elif action == 4: ## modify then substitute
      if len(self.satisfied_movable_constraints) == 0:
        ## no satisfied constraints to modify or substitute
        ## state don't change and there's negative reward
        next_state = self.curr_state
        reward = -2
        done = self.getCSP() >= self.target_movable_csp
        return (next_state,reward,done,action)

      ## list of non-satisfied constraints for which we can replace satisfied constraints
      non_satisfied_movable_constraints = [constr for constr in self.movable_constraints_to_satisfy
                                  if constr not in self.satisfied_movable_constraints]
      
      ## no new constraint to replace old one
      if len(non_satisfied_movable_constraints) == 0:
        next_state = self.curr_state
        reward = -2 ## negative reward to discourage such action
        done = self.getCSP() >= self.target_movable_csp
        return (next_state,reward,done,action)

      np.random.seed(10)
      old_constraint_to_modify_then_remove = np.random.choice(self.satisfied_movable_constraints)

      #print('Constraint to modify is ',old_constraint_to_modify_then_remove)

      

      ## get the previous values of the parameters before the modify to help with undo the modify part
      prev_value = self.getPreviousParameterValues(old_constraint_to_modify_then_remove)

      constraint_to_modify = old_constraint_to_modify_then_remove
      
      
      ## performs the modify and then substitute action
      modifyConstraint(self.library,constraint_to_modify)

      np.random.seed(10)
      new_constraint_to_add = np.random.choice(non_satisfied_movable_constraints)

      substituteConstraint(self.library,constraint_to_modify,new_constraint_to_add)

      self.library.solve()

      ## modified and then substituted constraint satisfied (at least one modification performed)
      if self.library.isOptimal:
        if self.at_least_one_constraint_mod_sub == False:
          self.at_least_one_constraint_mod_sub = True

          ## does not change the number of constraints added and satisfied
          next_state = self.curr_state + self.num_movable_constraints_to_satisfy + 1
          self.curr_state = next_state
          reward = +0.5 # +0.5 for a successful modification
          done = self.getCSP() >= self.target_movable_csp
          return (next_state,reward,done,action)
        else:
          next_state = self.curr_state ## no change in state since no additional constraint added and satisfied
          reward = +0.5
          done = self.getCSP() >= self.target_movable_csp
          return (next_state,reward,done,action)
        
      else: ## modified constraint is not satisfied, so we need to take corrective action
        ## only corrective action that makes sense is undo the modification

        ## undo the substitution
        substituteConstraint(self.library,new_constraint_to_add,constraint_to_modify)

        ## undo the modification
        self.undoModification(old_constraint_to_modify_then_remove,prev_value)
        
        ## the parameters of the old_constraint_to_modify_then_remove changes to default upon deletion
        #deleteConstraint(self,old_constraint_to_modify_then_remove)

        ## adding back the original non-modified constraint
        #addConstraint(self,old_constraint_to_modify_then_remove)

        ## after the modification is undone, there is no reward, and no change in state (because of no successful modifcation)
        next_state = self.curr_state
        reward = 0
        done = self.getCSP() >= self.target_movable_csp
        return (next_state,reward,done,action)

    ## Here we just raise a ValueError when the action is anything
    ## other than add or remove or substitute
    else:
      raise ValueError(f'action{action} not part of action space')
  
  ## Here, we will add a constraint to the constraint library that the RL agent for
  ## the movable constraints has access to (namely, self.constraint_library). We take
  ## in the ID of the constraint to be added


  ## Note here that the reset of the AI gym environment, which is not present in this file
  ## when we submitted the Design Day poster, simply resets the environment back to the starting state
  ## for future use. For this function,
  ## we will clear the cumulative rewards, the list of satisfied constraint ids, as well
  ## as bring current state of the Markov Decision Process back to c0, the starting state
  def reset(self):
    self.curr_state = 0
    self.curr_reward = 0
    self.satisfied_movable_constraints = []

    ## the immovable constraints satisfied do not get deleted
    self.satisfied_constraints = self.immovable_constraints_satisfied

    self.num_movable_constraints_satisfied = 0
    self.library.__init__()
    self.cumulative_reward = 0
    self.at_least_one_constraint_mod_sub = False

    ## goes back to the 0th timestep
    self.curr_timestep = 0
    
    for constr in self.immovable_constraints_satisfied:
      addConstraint(self.library,constr)

    self.curr_timestep = 0 ## timestep goes back to 0 for future use
    return 0 ## return the initial state which is 0


  ## Here, the RL agent for the movable constraints will get the CSP value 
  ## based on the number of satisfie movable constraints over the number of movable 
  ## constraints to satisfy. The RL agent will then use this value to determine whether 
  ## the target movable CSP value is then met
  def getCSP(self):
    return self.num_movable_constraints_satisfied / self.num_movable_constraints_to_satisfy

  ## This is the render method of the AI gym environment for the movable constraint 
  ## RL agent. Note here that we are using a randomly policy and haven't introduced discounting yet
  ## This is an episodic task as we are doing a finite number of iterations. 
  ## We use that method to check that each constraint is added and satisfied as we step through the
  ## AI gym framework
  def render(self, output_file):
    print('\nRendering the Movable AI Gym Environment.\nThe percent of movable constraints satisfied (intermediate movable CSP) are ',
      self.getCSP(), file=output_file)
    print('The movable constraints satisfied are ', self.satisfied_movable_constraints, file=output_file)
    print('The curr_state is ', self.curr_state, file=output_file)
    print('The cumulative discounted reward received so far is ', self.cumulative_reward, file=output_file)

    
    

  