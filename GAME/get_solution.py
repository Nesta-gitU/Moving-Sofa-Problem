import Moving_sofa_env
from shapely.geometry import Point, Polygon
import random
import pandas as pd


def get_solution(action_list, N):
    
    env = Moving_sofa_env.Moving_sofa_env()

    actions_taken = []
    
    for i in range(N):
        action = random.sample(action_list, 1)[0]

        observation, reward, terminated, truncated, info = env.step(action)

        actions_taken.append(action)

        if terminated or truncated:
            return actions_taken, 0
    
    loss = 0
    return actions_taken, loss


def main():
    #######parameters#######
    action_list = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90] #because of the weird grid no minusus. I guess just put minusus in the final paper. 
    N = 300 #number of Decision Epochs
    n_episodes = 10

    actions_all_episodes = []

    for i in range(n_episodes):
        actions_taken, loss = get_solution(action_list, N)
        actions_all_episodes.append(actions_taken)

    # add one where we "reach the end" in less moves (it doesnt I just wanna see what happens)
    actions_all_episodes.append(random.choices(action_list, k = 50))
    
    # create a dictionary where the keys are the column names and the values are the inner lists
    data_dict = {f"actions_taken{i+1}": inner_list for i, inner_list in enumerate(actions_all_episodes)}

    # create a dataframe from the dictionary
    df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()

    print(df)
    df.to_csv('actions.csv', index=False)

main()