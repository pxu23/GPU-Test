# This is the functions for the training with the Deep Q Learning
from operator import mod

import matplotlib.pyplot as plt
import torch
import numpy as np
import torch.nn as nn
import datetime
import time

# trains the immovable RL agent
# function to train the immovable RL agent and returns the loss history
def trainImmovableAgent(batch_size,learning_rate,
                        sync_target_frames, replay_size,
                        replay_start_size,eps_start,
                        eps_decay, eps_min, 
                        gamma,training_policy,
                        constraint_library,
                        buffer,immovable_env,agent,net_immovable,
                        target_net_immovable,
                        loss_fct,
                        optimizer,
                        training_results,
                        MEAN_REWARD_BOUND,
                        device,max_iterations):

  """

  :param batch_size: the size of a batch of experiences for training
  :param learning_rate: the
  :param sync_target_frames:
  :param replay_size:
  :param replay_start_size:
  :param eps_start:
  :param eps_decay:
  :param eps_min:
  :param gamma:
  :param training_policy:
  :param constraint_library:
  :param buffer:
  :param immovable_env:
  :param agent:
  :param net_immovable:
  :param target_net_immovable:
  :param loss_fct:
  :param optimizer:
  :param training_results:
  :param MEAN_REWARD_BOUND:
  :param device:
  :param max_iterations:
  :return:
  """
  torch.manual_seed(20)

  epsilon = eps_start
  frame_idx = 0
  best_mean_reward = None
  training_iteration = 1
  total_rewards = []

  # final training loss
  final_immovable_loss = 0

  immovable_loss_history = np.zeros(max_iterations)

  start_time_experience_gain = time.time()

  print_experience_replay = True
  # train for only max_iterations iterations
  while training_iteration <= max_iterations:
      # print('\n frame_idx is ',frame_idx)
      # print('training iteration is ',training_iteration)
      iteration_start_time = time.time()

      frame_idx += 1
      epsilon = max(epsilon * eps_decay,eps_min)

      if training_policy == "boltzmann":
          reward = agent.play_step_boltzmann(net_immovable,epsilon,device = device)
      elif training_policy == "epsilon-greedy":
          reward = agent.play_step(net_immovable, epsilon, device=device)
      else:
          reward = None

      if reward is not None:
        total_rewards.append(reward)
        mean_reward = np.mean(total_rewards[-100:])
        #print("%d: %d games, mean reward %.3f, (epsilon %.2f)" %
        #      (frame_idx,len(total_rewards),mean_reward,epsilon))

        best_mean_reward = mean_reward
        
        if best_mean_reward is None or best_mean_reward < mean_reward:
          ## replace TEST ENVIRONMENT with name for immovable and movable constraints
          #torch.save(net.state_dict(),"TEST ENVIRONMENT -best.dat")

          best_mean_reward = reward

        # if best_mean_reward is not None:
        #      print("Best mean reward updated is %.3f" % (best_mean_reward))

        ## Termination when the mean reward is above MEAN_REWARD_BOUND
        #if mean_reward > MEAN_REWARD_BOUND:
          #print("Solved in %d frames!" % (best_mean_reward))
      
      # print('number of experience is ',len(buffer))
      if len(buffer) < replay_start_size:
        num_experiences = len(buffer)
        #print(f'Number of experiences is {num_experiences}')
        continue

      # print(f'Training Iteration {training_iteration} of RL_I agent')
      end_time_experience_replay = time.time()
      if print_experience_replay:
        print(f"Total time for experience replay is {end_time_experience_replay - start_time_experience_gain}")

      print_experience_replay = False

      batch = buffer.sample(batch_size)
      states,actions,rewards,dones,next_states = batch

      states_v = torch.Tensor(states).reshape(-1,1).to(device)
      next_states_v = torch.Tensor(next_states).reshape(-1,1).to(device)
      actions_v = torch.Tensor(actions).to(device)
      rewards_v = torch.Tensor(rewards).to(device)
      done_mask = torch.ByteTensor(dones).to(device)

      #print('states_v are',states_v)
      #print('next_states_v are ',next_states_v)

      net_states_v = net_immovable(states_v)

      state_action_values = torch.zeros(actions_v.shape)
      #print('state_action_values initially ',state_action_values)
      num_actions = actions_v.size(dim = 0)
      #print('number of actions are ',num_actions)
      for i in range(num_actions):
        action = int(actions_v[i])
        state_action_values[i] = net_states_v[i][action]

      next_state_values = target_net_immovable(next_states_v).max(1)[0]
      next_state_values[done_mask] = 0.0
      next_states_values = next_state_values.detach()

      expected_state_action_values = next_state_values*gamma + rewards_v

      # either the huber loss or the MSE loss
      if loss_fct == "mse":  # the mse loss
          loss_t_immovable = nn.MSELoss()(state_action_values, expected_state_action_values)

      if loss_fct == "huber":  # loss is huber
          loss_t_immovable = nn.HuberLoss()(state_action_values, expected_state_action_values)

      ## print out the training loss
      #print('Training loss is ',loss_t_immovable)
      #training_results.write(str(loss_t_immovable.item())+'\n')

      immovable_loss_history[training_iteration - 1] = loss_t_immovable
      final_immovable_loss = loss_t_immovable

      optimizer.zero_grad()
      loss_t_immovable.backward(retain_graph=False)
      optimizer.step()

      if frame_idx % sync_target_frames == 0:
        target_net_immovable.load_state_dict(net_immovable.state_dict())

      iteration_end_time = time.time()

      if mod(training_iteration, 10) == 0:
        print(f'Total time for Training Iteration {training_iteration} is {iteration_end_time - iteration_start_time}')
      training_iteration += 1

  #training_results.close()
  return immovable_loss_history, final_immovable_loss

