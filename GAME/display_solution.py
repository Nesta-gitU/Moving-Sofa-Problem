import Board
import Shape
import Display_board
import pygame
import pandas as pd
from shapely.geometry import Point, Polygon

pygame.init()

def display_solution(action_list, h, N):
    point_list = getPointList()
    polygon = Polygon(point_list)
    shape = Shape.Shape(polygon = polygon)
    board = Board.Board()
    display = Display_board.Display_board()
    
    for i in range(N):
        pygame.time.wait(1)
        action = action_list[i]
        
        shape.rotate(board, degrees = action)
        shape.moveForward(board, distance = h)

        display.setShape(shape)
        display.show()

        
def getPointList():
    point = Point(0.1000, 0.5000)
    
    point_list = point.buffer(0.1).exterior.coords
    return point_list


def main():
    actions_all_episodes = pd.read_csv('actions.csv')

    h = actions_all_episodes['h'][0]

    actions_all_episodes = actions_all_episodes.drop('h', axis=1)
    #actions_all_episodes = actions_all_episodes.drop('actions_taken4', axis=1)

    for episode in actions_all_episodes.columns:
        print(episode)
        print('wtf')
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        N = len(actions)
        display_solution(actions, h, N)


main()