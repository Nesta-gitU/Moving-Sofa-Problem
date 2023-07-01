import Savings_problem_env
import Qlearning
import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt

#np.random.seed(1)
#45np.random.seed(0)
def get_solution(N, env, Qlearner):
     
    state, info = env.reset()
    #print('state:' + str(state)) it starts at (h = 1, state = 0)

    actions_taken = []
    amounts_consumed = []
    assets_per_action = []

    total_reward = 0
    
    for i in range(N):
        
        action_index = Qlearner.get_action(state)
        action = env.action_space[action_index]
        #print(action)

        if i == N-1:
            #print(i)
            #print(state)
            #print('epoch', env.current_epoch)
            action_index = len(env.action_space) - 1
            #print(action_index)
            action = env.action_space[action_index]
            #print(action)

        next_state, reward, terminated, truncated, info = env.step(action, epoch = i + 1)

        total_reward += reward

        actions_taken.append(action)
        amounts_consumed.append(info['amount consumed'])
        assets_per_action.append(env.current_assets)
        
        #print('i =', i)
        Qlearner.update_q_table(state, action_index, reward, next_state)

        if terminated or truncated:
            return actions_taken, amounts_consumed, assets_per_action, total_reward
        
        state = next_state


    return actions_taken, sum(amounts_consumed), sum(assets_per_action), total_reward

def main():
    #######parameters#######
    N = 6 #
    D = 6 #
    n_episodes = 20000 

    env = Savings_problem_env.Savings_problem_env(number_of_epochs= N)
    Qlearner = Qlearning.Qlearning(n_states= env.state_space[-1,-1] + 1 , n_actions=len(env.action_space))
    print(env.state_space[-1,-1] + 1)

    actions_all_episodes = []
    Q_table_per_episode = []

    total_reward_per_episode = []
    amounts_consumed_per_episode = []
    assets_per_action_per_episode = []
    epsilon_per_episode = []


    for i in range(n_episodes):
        actions_taken, amounts_consumed, assets_per_action, total_reward = get_solution(N, env, Qlearner)

        actions_all_episodes.append(actions_taken)
        amounts_consumed_per_episode.append(amounts_consumed)
        assets_per_action_per_episode.append(assets_per_action)
        total_reward_per_episode.append(total_reward)

        Q_table_per_episode.append(copy.deepcopy(Qlearner.q_table))

        epsilon_per_episode.append(Qlearner.epsilon)
        #updates that should happen after each episode
        Qlearner.update_epsilon()

    #print(Q_table_per_episode)

    Q_table_to_csv(Q_table_per_episode, N)
    
    #export such that I can read It and check correctness
    pd.DataFrame(Q_table_per_episode[-1]).to_csv("lastQtable-savings.csv")
    
    # create a dictionary where the keys are the column names and the values are the inner lists
    data_dict = {f"actions_taken{i+1}": inner_list for i, inner_list in enumerate(actions_all_episodes)}

    # create a dataframe from the dictionary
    df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()

    df.to_csv('actions-savings.csv', index=False)

    makeplots(n_episodes, total_reward_per_episode,  epsilon_per_episode, assets_per_action_per_episode)


def makeplots(n_episodes, rewards,  epsilon_per_episode, assets_per_action_per_episode):
    plt.plot(range(n_episodes), rewards)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid()
    plt.show()

    plt.plot(range(n_episodes), epsilon_per_episode)
    plt.xlabel('Episode')
    plt.ylabel('Epsilon')
    plt.grid()
    plt.show()

def  Q_table_to_csv(Q_table_per_episode, N):
    print('---------------------------------------------------\n--------------------------------------------------\n------------------------------------------\n-------------------------------')
    env = Savings_problem_env.Savings_problem_env(number_of_epochs=N)

    episodes_state_list = []
    episode_amounts_consumed = []
    episode_assets_per_action = []
    episode_rewards = []
    episode_rewards_summed = []

    for Q_table in Q_table_per_episode:
        state, info = env.reset()
        action_list = []
        amounts_consumed = []
        assets_per_action = []
        rewards = []

        for i in range(N):
            #print(Q_table[state])
            index = np.argmax(Q_table[state])
            action = env.action_space[index]

            next_state, reward, terminated, truncated, info = env.step(action, epoch = i + 1)

            rewards.append(reward)
            action_list.append(action)
            amounts_consumed.append(info['amount consumed'])
            assets_per_action.append(env.current_assets)
            
            if terminated or truncated:
                break
            
            state = next_state
            
        
        episodes_state_list.append(action_list)
        episode_amounts_consumed.append(amounts_consumed)
        episode_assets_per_action.append(assets_per_action)
        episode_rewards_summed.append(sum(rewards))
        episode_rewards.append(rewards)
    
    print('amount consumed:', episode_amounts_consumed[19990:20000])
    print('assets:', episode_assets_per_action[19990:20000])
    print('actions:', episodes_state_list[19990:20000])
    print('rewards:', episode_rewards[19990:20000])

    makeplots(len(Q_table_per_episode), episode_rewards_summed, episode_amounts_consumed, episode_assets_per_action)

    # create a dictionary where the keys are the column names and the values are the inner lists
    data_dict = {f"Q_actions{i+1}": inner_list for i, inner_list in enumerate(episodes_state_list)}

    # create a dataframe from the dictionary
    df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()

    df.to_csv('Q_actions_savings.csv', index=False)

main()