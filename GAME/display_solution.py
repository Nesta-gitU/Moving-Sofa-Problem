import Board
import Shape
import Display_board
import pygame
import pandas as pd
from shapely.geometry import Point, Polygon
import Moving_sofa_env
import matplotlib.pyplot as plt

pygame.init()

def display_solution(action_list, h, N, states = None):
    point_list = getPointList()
    polygon = Polygon(point_list)
    shape = Shape.Shape(polygon = polygon)
    board = Board.Board()
    display = Display_board.Display_board()
    env = Moving_sofa_env.Moving_sofa_env()

    total_reward = 0
    
    for i in range(N):
        #pygame.time.wait(1)
        action = action_list[i]
        #print(shape.polygon.centroid)
        #print(action)
        
        shape.rotate(board, degrees = action)
        shape.moveForward(board, distance = h)

        display.setShape(shape)
        display.show() 

        shape.move_to_box_center(board)

        display.setShape(shape)
        display.show() 

        next_state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
    
    return total_reward



        
def getPointList():
    point = Point(0.1000, 0.5000)
    
    point_list = point.buffer(0.1).exterior.coords
    return point_list


def main():
    actions_all_episodes = pd.read_csv('Q_actions.csv')
    states_seen = pd.read_csv('states_seen.csv')

    h = Board.Board().h
    print(h)

    rewards = []

    for episode in [actions_all_episodes.columns[-1]]:
        print(episode)
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        
        #states = states_seen[episode].dropna()
        #states = list(states)
        #print(states)
        N = len(actions)
        reward =display_solution(actions, h, N)
        rewards.append(reward)
    
    plt.plot(range(len(rewards)), rewards)
    plt.show()
    
main()