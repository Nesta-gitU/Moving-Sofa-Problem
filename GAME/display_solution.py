import Board
import Shape
import Display_board
import pygame
import pandas as pd
from shapely.geometry import Point, Polygon
import Moving_sofa_env
import matplotlib.pyplot as plt
import math

pygame.init()

def display_solution(action_list, h, N, states = None):
    env = Moving_sofa_env.Moving_sofa_env()
    point_list = getPointList(env)
    polygon = Polygon(point_list)
    shape = Shape.Shape(polygon = polygon)
    board = Board.Board()

    display = Display_board.Display_board()
    
    display.setShape(shape)
    display.show() 

    total_reward = 0
    distance_travelled = 0
    finished = False
    
    for i in range(N):
        #pygame.time.wait(1)
        action = action_list[i]
        #print(shape.polygon.centroid)
        #print(action)

        previous_centroid = shape.polygon.centroid
        
        shape.rotate(board, degrees = action)
        shape.moveForward(board, distance = h)

        display.setShape(shape)
        display.show() 

        shape.move_to_box_center(board)

        current_centroid = shape.polygon.centroid

        dx = current_centroid.x - previous_centroid.x
        dy = current_centroid.y - previous_centroid.y
        distance = math.sqrt(dx**2 + dy**2)
        distance_travelled += distance

        display.setShape(shape)
        display.show() 


        next_state, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            finished = True
            

        total_reward += reward

    distance_left = board.get_distance_value(shape)

    if distance_left < 0:
        distance_left = 0
    
    
    return total_reward/N, distance_left, distance_travelled, finished



        
def getPointList(env):
    point = env.get_middle_box_center()
    
    point_list = point.buffer(0.1).exterior.coords
    return point_list


def main():
    actions_all_episodes = pd.read_csv('C:/Nesta/Bachelor thesis/Moving Couch split display and solution/Q_actions.csv')
    states_seen = pd.read_csv('C:/Nesta/Bachelor thesis/Moving Couch split display and solution/states_seen.csv')

    h = Board.Board().h
    print(h)

    rewards = []
    distances = []
    distances_travelled = []
    finished_list = []

    n_episodes = len(actions_all_episodes.columns)

    for episode in actions_all_episodes.columns[400:500]:
        print(episode)
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        print(actions)
        
        #states = states_seen[episode].dropna()
        #states = list(states)
        #print(states)
        N = len(actions)
        reward, distance, distance_travelled, finished =display_solution(actions, h, N)
        rewards.append(reward)
        distances.append(distance)
        distances_travelled.append(distance_travelled)
        finished_list.append(finished)

    print('final_distance_travelled:', distances_travelled[-1])

    makeplots(n_episodes, rewards, distances, distances_travelled, finished_list)
    

def makeplots(n_episodes, rewards, distances, distances_travelled, finished_list):
    print(finished_list)
    color_list = ['green' if finished else 'red' for finished in finished_list]

    plt.plot(range(n_episodes), rewards)
    plt.xlabel('Episode')
    plt.ylabel('Average Reward per Action')
    plt.grid()
    plt.show()

    plt.plot(range(n_episodes), distances)
    plt.xlabel('Episode')
    plt.ylabel('Remaining Distance to Finish')
    plt.grid()
    plt.show()

    plt.scatter(range(n_episodes), distances_travelled, c=color_list, cmap='viridis')
    plt.plot(range(n_episodes), distances_travelled, c='black', linewidth=1)
    plt.xlabel('Episode')
    plt.ylabel('Total Distance Travelled')
    plt.grid(True)
    #plt.colorbar(label='Color')
    plt.show()

main()