import Moving_sofa_env
import Qlearning
from shapely.geometry import Point, Polygon
import random
import pandas as pd
import numpy as np


def get_solution(N, env, Qlearner):
    
    state, info = env.reset()

    actions_taken = []
    
    for i in range(N):
        action_index = Qlearner.get_action(state)
        action = env.action_space[action_index]

        next_state, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            return actions_taken, 0

        Qlearner.update_q_table(state, action_index, reward, next_state)

        actions_taken.append(action)

        state = next_state

        
    
    loss = 0
    return actions_taken, loss


def main():
    #######parameters#######
    action_list = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90] #because of the weird grid no minusus. I guess just put minusus in the final paper. 
    N = 200 #number of Decision Epochs
    n_episodes = 10

    env = Moving_sofa_env.Moving_sofa_env()
    Qlearner = Qlearning.Qlearning(n_states= len(env.state_space), n_actions=len(env.action_space))

    actions_all_episodes = []
    Q_table_per_episode = []

    for i in range(n_episodes):
        actions_taken, loss, = get_solution(N, env, Qlearner)
        actions_all_episodes.append(actions_taken)
        Q_table_per_episode.append(Qlearner.q_table)
        Qlearner.update_epsilon()

    print(Q_table_per_episode)

    Q_table_to_csv(Q_table_per_episode, N)
    
    # create a dictionary where the keys are the column names and the values are the inner lists
    data_dict = {f"actions_taken{i+1}": inner_list for i, inner_list in enumerate(actions_all_episodes)}

    # create a dataframe from the dictionary
    df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()

    df.to_csv('actions.csv', index=False)

def  Q_table_to_csv(Q_table_per_episode, N):
    env = Moving_sofa_env.Moving_sofa_env()

    episodes_state_list = []

    for Q_table in Q_table_per_episode:
        state, info = env.reset()
        action_list = []
        for i in range(N):
            index = np.argmax(Q_table[state])
            action = env.action_space[index]

            next_state, reward, terminated, truncated, info = env.step(action)
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