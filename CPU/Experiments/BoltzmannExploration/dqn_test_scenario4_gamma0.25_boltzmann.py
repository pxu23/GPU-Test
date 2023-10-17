# Press the green button in the gutter to run the script.
import numpy as np

from High_A_Central_Constraints.constraint_library_gurobi import BaseballSchedulingConstraintLibraryGurobi
from Experiments.simulation import performSimulation
import time

from RL_Framework.rl_boss_agent import RLAgentBoss

if __name__ == '__main__':

     MEAN_REWARD_BOUND = 200.0

     # set a random seed to ensure reproducibility
     np.random.seed(10)

     # initially set target immovable CSP to 0.5
     target_immovable_csp = 0.7

     # initially set target movable CSP to 0.5
     target_movable_csp = 0.8

     # initially set weight_immovable_csp
     weight_immovable_csp = 0.7

     # initially set weight_movable_csp
     weight_movable_csp = 1 - weight_immovable_csp

     # for our testing, we set the target satisfaction threshold to 0.8
     target_satisfaction_threshold = 0.8




     # list of key immovable constraints of the High A Central (only a subset of the constraints) to test
     immovable_constraint_list = ['SouthBendRequiredToPlayAllEasternClubsOnce',
                                  'CertainMatchupTwoToTwo',
                                  'EachClub132Games',
                                  'AllSeriesSixGamesWithTwoThreeGame',
                                  'ClubCannotHostMoreThanOnceInFourWeekPeriod',
                                  'certainMatchupGuaranteedThreeSeries',
                                  'WestTeamsHomeRoadMatchupInDivision']


     num_immovable_constraints = 5


     # list of key movable constraints of the High A Central (only a subset of all the constraints) to test
     movable_constraint_list = ['homeOnOneSideOfASG',
                                'NonDivisionalOpponent',
                                'EastToWestMaxTwoTravel',
                                'WestToEastMaxTwoTravel',
                                'PlayNoMoreThanOnceThreeWeeks',
                                'EastTeamsHomeRoadMatchupInDivision',
                                'spacingOppRegionTrips']

     num_movable_constraints = 3

     rl_agent_boss = RLAgentBoss(target_immovable_csp, target_movable_csp, weight_immovable_csp,
                                 weight_movable_csp, immovable_constraint_list,
                                 movable_constraint_list, num_immovable_constraints, num_movable_constraints)

     library = BaseballSchedulingConstraintLibraryGurobi()


     start_time = time.time()

     testing_output = ('outputs_testDQN_Boltzmann/scenario4/testing_output_dqn_scenario4_gamma0.25.txt')
     output_statistics_file = ('outputs_testDQN_Boltzmann/scenario4/output_statistics_dqn_scenario4_gamma0.25.txt')

     csp_i_scenario4_output_file = ('outputs_testDQN_Boltzmann/scenario4/csp_i_dqn_scenario4_gamma0.25.txt')
     csp_m_scenario4_output_file = ('outputs_testDQN_Boltzmann/scenario4/csp_m_dqn_scenario4_gamma0.25.txt')
     movable_rewards_scenario4_output_file = ('outputs_testDQN_Boltzmann/scenario4/cumrewards_movable_scenario4_gamma0.25.txt')
     immovable_rewards_scenario4_output_file = ('outputs_testDQN_Boltzmann/scenario4/cumrewards_immovable_scenario4_gamma0.25.txt')
     schedule_score_scenario4_output_file = ('outputs_testDQN_Boltzmann/scenario4/schedule_score_scenario4_gamma0.25.txt')

     average_immovable_loss_history_scenario4_output_file = (
         'outputs_testDQN_Boltzmann/scenario4/average_immovable_loss_history_scenario4_gamma0.25.txt')
     average_movable_loss_history_scenario4_output_file = (
         'outputs_testDQN_Boltzmann/scenario4/average_movable_loss_history_scenario4_gamma0.25.txt')

     performSimulation(immovable_constraint_list, movable_constraint_list, 5,
                       3, target_immovable_csp,
                       target_movable_csp, target_satisfaction_threshold, MEAN_REWARD_BOUND,gamma=0.25,
                       training_policy="boltzmann",
                       loss_fct="mse",
                       he_initialization=False,
                       log_intermediate_output=False,
                       log_statistics=True,
                       log_csp_I=True, log_csp_M=True, log_schedule_score=True, log_immovable_rewards=True,
                       log_movable_rewards=True, log_immovable_average_loss_history=True, log_movable_average_loss_history=True,
                       rl_agent_boss=rl_agent_boss, output_file=testing_output,output_statistics_file=output_statistics_file,
                       output_file_rewards_immovable=immovable_rewards_scenario4_output_file,
                       output_file_rewards_movable=movable_rewards_scenario4_output_file,
                       output_file_csp_i=csp_i_scenario4_output_file,
                       output_file_csp_m=csp_m_scenario4_output_file,
                       output_file_schedule_score=schedule_score_scenario4_output_file,
                       output_file_average_immovable_loss_history=average_immovable_loss_history_scenario4_output_file,
                       output_file_average_movable_loss_history=average_movable_loss_history_scenario4_output_file)

     end_time = time.time()

     print(f'Total time is {end_time-start_time}')