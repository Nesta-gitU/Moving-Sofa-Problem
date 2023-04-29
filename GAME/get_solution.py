import Board
import Shape
from shapely.geometry import Point, Polygon
import random
import pandas as pd

def get_solution(action_list, h, N):
    point_list = getPointList()
    polygon = Polygon(point_list)
    shape = Shape.Shape(polygon = polygon)
    board = Board.Board()

    actions_taken = []
    
    for i in range(N):
        action = random.sample(action_list, 1)[0]

        shape.rotate(board, degrees = action)
        shape.moveForward(board, distance = h)

        actions_taken.append(action)

        if board.is_finished(shape):
            loss = 0
            return actions_taken, loss
    
    loss = board.get_distance_value(shape)
    return actions_taken, loss

        
def getPointList():
    point = Point(0.1000, 0.5000)
    
    point_list = point.buffer(0.1).exterior.coords
    return point_list


def main():
    #######parameters#######
    action_list = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90] #because of the weird grid no minusus. I guess just put minusus in the final paper. 
    N = 100 #number of Decision Epochs
    h = 0.5 #travel distance and bucket size
    n_episodes = 10

    actions_all_episodes = []

    for i in range(n_episodes):
        actions_taken, loss = get_solution(action_list, h, N)
        actions_all_episodes.append(actions_taken)

    # add one where we "reach the end" in less moves (it doesnt I just wanna see what happens)
    actions_all_episodes.append(random.choices(action_list, k = 50))
    
    # create a dictionary where the keys are the column names and the values are the inner lists
    data_dict = {f"actions_taken{i+1}": inner_list for i, inner_list in enumerate(actions_all_episodes)}

    # create a dataframe from the dictionary
    df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()
    df['h'] = h

    print(df)
    df.to_csv('actions.csv', index=False)

main()