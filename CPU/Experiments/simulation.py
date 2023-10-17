# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import itertools
import time

import numpy as np
# from AIGym import BaseballSchedulingEnv
import torch
import torch.optim as optim

from DeepQNetwork.dqn import DQN
from RL_Framework.MovableRLAgent import MovableRLAgentDQN
from High_A_Central_Constraints.constraint_library_gurobi import BaseballSchedulingConstraintLibraryGurobi
from DeepQNetwork.dqn_utils import trainImmovableAgent, trainMovableAgent, deployImmovableAgent, deployMovableAgent,\
    write_training_loss_history_to_output_file
from DeepQNetwork.experience import ExperienceReplay
from AI_Gym_Environments.immovable_AI_gym import ImmovableRLEnv
from RL_Framework.immovable_RL_agent import ImmovableRLAgentDQN
from AI_Gym_Environments.movable_AI_gym import MovableRLEnv


def performSimulation(immovable_constraint_list, movable_constraint_list, num_immovable_constraints,
                      num_movable_constraints, target_immovable_csp,
                      target_movable_csp, target_satisfaction_threshold, MEAN_REWARD_BOUND, gamma,
                      training_policy, loss_fct, he_initialization,
                      log_intermediate_output, log_statistics,
                      log_csp_I, log_csp_M, log_schedule_score, log_immovable_rewards, log_movable_rewards,
                      log_immovable_average_loss_history, log_movable_average_loss_history, rl_agent_boss,
                      output_file, output_statistics_file,
                      output_file_rewards_immovable, output_file_rewards_movable, output_file_csp_i,
                      output_file_csp_m, output_file_schedule_score,
                      output_file_average_immovable_loss_history, output_file_average_movable_loss_history):

    # hoping the training results with be reproducible
    torch.manual_seed(20)

    if log_statistics:
        output_statistics_file = open(output_statistics_file, "w")
        print('NumImmovableConstraints', 'NumMovableConstraints', 'AverageImmovableTrainingLoss',
              'AverageMovableTrainingLoss', 'AverageImmovableCSPAchieved', 'AverageMovableCSPAchieved',
              'AverageCumulativeRewardImmovable', 'AverageCumulativeRewardMovable',
              'AverageScore', 'ProportionSatisfyingThreshold', 'MinSatisfactionThreshold\n',
              sep='\t', file=output_statistics_file)

    if log_intermediate_output:
        output_file = open(output_file, "w")

    if log_csp_I:
        output_file_csp_i = open(output_file_csp_i, "w")

    if log_csp_M:
        output_file_csp_m = open(output_file_csp_m, "w")

    if log_schedule_score:
        output_file_schedule_score = open(output_file_schedule_score, "w")

    if log_immovable_rewards:
        output_file_rewards_immovable = open(output_file_rewards_immovable, "w")

    if log_movable_rewards:
        output_file_rewards_movable = open(output_file_rewards_movable, "w")

    if log_immovable_average_loss_history:
        output_file_average_immovable_loss_history = open(output_file_average_immovable_loss_history, "w")

    if log_movable_average_loss_history:
        output_file_average_movable_loss_history = open(output_file_average_movable_loss_history, "w")

    print(f'\nScenario of {num_immovable_constraints} immovable constraints and {num_movable_constraints} movable constraints')

    # used to get the average loss history across all trials (i.e. combinations) of a scenario
    aggregate_loss_history_immovable = np.zeros(200)
    aggregate_loss_history_movable = np.zeros(200)

    # total training loss (immovable and movable) and thus the average training loss
    sum_movable_training_loss = 0
    sum_immovable_training_loss = 0

    sum_movable_csp_achieved = 0
    sum_immovable_csp_achieved = 0

    sum_movable_cumulative_reward = 0
    sum_immovable_cumulative_reward = 0

    sum_schedule_score = 0

    num_times_meet_threshold = 0

    immovable_combinations = list(itertools.combinations(immovable_constraint_list, num_immovable_constraints))
    movable_combinations = list(itertools.combinations(movable_constraint_list, num_movable_constraints))

    combinations = list(itertools.product(immovable_combinations, movable_combinations))
    num_combinations = len(combinations)

    combo_index = 1
    for combination in combinations:
        if log_intermediate_output:
            print(f'Combination is {combo_index}', file=output_file)
        print(f'Combination is {combo_index}')

        immovable_constraints_to_satisfy = combination[0]
        movable_constraints_to_satisfy = combination[1]

        if log_intermediate_output:
            print(f'Immovable constraints to satisfy is {immovable_constraints_to_satisfy}', file = output_file)
            print(f'Movable constraints to satisfy is {movable_constraints_to_satisfy}', file = output_file)

        print(f'Immovable constraints to satisfy is {immovable_constraints_to_satisfy}')
        print(f'Movable constraints to satisfy is {movable_constraints_to_satisfy}')

        start_time = time.time()
        #  Here we will set the training hyper-parameters
        #  Note: We will explore the effects of changing different hyperparameters
        batch_size = 32  # sample a batch size of 32 from experience replay for the target network
        learning_rate = 1e-4
        sync_target_frames = 1000
        replay_size = 500
        replay_start_size = 500

        eps_start = 1.0
        eps_decay = 0.05
        eps_min = 0.02

        # gamma = 0.25  # try discount of 0.8,0.5,and 0.25

        # sets up the constraint library for use
        constraint_library = BaseballSchedulingConstraintLibraryGurobi()

        # sets up the ExperienceReplay to store past experiences to help training
        buffer = ExperienceReplay(replay_size)

        # relates the immovable RL agent's environment
        immovable_env = ImmovableRLEnv(num_immovable_constraints, immovable_constraints_to_satisfy,
                                         target_immovable_csp, constraint_library, gamma)

        # training for the immovable RL agent
        agent = ImmovableRLAgentDQN(immovable_env, buffer)
        #

        if he_initialization:
            net_immovable = DQN((1, 1), 3, he_initialization=True)  # set up the predictive network
            target_net_immovable = DQN((1, 1), 3, he_initialization=True)  # set up the target network
        else:
            net_immovable = DQN((1,1),3, he_initialization=False)
            target_net_immovable = DQN((1,1), 3, he_initialization=False)

        # We will use the Adam optimizer for our problem
        optimizer = optim.Adam(net_immovable.parameters(), lr=learning_rate)

        # random seed for training
        np.random.seed(10)

        start = time.time()
        loss_history_immovable_combination, final_immovable_loss_combination = trainImmovableAgent(batch_size, learning_rate,
                              sync_target_frames, replay_size,
                              replay_start_size, eps_start,
                              eps_decay, eps_min,
                              gamma, training_policy,
                              constraint_library,
                              buffer, immovable_env, agent, net_immovable,
                              target_net_immovable,
                              loss_fct,
                              optimizer,
                              None,
                              MEAN_REWARD_BOUND,
                              device=torch.device('cpu'),max_iterations=200)
        end = time.time()
        print(f'Time to train the immovable RL agent with Gurobi is {end - start} seconds\n')

        start = time.time()
        aggregate_loss_history_immovable = (aggregate_loss_history_immovable + loss_history_immovable_combination)
        sum_immovable_training_loss += final_immovable_loss_combination
        end = time.time()
        print(f"Time to aggregate the immovable loss is {end - start} seconds")

        start = time.time()
        immovable_csp_achieved, immovable_constraints_satisfied, immovable_cumulative_reward = deployImmovableAgent(net_immovable,immovable_env, max_iteration = 10)
        end = time.time()
        print(f"Time to deploy the immovable agent is {end - start} seconds")

        if log_csp_I:
            output_file_csp_i.write(f'{immovable_csp_achieved}\n')

        if log_immovable_rewards:
            output_file_rewards_immovable.write(f'{immovable_cumulative_reward}\n')

        sum_immovable_csp_achieved += immovable_csp_achieved

        sum_immovable_cumulative_reward += immovable_cumulative_reward

        # gamma = 0.25  # try discount of 0.99,0.7,and 0.25

        batch_size = 32  ## sample a batch size of 32 from experience replay for the target network
        learning_rate = 1e-4
        sync_target_frames = 1000
        replay_size = 500
        replay_start_size = 500

        eps_start = 1.0
        eps_decay = 0.05
        eps_min = 0.02

        num_movable_constraints_to_satisfy = len(movable_constraints_to_satisfy)


        # calls the custom AI gym environment for the movable constraints (will be modified once
        # new constraints are introduced)
        movable_env = MovableRLEnv(num_movable_constraints_to_satisfy, movable_constraints_to_satisfy,
                                 target_movable_csp, constraint_library, gamma, immovable_constraints_satisfied)

        # sets up the ExperienceReplay to store past experiences to help training
        buffer = ExperienceReplay(replay_size)

        # training for the movable RL agent
        agent = MovableRLAgentDQN(movable_env, buffer)

        if he_initialization:
            net_movable = DQN((1, 1), 5, he_initialization=True).to(
                device=torch.device('cpu'))  # set up the predictive network
            target_net_movable = DQN((1, 1), 5, he_initialization=True).to(
                device=torch.device('cpu'))  # set up the target network
        else:
            net_movable = DQN((1, 1), 5, he_initialization=False).to(
                device=torch.device('cpu'))  # set up the predictive network
            target_net_movable = DQN((1, 1), 5, he_initialization=False).to(
                device=torch.device('cpu'))  # set up the target network

        epsilon = eps_start

        # We will use the Adam optimizer for our problem
        optimizer = optim.Adam(net_movable.parameters(), lr=learning_rate)

        # random seed for training
        np.random.seed(10)

        start = time.time()

        print(f"Training of movable agents begin")



        loss_history_movable_combination, final_movable_loss_combination = trainMovableAgent(batch_size, learning_rate,
                           sync_target_frames, replay_size,
                           replay_start_size, eps_start,
                           eps_decay, eps_min,
                           gamma, training_policy,
                           constraint_library,
                           buffer, movable_env, agent, net_movable,
                           target_net_movable,
                            loss_fct, optimizer,
                           None,
                            MEAN_REWARD_BOUND,
                            device=torch.device('cpu'),max_iteration=200)
        end = time.time()
        print(f'Time to train the movable RL agent with Gurobi is {end - start} seconds\n')

        start = time.time()
        aggregate_loss_history_movable = (aggregate_loss_history_movable + loss_history_movable_combination)
        sum_movable_training_loss += final_movable_loss_combination
        end = time.time()
        print(f"Time to train aggregate the movable loss is {end - start} seconds")

        movable_csp_achieved, movable_constraint_satisfied, movable_cumulative_reward = deployMovableAgent(net_movable,movable_env,max_iteration = 10)

        if log_csp_M:
            output_file_csp_m.write(f'{movable_csp_achieved}\n')

        if log_movable_rewards:
            output_file_rewards_movable.write(f'{movable_cumulative_reward}\n')

        sum_movable_csp_achieved += movable_csp_achieved

        sum_movable_cumulative_reward += movable_cumulative_reward

        score = rl_agent_boss.calculateScheduleScore(immovable_csp_achieved, movable_csp_achieved)

        if log_intermediate_output:
            print(f'The final score achieved is {score}', file=output_file)

        print(f'The final score achieved is {score}')

        if log_schedule_score:
            output_file_schedule_score.write(f'{score}\n')

        sum_schedule_score += score

        # checks if the score is above or equal to a particular threshold
        if score >= target_satisfaction_threshold:
            if log_intermediate_output:
                print(f'Threshold of {target_satisfaction_threshold} acheived with score {score}.'
                  f' Next is to finalize the schedule',
                  file = output_file)
            print(
                f'Threshold of {target_satisfaction_threshold} acheived with score {score}.'
                f' Next is to finalize the schedule')
            num_times_meet_threshold += 1
        else:
            print(f'Score of {score} did not achieve threshold of {target_satisfaction_threshold}')

        combo_index += 1

    average_immovable_csp_achieved = sum_immovable_csp_achieved / num_combinations
    average_loss_history_immovable = aggregate_loss_history_immovable / num_combinations
    average_cumulative_reward_immovable = sum_immovable_cumulative_reward / num_combinations

    if log_immovable_average_loss_history:
        write_training_loss_history_to_output_file(average_loss_history_immovable,
                                                   output_file_average_immovable_loss_history)

    average_movable_csp_achieved = sum_movable_csp_achieved / num_combinations
    average_loss_history_movable = aggregate_loss_history_movable / num_combinations
    average_cumulative_reward_movable = sum_movable_cumulative_reward / num_combinations

    if log_immovable_average_loss_history:
        write_training_loss_history_to_output_file(average_loss_history_movable,
                                                   output_file_average_movable_loss_history)

    average_score = sum_schedule_score / num_combinations
    proportion_meeting_threshold = num_times_meet_threshold / num_combinations

    average_final_training_loss_immovable = sum_immovable_training_loss / num_combinations
    average_final_training_loss_movable = sum_movable_training_loss / num_combinations

    if log_statistics:
        print(num_immovable_constraints, num_movable_constraints, average_final_training_loss_immovable,
              average_final_training_loss_movable, average_immovable_csp_achieved, average_movable_csp_achieved,
           average_cumulative_reward_immovable, average_cumulative_reward_movable,
          average_score, proportion_meeting_threshold, target_satisfaction_threshold, sep='\t', file=output_statistics_file)

    if log_intermediate_output:
        output_file.close()

    if log_schedule_score:
        output_file_schedule_score.close()

    if log_csp_I:
        output_file_csp_i.close()

    if log_csp_M:
        output_file_csp_m.close()

    if log_immovable_rewards:
        output_file_rewards_immovable.close()

    if log_movable_rewards:
        output_file_rewards_movable.close()

    if log_immovable_average_loss_history:
        output_file_average_immovable_loss_history.close()

    if log_movable_average_loss_history:
        output_file_average_movable_loss_history.close()

    return (average_loss_history_immovable, average_loss_history_movable, average_final_training_loss_immovable, \
        average_final_training_loss_movable, average_immovable_csp_achieved, average_movable_csp_achieved,
        average_cumulative_reward_immovable,  \
        average_cumulative_reward_movable, average_score, proportion_meeting_threshold)
