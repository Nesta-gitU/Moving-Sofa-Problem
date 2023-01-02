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
    #self.update()
    
    # show updated image
    boardIm = Image.fromarray(self.grid * 255)
    self.ax.imshow(boardIm)
    plt.show(block = False)

    #print the array
    print(self.grid) 

  def setShape(self, shape):
    # first wipe away the previous shape and reset bounds
    self.grid = np.zeros(shape = (self.BOARDSIZE, self.BOARDSIZE))
    self.setBounds()

    # set the shape
    for coordinate in shape.coordinateList:
      self.grid[coordinate.x, coordinate.y] = 1


  def setBounds(self):
    order = len(str(self.BOARDSIZE)) 
    zeros = order - 1
    corridorSize = 10**zeros
    


    self.grid[0, :] = 1
    self.grid[corridorSize, 0:(self.BOARDSIZE - corridorSize)] = 1
    self.grid[corridorSize:self.BOARDSIZE, (self.BOARDSIZE - corridorSize)] = 1
    self.grid[:, self.BOARDSIZE - 1] = 1


