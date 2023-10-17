import gym
import gym.spaces
import numpy as np

from High_A_Central_Constraints.constraint_operation_toolbox import addConstraint,deleteConstraint,substituteConstraint

# This is the RL Agent for the immovable constraints (note that this currently follow
# a random policy). This RL agent interacts with the RL boss agent to create optimal
# sports schedules. Even though the actions include add, remove, and substitute, for
# our purpose, we decided to stick with add and remove for simplicity unless Dr. Clark
# says otherwise.


class ImmovableRLEnv(gym.Env):

  # Here we intialize the AI Gym environment for the RL agent for the immovable constraints
  # we pass in the parameters representing the number of immovable constraints under
  # consideration (numImmovableConstraints),target immovable CSP set by the boss agent
  # as well as the constraint library in which we add, remove constraints and solve
  # the problem to produce optimal sports schedules
  # the constraints_to_satisfy represents the list of constraints to satisfy
  # per the league scheduler's random requests
  # gamma represents the discount rate between 0 to 1
  def __init__(self, numImmovableConstraints, constraints_to_satisfy,
               target_immovable_csp, constraintLibrary, gamma):
    super(ImmovableRLEnv, self).__init__()

    # initializes the instance variables for the number of immovable constraints
    # under consideration, as well as the targeted immovable CSP values
    # we use a num_immovable_constraints_satisfied variable to track how many
    # immovable constraints were added and satisfied so far, as we step through
    # the AI gym environment
    self.num_immovable_constraints = numImmovableConstraints
    self.num_immovable_constraints_satisfied = 0
    self.target_immovable_csp = target_immovable_csp

    # is at least one constraint substituted?
    self.at_least_one_constraint_substituted = False

    # The states are in the form i where i is the number of immovable constraints
    # added and satisfied. For i from numImmovableConstraints to 2 * numImmovableConstraints
    # exclusive, this represents i - numImmovableConstraints added and satisfied where
    # at least one constraint is being substituted.

    self.states = [i for i in range(2 * (numImmovableConstraints + 1))]
    #self.states = gym.spaces.Box(low=[0,0], high )

    # 0 represents add, 1 represents remove, and 2 represents substitute
    self.action_space = gym.spaces.Discrete(3, seed=20)

    # Initially, no constraints are added and satisfied, so the initial state of the
    # Markov Decision Process is 0 (no constraint is added and satisfied and there
    # have been no substitution)
    self.curr_state = 0

    # the constraint ids that we are working to satisfy (different from the list of
    # constraint ids already added and satisfied)
    self.constraints_to_satisfy = constraints_to_satisfy

    # This list represents the ids of the constraints being added and satisfied
    self.satisfied_constraints = []

    # the constraint library that the RL agent for the immovable constraints is
    # working with (a place where immovable constraints are added, removed, and
    # if needed, substituted)
    self.library = constraintLibrary

    # We will define the rewards in the step function of the AI gym environment
    # to fit with our implementation of the DQN
    # Here we define the cumulative discounted reward
    self.cumulative_reward = 0

    # gamma value
    self.gamma = gamma

    # timestamp index to calculate the discounted reward (initially 0)
    self.curr_timestep = 0
  
  # This is the step function of the AI Gym environment for the immovable constraints
  # we take in an action (which is add or remove for simplicity). We write the outputs
  # to the console to check that the environment is working correctly
  def step(self,action):
    # Here the add is chosen
    if action ==  0:

      
      
      # get a list of non satisfied constraints
      non_satisfied_constrants = [constr for constr in self.constraints_to_satisfy
                                  if constr not in self.satisfied_constraints]

      # maximum number of constraints reached so cannot add one more and we just
      # return and get zero reward
      if len(non_satisfied_constrants) == 0:
        # print('Maximum number of constraints reached at ',self.num_immovable_constraints)
        next_state = self.curr_state
        reward = -2 ## negative reward to discourage such action
        done = self.getCSP() >= self.target_immovable_csp
        self.cumulative_reward += (self.gamma ** self.curr_timestep * reward)

        # increment the timestep by 1
        self.curr_timestep += 1
        return next_state,reward,done,action

      # we choose a random constraint to add from the list of unsatisfied immovable constraints
      # to simulate the randomness of the next state given the current state (the number of immovable
      # constraints added and satisfied) and the action add
      np.random.seed(10)
      immovable_constraint_to_add = np.random.choice(non_satisfied_constrants)

      
      # we log to the console the immovable constraint
      # we are trying to add.
      # print(f'the immovable constraint to add is {immovable_constraint_to_add}')

      # call the addConstraint taking in the constraint to add
      addConstraint(self.library,immovable_constraint_to_add)
      self.library.solve()

      # constraint added and satisfied
      if self.library.isOptimal:
        # print('constraint added and satisfied')
        next_state = self.curr_state + 1
        reward = +1 ## +1 reward for each additional constraint added and satisfied
        self.curr_state = next_state
        self.num_immovable_constraints_satisfied += 1
        self.satisfied_constraints.append(immovable_constraint_to_add)
        done = self.getCSP() >= self.target_immovable_csp
        self.cumulative_reward += (self.gamma ** (self.curr_timestep) * reward)
        self.curr_timestep += 1
        return next_state,reward,done,action
      else: # constraint added but not satisfied
        # try to go through both delete and substitute corrective action
        np.random.seed(10)
        corrective_action = np.random.choice(['delete','substitute'])
        if corrective_action == 'substitute':
          # Here we substitute for a different constraints

          # possible constraints to substitute
          possible_new_constraints = [constr for constr in self.constraints_to_satisfy
                                      if constr != immovable_constraint_to_add
                                      and constr not in self.satisfied_constraints]
          # to substitute for a new one, we need to delete the old one first
          old_constraint_to_remove = immovable_constraint_to_add

          # no possible new constraints to substitute for the old one
          if len(possible_new_constraints) == 0:
            # just delete the unsatisfied one
            deleteConstraint(self.library,immovable_constraint_to_add)
            self.library.solve()

            reward = -2
            next_state = self.curr_state
            done = self.getCSP() >= self.target_immovable_csp
            self.cumulative_reward += (self.gamma **(self.curr_timestep)* reward)
            self.curr_timestep += 1
            return next_state,reward,done,action

          np.random.seed(10)
          new_constraint_to_add = np.random.choice(possible_new_constraints)
          substituteConstraint(self.library,old_constraint_to_remove,new_constraint_to_add)
          self.library.solve()

          # the newly substituted constraint added and satisfied
          if self.library.isOptimal:
            reward = 0.5 # 0.5 reward since we substituted a constraints
                        # but still one more constraint added and satisfied
            if self.at_least_one_constraint_substituted == False:
              self.at_least_one_constraint_substituted = True
              next_state = self.curr_state + 1 + self.num_immovable_constraints + 1
              self.num_immovable_constraints_satisfied += 1
              self.satisfied_constraints.append(new_constraint_to_add)
              self.curr_state = next_state
              done = self.getCSP() >= self.target_immovable_csp
              self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)

              # increment timestep by 1
              self.curr_timestep += 1
            else:
              next_state = self.curr_state + 1
              self.num_immovable_constraints_satisfied += 1
              self.satisfied_constraints.append(new_constraint_to_add)
              self.curr_state = next_state
              done = self.getCSP() >= self.target_immovable_csp
              self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
              self.curr_timestep += 1
            return (next_state,reward,done,action)
          else: # newly substituted constraint added but not satisfied
            # just delete that newly added constraint from the solver of the
            # constraint library
            deleteConstraint(self.library,new_constraint_to_add)
            self.library.solve()
            
            # the number of satisfied constraints and the status of whether at
            # least one of the satisfied constraints is substituted does not change
            # so we do not change the self.num_immovable_constraints_satisfied and
            # the self.satisfied_constraints
            next_state = self.curr_state
            reward = 0 # get no reward
            done = self.getCSP() >= self.target_immovable_csp
            self.cumulative_reward = self.cumulative_reward + self.gamma ** (self.curr_timestep)* reward
            self.curr_timestep += 1
            return (next_state,reward,done,action)
        
        elif corrective_action == 'delete':
          # print('delete corrective action is underway')
          # delete it from the OR tool constraint library solver
          deleteConstraint(self.library,immovable_constraint_to_add)
          self.library.solve()

          # number of immovable constraints satisfied as well
          # as the list of satisfied immovable constraints remain unchanged

          reward = 0 # get no reward
          next_state = self.curr_state
          done = self.getCSP() >= self.target_immovable_csp
          self.cumulative_reward += (self.gamma ** (self.curr_timestep) * reward)
          self.curr_timestep += 1
          return next_state,reward,done,action
        
    elif action == 1: # Here, 1 corresponds to remove
      if len(self.satisfied_constraints) == 0:
        # no constraint added and satisfied so we cannot remove
        # print('No constraint to remove')
        reward = -2 # negative reward to discourage such action
        next_state = self.curr_state
        done = self.getCSP() >= self.target_immovable_csp
        self.cumulative_reward = self.cumulative_reward + self.gamma ** (self.curr_timestep)* reward
        self.curr_timestep += 1
        return next_state,reward,done,action
      

      # we randomly choose between none (which signifies that we are not removing any constraint)
      # and the constraint to remove (among the list of constraints under consideration - which is distinct
      # from the list of satisfied constraints). This means that it might be the case that the constraint we
      # are trying to remove is not in the list of satisfied constraints, and we will have to print an error message
      np.random.seed(10)
      immovable_constraint_to_remove = np.random.choice(self.satisfied_constraints)

      # we will then call the deleteConstraint passing in the immovable_constraint_to_remove and the outputFile
      deleteConstraint(self.library,immovable_constraint_to_remove)
      self.library.solve()

      reward = -1 # -1 since we deleted a constraint
      self.num_immovable_constraints_satisfied -= 1

      next_state = self.curr_state - 1

      self.curr_state = next_state

      # remove that constraint from the list of satisfied constraints
      self.satisfied_constraints.remove(immovable_constraint_to_remove)
      done = self.getCSP() >= self.target_immovable_csp
      self.cumulative_reward = self.cumulative_reward + self.gamma ** (self.curr_timestep)* reward
      self.curr_timestep += 1
      return next_state,reward,done,action
    elif action == 2:
      non_satisfied_constraints = [constr for constr in self.constraints_to_satisfy if
                                   constr not in self.satisfied_constraints]

      # corresponds to the substitute action
      if len(non_satisfied_constraints) == 0:
        # no new unsatisfied constraint to substitute so we cannot substitute
        reward = -2 # negative reward to discourage such action
        next_state = self.curr_state
        done = self.getCSP() >= self.target_immovable_csp
        self.cumulative_reward += (self.gamma ** (self.curr_timestep) * reward)
        self.curr_timestep += 1
        return next_state,reward,done,action

      if len(self.satisfied_constraints) == 0:
        reward = -2 # negative reward to discourage such action
        next_state = self.curr_state
        done = self.getCSP() >= self.target_immovable_csp
        self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
        self.curr_timestep += 1
        return next_state,reward,done,action

      np.random.seed(10)
      old_constraint_to_remove = np.random.choice(self.satisfied_constraints)

      # remove that old constraint from the list of satisfied constraints
      self.satisfied_constraints.remove(old_constraint_to_remove)

      np.random.seed(10)
      new_constraint_to_add = np.random.choice(non_satisfied_constraints)
      substituteConstraint(self.library,old_constraint_to_remove,new_constraint_to_add)
      self.library.solve()

      # new constraint added and satisfied and replaced the old constraint to
      # be substituted
      if self.library.isOptimal:
        # the number of immovable constraints satisfied does not change
        # since we just removed a satisfied immovable constraint and replaced
        # it with the new one
        # but we add that new constraint to the list of satisfied constraints
        self.satisfied_constraints.append(new_constraint_to_add)

        if self.at_least_one_constraint_substituted == False:
          self.at_least_one_constraint_substituted = True
          
          # next_state represent the same number of immovable constraints
          # added and satisfied where at least substitution is performed
          next_state = self.curr_state + self.num_immovable_constraints + 1
          self.curr_state = next_state

          # number of immovable constraint satisfied does not change
          reward = 0 ## no reward since there is no additional constraint added and satisfied

          done = self.getCSP() >= self.target_immovable_csp
          self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)

          self.curr_timestep += 1
          return (next_state,reward,done,action)
        else:
          next_state = self.curr_state
          reward = 0
          done = self.getCSP() >= self.target_immovable_csp
          self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
          self.curr_timestep += 1
          return (next_state,reward,done,action)

      else: # new constraint added but not satisfied
        # backtracking action involve undoing the substitution
        substituteConstraint(self.library,new_constraint_to_add,old_constraint_to_remove)
        self.library.solve()
        reward = 0
        next_state = self.curr_state # state does not change since the action is undone
        done = self.getCSP() >= self.target_immovable_csp
        self.cumulative_reward += (self.gamma ** (self.curr_timestep)* reward)
        self.curr_timestep += 1
        return (next_state,reward,done,action)
    
    # Here we just raise a ValueError when the action is anything
    # other than add or remove or substitute
    else:
      raise ValueError(f'action{action} not part of action space')

  # Note here that the reset of the AI gym environment, which is not present in this file
  # when we submitted the Design Day poster, simply resets the environment back to the starting state
  # for future use. For this function,
  # we will clear the cumulative rewards, the list of satisfied constraint ids, as well
  # as bring current state of the Markov Decision Process back to c0, the starting state
  def reset(self):
    self.curr_state = 0
    self.curr_reward = 0
    self.satisfied_constraints = []
    self.num_immovable_constraints_satisfied = 0
    self.library.__init__()
    self.cumulative_reward = 0

    # reset the timestep back to 0
    self.curr_timestep = 0

    # the indicator to whether at least one constraint has been substituted becomes false
    self.at_least_one_constraint_substituted = False
    
    return self.curr_state # return the initial state which is 0


  # Here, the RL agent for the immovable constraints will get the CSP value
  # based on the number of satisfie immovable constraints over the number of immovable
  # constraints to satisfy. The RL agent will then use this value to determine whether
  # the target immovable CSP value is then met
  def getCSP(self):
    return self.num_immovable_constraints_satisfied / self.num_immovable_constraints
  
  # This is the render method of the AI gym environment for the immovable constraint
  # RL agent. Note here that we are using a randomly policy and haven't introduced discounting yet
  # This is an episodic task as we are doing a finite number of iterations.
  # We use that method to check that each constraint is added and satisfied as we step through the
  # AI gym framework
  def render(self, output_file):
    print(f'\nRendering the Immovable AI Gym Environment for gamma of {self.gamma}', file=output_file)
    print(f'The percent of immovable constraints satisfied (intermediate immovable CSP) are {self.getCSP()}', file=output_file)
    print(f'Has at least one immovable constraint be substituted throughout? {self.at_least_one_constraint_substituted}',
          file=output_file)
    print(f'The target immovable CSP is {self.target_immovable_csp}', file=output_file)
    print(f'The immovable constraints satisfied are {self.satisfied_constraints}', file=output_file)
    print(f'The curr_state is {self.curr_state}', file=output_file)
    print(f'The cumulative discounted reward received so far is {self.cumulative_reward}', file=output_file)