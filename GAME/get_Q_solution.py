import Moving_sofa_env
import Qlearning
from shapely.geometry import Point, Polygon
import random
import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt

np.random.seed(0)

def get_solution(N, env, Qlearner):
    
    state, info = env.reset()
    #print('state:' + str(state)) it starts at (h = 1, state = 0)

    actions_taken = []
    states_seen = []
    distances = [env.board.get_distance_value(env.shape)]
    total_reward = 0
    
    for i in range(N):
        action_index = Qlearner.get_action(state)
        action = env.action_space[action_index]

        next_state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

        actions_taken.append(action)
        states_seen.append(state)
        distances.append(env.board.get_distance_value(env.shape))

        if terminated or truncated:
            return actions_taken, 0, states_seen, distances, total_reward

        Qlearner.update_q_table(state, action_index, reward, next_state)

        state = next_state

        
    
    loss = env.board.get_distance_value(env.shape)
    return actions_taken, loss, states_seen, distances, total_reward


def main():
    #######parameters#######
    action_list = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90] #because of the weird grid no minusus. I guess just put minusus in the final paper. 
    N = 50 #number of Decision Epochs
    n_episodes = 100

    env = Moving_sofa_env.Moving_sofa_env()
    Qlearner = Qlearning.Qlearning(n_states= len(env.state_space), n_actions=len(env.action_space))

    actions_all_episodes = []
    states_all_episodes = []
    Q_table_per_episode = []
    distances_per_episode = []
    total_reward_per_episode = []
    loss_per_episode = []

    for i in range(n_episodes):
        actions_taken, loss, states_seen, distances, total_reward = get_solution(N, env, Qlearner)
        actions_all_episodes.append(actions_taken)
        states_all_episodes.append(states_seen)
        distances_per_episode.append(distances)
        total_reward_per_episode.append(total_reward)
        loss_per_episode.append(loss)
        Q_table_per_episode.append(copy.deepcopy(Qlearner.q_table))
        Qlearner.update_epsilon()

    #print(Q_table_per_episode)

    Q_table_to_csv(Q_table_per_episode, N)
    
    #export such that I can read It and check correctness
    pd.DataFrame(Q_table_per_episode[9]).to_csv("10thQtable.csv")


    
    # create a dictionary where the keys are the column names and the values are the inner lists
    data_dict = {f"actions_taken{i+1}": inner_list for i, inner_list in enumerate(actions_all_episodes)}

    # create a dataframe from the dictionary
    df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()

    df.to_csv('actions.csv', index=False)

     # create a dictionary where the keys are the column names and the values are the inner lists
    data_dict2 = {f"actions_taken{i+1}": inner_list for i, inner_list in enumerate(states_all_episodes)}

    # create a dataframe from the dictionary
    df2 = pd.DataFrame.from_dict(data_dict2, orient='index').transpose()

    df2.to_csv('states_seen.csv', index=False)


    make_figures(n_episodes, distances_per_episode, loss_per_episode, total_reward_per_episode)


def make_figures(n_episodes, distances_per_episode, loss_per_episode, total_reward_per_episode):
    plt.plot(range(n_episodes), total_reward_per_episode)
    plt.show()
    plt.plot(range(n_episodes), loss_per_episode)
    plt.show()



def  Q_table_to_csv(Q_table_per_episode, N):
    env = Moving_sofa_env.Moving_sofa_env()

    episodes_state_list = []

    for Q_table in Q_table_per_episode:
        state, info = env.reset()
        action_list = []
        for i in range(N):
            #print(Q_table[state])
            index = np.argmax(Q_table[state])
            action = env.action_space[index]

            next_state, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                continue
            action_list.append(action)
            
            state = next_state
        
        episodes_state_list.append(action_list)
    
    print(episodes_state_list)
    # create a dictionary where the keys are the column names and the values are the inner lists
    data_dict = {f"Q_actions{i+1}": inner_list for i, inner_list in enumerate(episodes_state_list)}

    # create a dataframe from the dictionary
    df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()

    df.to_csv('Q_actions.csv', index=False)

main()