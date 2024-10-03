# AUTHOR: JAG
# TIME: [2024]
# DESCRIPTION: Internal functions that control the state of the world.

from agent import qAgent
from loader import Loader

# From standard Python modules.
import logging
import numpy as np
import pygame
import random
import sys

# Controller for the Grid World internals. Internals, world loading, world saving,
# and all other core functions are done here.
class GridWorldController():

    def __init__(self,
                 dimensions : tuple = (), 
                 env_path : str = None,
                 show_world : bool = False) -> None:

        self.dimensions = dimensions
        self.environment = None
        self.show_world = show_world

        self.loader = Loader()

        # Default to creating a new world if both variables are set.
        if (len(dimensions) != 0 and env_path != None):
            logging.warning("Both environment initializers set.  Using tuple definition.")
            self.environment = np.zeros(shape=(dimensions[0], dimensions[1]))
            self.insert_reward()

        elif len(dimensions) == 0:
            if env_path == None:
                logging.critical("The controller must have a world to initialize!")
                sys.exit(-1)
            else:
                # Load an existing world from a CSV file.
                self.load_world(env_path)
        else:
            # Create a new world with a randomly placed reward.
            self.environment = np.zeros(shape=(dimensions[0], dimensions[1]))
            self.insert_reward()
    
    # Load an already created world for training.
    def load_world(self, env_path : str):
        self.environment = np.loadtxt(env_path, delimiter=",", dtype=int)

    # Save a newly created world in a CSV for future use.
    def save_world(self):
        for val in self.environment:
            val = int(val)
        np.savetxt("world.csv", self.environment, delimiter=",")

    # Insert a reward at a random spot in the world.
    def insert_reward(self):
        env_rows = len(self.environment)
        env_cols = len(self.environment[0])
        self.environment[random.randint(1, env_rows-1)][random.randint(1, env_cols-1)] = 1
    
    ##
    # If enabled, start pygame viewer and environment updates.
    def start(self, num_epochs : int, win_size : tuple = (1080, 720)):

        if self.show_world:
            # Initialize pygame internals
            pygame.init()
            self.screen = pygame.display.set_mode(win_size)
            self.clock = pygame.time.Clock()

            # Initialize other environment settings.
            grid_tile_width = win_size[0] / self.dimensions[0] # Width of a grid tile in pixels
            grid_tile_height = win_size[1] / self.dimensions[1] # Height of a grid tile in pixels

        self.running = True
        
        # Initialize Agent
        epoch = 0
        agent = qAgent(self.dimensions)

        # Start main event loop
        while self.running and epoch < num_epochs:
            
            if self.show_world:
                # Check if the user manually stopped the session
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                self.screen.fill('white')

                self.draw_grid(grid_tile_width, grid_tile_height, win_size)

                pygame.display.flip()
                self.clock.tick(60)
            
            epoch += 1

        self.stop()
    
    def stop(self):
        try:
            pygame.quit()
        except:
            sys.exit(-1)
    
    def draw_grid(self, width, height, win_size):
        for row in range(0, win_size[0], int(width)):
            for col in range(0, win_size[1], int(height)):
                rect = pygame.Rect(row, col, width, height)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

