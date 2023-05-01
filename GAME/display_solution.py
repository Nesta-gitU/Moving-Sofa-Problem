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

    h = Board.Board().h

    for episode in actions_all_episodes.columns:
        print(episode)
        actions = actions_all_episodes[episode].dropna()
        actions = list(actions)
        N = len(actions)
        display_solution(actions, h, N)

main()