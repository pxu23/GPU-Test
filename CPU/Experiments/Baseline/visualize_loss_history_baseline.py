from DeepQNetwork.dqn_utils import visualize_training_loss

if __name__=="__main__":
    # for the RL_I agent
    # input_files = ['./outputs_testDQN/scenario1/average_immovable_loss_history_scenario1.txt',
    #                './outputs_testDQN/scenario2/average_immovable_loss_history_scenario2.txt',
    #                './outputs_testDQN/scenario3/average_immovable_loss_history_scenario3.txt',
    #                './outputs_testDQN/scenario4/average_immovable_loss_history_scenario4.txt',
    #                './outputs_testDQN/scenario5/average_immovable_loss_history_scenario5.txt',
    #                './outputs_testDQN/scenario6/average_immovable_loss_history_scenario6.txt',
    #                './outputs_testDQN/scenario7/average_immovable_loss_history_scenario7.txt']
    #
    # title = "Average Loss History for the RL_I agent"
    # ylabel = "Average Training Loss"
    # output_file = "./loss_history/immovable_agent_training_loss.png"
    # visualize_training_loss_multiple_files(input_files,title,ylabel,output_file)
    #
    # # for the RL_M agent
    # input_files = ['./outputs_testDQN/scenario1/average_movable_loss_history_scenario1.txt',
    #                './outputs_testDQN/scenario2/average_movable_loss_history_scenario2.txt',
    #                './outputs_testDQN/scenario3/average_movable_loss_history_scenario3.txt',
    #                './outputs_testDQN/scenario4/average_movable_loss_history_scenario4.txt',
    #                './outputs_testDQN/scenario5/average_movable_loss_history_scenario5.txt',
    #                './outputs_testDQN/scenario6/average_movable_loss_history_scenario6.txt',
    #                './outputs_testDQN/scenario7/average_movable_loss_history_scenario7.txt']
    #
    # title = "Average Loss History for the RL_M agent"
    # ylabel = "Average Training Loss"
    # output_file = "./loss_history/movable_agent_training_loss.png"
    # visualize_training_loss_multiple_files(input_files, title, ylabel, output_file)

    # Scenario 1
    visualize_training_loss(input_file='./outputs_testDQN/scenario1/average_immovable_loss_history_scenario1_gamma0.25.txt',
                            output_file='./loss_history/immovable_agent_training_loss_scenario1_gamma0.25.png')
    visualize_training_loss(input_file='./outputs_testDQN/scenario1/average_movable_loss_history_scenario1_gamma0.25.txt',
                            output_file='./loss_history/movable_agent_training_loss_scenario1_gamma0.25.png')

    # Scenario 2
    visualize_training_loss(input_file='./outputs_testDQN/scenario2/average_immovable_loss_history_scenario2_gamma0.25.txt',
                            output_file='./loss_history/immovable_agent_training_loss_scenario2_gamma0.25.png')
    visualize_training_loss(input_file='./outputs_testDQN/scenario2/average_movable_loss_history_scenario2_gamma0.25.txt',
                            output_file='./loss_history/movable_agent_training_loss_scenario2_gamma0.25.png')

    # Scenario 3
    visualize_training_loss(input_file='./outputs_testDQN/scenario3/average_immovable_loss_history_scenario3_gamma0.25.txt',
                            output_file='./loss_history/immovable_agent_training_loss_scenario3_gamma0.25.png')
    visualize_training_loss(input_file='./outputs_testDQN/scenario3/average_movable_loss_history_scenario3_gamma0.25.txt',
                            output_file='./loss_history/movable_agent_training_loss_scenario3_gamma0.25.png')

    # Scenario 4
    visualize_training_loss(input_file='./outputs_testDQN/scenario4/average_immovable_loss_history_scenario4_gamma0.25.txt',
                            output_file='./loss_history/immovable_agent_training_loss_scenario4_gamma0.25.png')
    visualize_training_loss(input_file='./outputs_testDQN/scenario4/average_movable_loss_history_scenario4_gamma0.25.txt',
                            output_file='./loss_history/movable_agent_training_loss_scenario4_gamma0.25.png')

    # Scenario 5
    visualize_training_loss(input_file='./outputs_testDQN/scenario5/average_immovable_loss_history_scenario5_gamma0.25.txt',
                            output_file='./loss_history/immovable_agent_training_loss_scenario5_gamma0.25.png')
    visualize_training_loss(input_file='./outputs_testDQN/scenario5/average_movable_loss_history_scenario5_gamma0.25.txt',
                            output_file='./loss_history/movable_agent_training_loss_scenario5_gamma0.25.png')

    # Scenario 6
    visualize_training_loss(input_file='./outputs_testDQN/scenario6/average_immovable_loss_history_scenario6_gamma0.25.txt',
                            output_file='./loss_history/immovable_agent_training_loss_scenario6_gamma0.25.png')
    visualize_training_loss(input_file='./outputs_testDQN/scenario6/average_movable_loss_history_scenario6_gamma0.25.txt',
                            output_file='./loss_history/movable_agent_training_loss_scenario6_gamma0.25.png')

    # Scenario 7
    visualize_training_loss(input_file='./outputs_testDQN/scenario7/average_immovable_loss_history_scenario7_gamma0.25.txt',
                            output_file='./loss_history/immovable_agent_training_loss_scenario7_gamma0.25.png')
    visualize_training_loss(input_file='./outputs_testDQN/scenario7/average_movable_loss_history_scenario7_gamma0.25.txt',
                            output_file='./loss_history/movable_agent_training_loss_scenario7_gamma0.25.png')

    # Scenario 8
    visualize_training_loss(input_file='./outputs_testDQN/scenario8/average_immovable_loss_history_scenario8_gamma0.25.txt',
                            output_file='./loss_history/immovable_agent_training_loss_scenario8_gamma0.25.png')
    visualize_training_loss(input_file='./outputs_testDQN/scenario8/average_movable_loss_history_scenario8_gamma0.25.txt',
                            output_file='./loss_history/movable_agent_training_loss_scenario8_gamma0.25.png')