def deployImmovableAgent(net_immovable, immovable_env ,max_iteration):
    #  This is for the immovable constraints RL agent deployment
    immovable_env.reset()

    torch.manual_seed(20)

    # print('target immovable CSP is ', immovable_env.target_immovable_csp)
    done = immovable_env.getCSP() >= immovable_env.target_immovable_csp

    cumulative_rewards = [0]
    iterations = [0]
    csp_values = [0]

    # random seed
    np.random.seed(10)

    curr_iteration = 0

    predictive_net_immovable = net_immovable

    while True:
        curr_state = immovable_env.curr_state
        action = torch.argmax(predictive_net_immovable(torch.Tensor([immovable_env.curr_state]))).item()
        # print(f'Action is {action}')
        immovable_env.step(action)
        cumulative_rewards.append(immovable_env.cumulative_reward)

        # get the intermediate immovable CSP value
        intermediate_csp = immovable_env.getCSP()
        csp_values.append(intermediate_csp)

        # produce schedule as long as possible until intermediate csp achieves 1
        if intermediate_csp >= 1:
            break

        curr_iteration += 1
        iterations.append(curr_iteration)
        # print(f'Current iteration is {curr_iteration}')
        # print(f'Intermediate CSP is {intermediate_csp}')

        if curr_iteration >= max_iteration:
            break

    immovable_constraints_satisfied = immovable_env.satisfied_constraints
    # print('immovable constraints satisfied are ', immovable_constraints_satisfied)
    immovable_csp_acheived = immovable_env.getCSP()
    # print(f'immovable_csp_achieved is {immovable_csp_acheived}')
    return immovable_csp_acheived, immovable_constraints_satisfied, immovable_env.cumulative_reward

