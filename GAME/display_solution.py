import Board
import Shape
import Display_board
import pygame
import pandas as pd
from shapely.geometry import Point, Polygon
import time

pygame.init()

display = Display_board.Display_board()

def display_solution(action_list, h, N, states = None):
    point_list = getPointList()
    polygon = Polygon(point_list)
    shape = Shape.Shape(polygon = polygon, delay_rectangles= True)
    board = Board.Board()
    
    
    for i in range(N):
        #time.sleep(1)
        action = action_list[i]
        #print(states[i])
        
        shape.rotate(board, degrees = action)
        shape.moveForward(board, distance = h)

        display.setShape(shape)
        display.show()
    print('hallo:', shape.getLargeRectangle().area)

    return shape.getLargeRectangle()
    
    

        
def getPointList():
    point = Point(0.1000, 0.5000)
    
    point_list = point.buffer(0.1).exterior.coords
    return point_list


def main():
    actions_all_episodes = pd.read_csv('Q_actions-new.csv')
    states_seen = pd.read_csv('states_seen.csv')

    h = Board.Board().h

    for episode in actions_all_episodes.columns[10:500:10]:
        print(episode)
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        
        #states = states_seen[episode].dropna()
        #states = list(states)
        #print(states)
        N = len(actions)
        largest = display_solution(actions, h, N)
    display.showPoly(largest)
    pygame.time.wait(1000)
    
        

main()