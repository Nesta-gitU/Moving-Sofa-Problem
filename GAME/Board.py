import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt

#Board should only be for display. And to store the boundaries. 
#So like the display in the snake game
class Board:
  BOARDSIZE = 400

  def __init__(self):
    self.grid = np.zeros(shape = (self.BOARDSIZE, self.BOARDSIZE))
    self.setBounds()

    # set up the view window
    fig, self.ax = plt.subplots()
    boardIm = Image.fromarray(self.grid * 255)
    self.ax.imshow(boardIm)
    plt.show(block = False)

  def show(self):
    #update the array before showing
    self.update()
    
    # show updated image
    boardIm = Image.fromarray(self.grid * 255)
    self.ax.imshow(boardIm)
    plt.show(block = False)

    print(self.grid)

  def update(self):
    self.grid[40:60, 40:60] = 1


  def setBounds(self):
    self.grid[0, :] = 1
    self.grid[100, 0:300] = 1
    self.grid[100:400, 299] = 1
    self.grid[:, 399] = 1


