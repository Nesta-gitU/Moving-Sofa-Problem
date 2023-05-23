import Board
import Shape
import Display_board
import pygame
import pandas as pd
from shapely.geometry import Point, Polygon
import Moving_sofa_env
import matplotlib.pyplot as plt
import time
from shapely import affinity

pygame.init()

display = Display_board.Display_board()

def display_solution(action_list, h, N, states = None):
    env = Moving_sofa_env.Moving_sofa_env()
    board = Board.Board()
    point_list = env.getPointList()
    polygon = Polygon(point_list)
    shape = Shape.Shape(polygon = polygon, delay_rectangles= False)
    #display = Display_board.Display_board()
   

    total_reward = 0
    
    display.setShape(shape)
    display.show() 
    
    clock = pygame.time.Clock()
    delay = 0  # Delay in milliseconds (5 seconds)

    for i in range(N):
        clock.tick(60)  # Adjust the frames per second (FPS) if needed
        pygame.event.pump()

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < delay:
            pygame.event.pump()
        action = action_list[i]
        #print(states[i])
        
        shape.rotate(board, degrees = action)
        shape.moveForward(board, distance = h)

        shape.move_to_box_center(board)

        display.setShape(shape)
        display.show() 

        next_state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

    largest = shape.getLargeRectangle()
    print('hallo:', shape.getLargeRectangle().area)
    
    return total_reward, largest

def checkPoly(action_list, h, N, largest_polygon):
    env = Moving_sofa_env.Moving_sofa_env()
    board = Board.Board()
    shape = Shape.Shape(polygon=largest_polygon, delay_rectangles=False, collisionOn=False)
    
    point_list = env.getPointList()
    polygon = Polygon(point_list)
    shape = Shape.Shape(polygon = polygon, delay_rectangles= False, largest= largest_polygon)
    display = Display_board.Display_board(show_largest=True)

    total_reward = 0

    display.setShape(shape)
    display.show()

    clock = pygame.time.Clock()
    delay = 1000  # Delay in milliseconds (5 seconds)

    for i in range(N):
        print('test')
        clock.tick(60)  # Adjust the frames per second (FPS) if needed
        pygame.event.pump()

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < delay:
            pygame.event.pump()

        action = action_list[i]
        shape.rotate(board, degrees=action)

        display.setShape(shape)
        display.show()

        #start_time = pygame.time.get_ticks()
        #while pygame.time.get_ticks() - start_time < delay:
        #    pygame.event.pump()


        shape.moveForward(board, distance=h)

        display.setShape(shape)
        display.show()

        shape.move_to_box_center(board)

        display.setShape(shape)
        display.show()

        next_state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

    return

def main1():
    actions_all_episodes = pd.read_csv('actions.csv')
    states_seen = pd.read_csv('states_seen.csv')

    h = Board.Board().h

    rewards = []

    for episode in actions_all_episodes.columns[::9]: 
        print(episode)
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        
        #states = states_seen[episode].dropna()
        #states = list(states)
        #print(states)
        N = len(actions)
        reward, largest =display_solution(actions, h, N)
        rewards.append(reward)
        display.showPoly(largest)

    
    pygame.time.wait(1000)
    
    plt.plot(range(len(rewards)), rewards)
    plt.show()

def main2():
    actions_all_episodes = pd.read_csv('Q_actions.csv')
    h = Board.Board().h

    for episode in [actions_all_episodes.columns[-1]]: 
        print(episode)
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        N = len(actions)
        reward, largest =display_solution(actions, h, N)
        display.showPoly(largest)
        checkPoly(actions, h, N, largest)



    
    pygame.time.wait(1000)
main1()