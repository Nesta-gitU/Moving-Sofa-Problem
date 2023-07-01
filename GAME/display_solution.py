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

        shape.move_forward_and_to_center(board)

        display.setShape(shape)
        display.show() 

        next_state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

    largest = shape.getLargeRectangle()
    print('hallo:', shape.getLargeRectangle().area)
    distance = board.get_distance_value(shape)

    if distance > 0:
        area = 0
        print('here')
    else:
        distance = 0
        area = largest.area
    
    return total_reward/N, largest, distance, area

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
        clock.tick(60)  # Adjust the frames per second (FPS) if needed
        pygame.event.pump()

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < delay:
            pygame.event.pump()

        action = action_list[i]
        shape.rotate(board, degrees=action)

        display.setShape(shape)
        display.show()

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < delay:
            pygame.event.pump()

        shape.move_forward_and_to_center(board)

        display.setShape(shape)
        display.show()

        next_state, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

    return 

def main1():
    actions_all_episodes = pd.read_csv('C:/Nesta/Bachelor thesis/Moving Couch split Area Value/Q_actions.csv')
    states_seen = pd.read_csv('states_seen.csv')

    h = Board.Board().h

    n_episodes = len(actions_all_episodes.columns) # put the same slicing here as below 

    rewards = []
    distances = []
    areas = []
    epsilons = []

    print(actions_all_episodes[actions_all_episodes.columns[-1]].dropna().tolist())

    last_row = actions_all_episodes[actions_all_episodes.columns[-1]]
    print(last_row)
    print(actions_all_episodes[actions_all_episodes.columns[-1]].equals(last_row))
    matching_columns = [col for col in actions_all_episodes.columns if actions_all_episodes[col].equals(last_row)] 
    print(matching_columns)

    # Get the index of the matching column
    column_index = actions_all_episodes.columns.get_loc(matching_columns[0])

    print(column_index + 1)
    

    for episode in actions_all_episodes.columns: 
        print(episode)
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        
        #states = states_seen[episode].dropna()
        #states = list(states)
        #print(states)
        N = len(actions)
        reward, largest, distance, area  = display_solution(actions, h, N)
        rewards.append(reward)
        distances.append(distance)
        areas.append(area)
        display.showPoly(largest)


    makeplots(n_episodes, rewards, distances, areas)

    print(actions_all_episodes[actions_all_episodes.columns[-1]].dropna().tolist())
    print(areas[-1])

    


    pygame.time.wait(1000)

def makeplots(n_episodes, rewards, distances, areas):
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
    
    plt.plot(range(n_episodes), areas)
    plt.xlabel('Episode')
    plt.ylabel('Area of Sofa')
    plt.grid()
    plt.show()


def main2():
    actions_all_episodes = pd.read_csv('C:/Nesta/Bachelor thesis/Moving Couch split Area Value/Q_actions.csv')
    h = Board.Board().h

    for episode in [actions_all_episodes.columns[-1]]: 
        print(episode)
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        N = len(actions)
        reward, largest, distance, area  =display_solution(actions, h, N)
        print('hallo:', largest.area)
        display.showPoly(largest)
        checkPoly(actions, h, N, largest)

    pygame.time.wait(1000)

main2()