def deployMovableAgent(net_movable, movable_env, max_iteration):
        torch.manual_seed(20)

        # load the trained weights that we saved for the immovable constraints predictive network
        predictive_net_movable = net_movable

        # This is for the immovable constraints RL agent deployment
        movable_env.reset()

        # print('target movable CSP is ', movable_env.target_movable_csp)
        done = movable_env.getCSP() >= movable_env.target_movable_csp

        cumulative_rewards = [0]
        iterations = [0]
        movable_csp_values = [0]

        # random seed
        np.random.seed(10)

        iteration = 0
        while True:
              #print('The immovable constraints satisfied are ', movable_env.immovable_constraints_satisfied)
              #print('iteration is ', iteration)
              curr_state = movable_env.curr_state
              action = torch.argmax(predictive_net_movable(torch.Tensor([movable_env.curr_state]))).item()
              #print('The action is', action)
              movable_env.step(action)

              intermediate_movable_csp = movable_env.getCSP()
              #print('The intermediate movable CSP is ', intermediate_movable_csp)

              # add in the intermediate movable CSP as well as the cumulative rewards received so far
              movable_csp_values.append(intermediate_movable_csp)
              cumulative_rewards.append(movable_env.cumulative_reward)

              #print('The number of movable constraints to satisfy is ', movable_env.num_movable_constraints)
              #print('The number of movable constraints satisfied is ', movable_env.num_movable_constraints_satisfied)
              if movable_env.getCSP() >= 1:
                  break

              iteration += 1
              iterations.append(iteration)

              # need to set maximum number of iterations during deployment to prevent infinite looping
              if iteration >= max_iteration:
                  break

        movable_constraints_satisfied = movable_env.satisfied_movable_constraints
        print('movable constraints satisfied are ', movable_constraints_satisfied)

        movable_csp_acheived = movable_env.getCSP()
        print(f'movable_csp_achieved is {movable_csp_acheived}')

        return movable_csp_acheived, movable_constraints_satisfied, movable_env.cumulative_reward

# trains the movable RL agent
def trainMovableAgent(batch_size,learning_rate,
                        sync_target_frames, replay_size,
                        replay_start_size,eps_start,
                        eps_decay, eps_min, 
                        gamma,training_policy,
                        constraint_library,
                        buffer,movable_env,agent,net_movable,
                        target_net_movable,
                        loss_fct,
                        optimizer,
                        training_results,
                        MEAN_REWARD_BOUND,
                        device, max_iteration):
  torch.manual_seed(20)
  epsilon = eps_start
  
  # keep track of where the training of the DQN for immovable RL agentstarted
  total_rewards = []
  frame_idx = 0
  best_mean_reward = None

  train_iteration = 1

  final_movable_loss = 0
  movable_loss_history = np.zeros(max_iteration)

  while train_iteration <= max_iteration:

    ## train for max_iteration iterations where each iteration is an update of the weights


    # print('\nframe index is ',frame_idx)
    iteration_start_time = time.time()

    frame_idx += 1
    epsilon = max(epsilon * eps_decay,eps_min)

    play_step_start_time = time.time()

    if training_policy == "boltzmann":
        reward = agent.play_step_boltzmann(net_movable,epsilon,device = device)
    elif training_policy == "epsilon-greedy":
        reward = agent.play_step(net_movable,epsilon,device=device)
    else:
        reward = None

    play_step_end_time = time.time()

    if mod(train_iteration, 10) == 0:
        print(f'Total time for the play step is {play_step_end_time - play_step_start_time}')

    if reward is not None:
      total_rewards.append(reward)
      mean_reward = np.mean(total_rewards[-100:])
      # print("%d: %d games, mean reward %.3f, (epsilon %.2f)" %
      #      (frame_idx,len(total_rewards),mean_reward,epsilon))
      
    

      best_mean_reward = mean_reward
      
      if best_mean_reward is None or best_mean_reward < mean_reward:
        # replace TEST ENVIRONMENT with name for immovable and movable constraints
        # torch.save(net_movable.state_dict(),"TEST ENVIRONMENT -best.dat")

        best_mean_reward = reward
        #if best_mean_reward is not None:
        #  print("Best mean reward updated is %.3f" % (best_mean_reward))
    
      ## Termination when the mean reward is above MEAN_REWARD_BOUND
      #if mean_reward > MEAN_REWARD_BOUND:
      #  print("Solved in %d frames!" % (best_mean_reward))
      #  break
    
    #print('Number of experience is ',len(buffer))
    if len(buffer) < replay_start_size:
        num_experiences = len(buffer)
        # print(f'Number of experiences for RL_M is {num_experiences}')
        continue

    #print(f'Training iteration {train_iteration} for RL_M')

    batch = buffer.sample(batch_size)
    states,actions,rewards,dones,next_states = batch

    states_v = torch.Tensor(states).reshape(-1,1).to(device)
    next_states_v = torch.Tensor(next_states).reshape(-1,1).to(device)
    actions_v = torch.Tensor(actions).to(device)
    rewards_v = torch.Tensor(rewards).to(device)
    done_mask = torch.ByteTensor(dones).to(device)

    net_states_v = net_movable(states_v)
    state_action_values = torch.zeros(actions_v.shape)
    #print('state_action_values initially ',state_action_values)
    num_actions = actions_v.size(dim = 0)
    #print('number of actions are ',num_actions)
    for i in range(num_actions):
      action = int(actions_v[i])
      state_action_values[i] = net_states_v[i][action]



    next_state_values = target_net_movable(next_states_v).max(1)[0]
    next_state_values[done_mask] = 0.0
    next_states_values = next_state_values.detach()

    expected_state_action_values = next_state_values*gamma + rewards_v

    if loss_fct == "mse":
        loss_t = nn.MSELoss()(state_action_values,expected_state_action_values)
    elif loss_fct == "huber":
        loss_t = nn.HuberLoss()(state_action_values, expected_state_action_values)
    else:
        loss_t = None

    movable_loss_history[train_iteration - 1] = loss_t
    final_movable_loss = loss_t


    #print('traning iteration is ',train_iteration)
    #print('loss is ',loss_t)
    #training_results.write(str(loss_t.item())+'\n')
    
    optimizer.zero_grad()
    loss_t.backward()
    optimizer.step()

    iteration_end_time = time.time()
    if mod(train_iteration, 10) == 0:
        print(f'Total time for Training Iteration {train_iteration} is {iteration_end_time - iteration_start_time}')
    # print(f'Total time for Iteration {train_iteration} is {iteration_end_time - iteration_start_time}')
    train_iteration += 1

    if frame_idx % sync_target_frames == 0:
      target_net_movable.load_state_dict(net_movable.state_dict())

  return movable_loss_history, final_movable_loss

