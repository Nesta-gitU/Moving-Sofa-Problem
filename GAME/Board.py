import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt
import pygame

#Board should only be for display. And to store the boundaries. 
#So like the display in the snake game
class Board:
  BOARDSIZE = 400

  def __init__(self):
    self.grid = np.zeros(shape = (self.BOARDSIZE, self.BOARDSIZE))
    self.setBounds()

    # set up the view window
    self.scrn = pygame.display.set_mode((self.BOARDSIZE, self.BOARDSIZE))
 
    # set the pygame window name
    pygame.display.set_caption('image')

  def show(self):
    #update the array before showing
    #self.update()
    
    # show updated image
    # Create a Pygame surface from the NumPy array
    surface = pygame.surfarray.make_surface(self.grid * 255)
 
    # Using blit to copy content from one surface to other
    self.scrn.blit(surface, (0, 0))
 
    # paint screen one time
    pygame.display.update()

    #print the array
    #print(self.grid) 

  def setShape(self, shape):
    # first wipe away the previous shape and reset bounds
    self.grid = np.zeros(shape = (self.BOARDSIZE, self.BOARDSIZE))
    self.setBounds()

    # set the shape
    for coordinate in shape.coordinateList:
      self.grid[round(coordinate.x), round(coordinate.y)] = 1


  def setBounds(self):
    order = len(str(self.BOARDSIZE)) 
    zeros = order - 1
    corridorSize = 10**zeros
    


    self.grid[:, 0] = 1
    self.grid[0:(self.BOARDSIZE - corridorSize), corridorSize] = 1
    self.grid[(self.BOARDSIZE - corridorSize), corridorSize:self.BOARDSIZE] = 1
    self.grid[self.BOARDSIZE - 1, :] = 1