# visualize the training loss specifically for the He initilization
def visualize_traing_loss_he_intialization(huber_loss_file, mse_loss_file, output_file):
    plt.figure()

    # read in the huber losses from input file
    huber_losses = pd.read_csv(huber_loss_file, names=['Training_Loss_Huber'])

    # read in the mse losses from the input file
    mse_losses = pd.read_csv(mse_loss_file, names=['Training_Loss_MSE'])

    huber_losses = huber_losses['Training_Loss_Huber'].values
    mse_losses = mse_losses['Training_Loss_MSE'].values

    plt.xlabel("Training Iteration")
    plt.ylabel('Average Training Loss')

    plt.plot(huber_losses, label = f"Huber Loss")
    plt.plot(mse_losses, label = f"MSE Loss")

    plt.legend()

    plt.savefig(output_file,bbox_inches="tight")

# writes training loss history (usually average for a scenario) to output file
def write_training_loss_history_to_output_file(average_loss_history, output_file):

    for loss in average_loss_history:
        output_file.write(f'{loss}\n')

    output_file.close()

# visualizes the training loss
import pandas as pd


def visualize_training_loss(input_file,output_file):

  plt.figure()

  # read in the losses from input file
  losses = pd.read_csv(input_file, names=['Training_Loss'])


  

  # the training loss looks pretty good for the basic framework
  # which suggests that if the AI gym environment is properly defined,
  # we should get pretty good results. We will use that approach toward
  # the Immovable constraints RL agent and the movable constraint RL agent
  # Since traning loss becomes very low after 200 epoches, it may or may not
  # be overfitting
  training_losses = losses['Training_Loss'].values
  plt.plot(training_losses)
  

  plt.xlabel('Training Iteration')
  plt.ylabel('Average Training Loss')

  # saving the figures for the training results
  plt.savefig(output_file, bbox_inches="tight")
