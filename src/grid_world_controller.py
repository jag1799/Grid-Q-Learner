from agent import qAgent
from loader import Loader

import fnmatch
import numpy as np
import pygame
import random

class GridEnvironmentController:

    """
    - **path**: *str*
        - Path to a configuration file for presets or new world/agent parameters.  Required if **dims** \
          is *None*.
    - **show_world**: *bool*
        - Flag to indicate whether to open Pygame window for training/testing visualization or not. Always required.
    """
    def __init__(self, env_path : str, agent_path : tuple, show_world : bool = True):
        self.agent_path = agent_path
        self.env_path = env_path
        self.show_world = show_world
    
        self.__set_environment__()
    
    ##
    # Insert a reward in a random position in the Grid world that isn't the agent's starting position.
    def __insert_reward__(self):
        try:
            env_rows = len(self.environment[0])
            env_cols = len(self.environment[1])
            self.environment[random.randint(1, env_rows-1)][random.randint(1, env_cols-1)] = 1
        except:
            raise AttributeError("Environment variable has not been initialized.")

    ##
    # Set the environment variable upon initialization of the controller.
    def __set_environment__(self):
        loader = Loader()

        if fnmatch.fnmatch(self.env_path, '*.world.yaml'):
            environment_params = loader.get_world_parameters(self.env_path)
            self.environment = np.zeros(shape=(int(environment_params['rows']), int(environment_params['columns'])))
            self.__insert_reward__()
        elif fnmatch.fnmatch(self.env_path, '*.world.csv'):
            self.environment = loader.load_world_preset(self.env_path)
        else:
            raise FileExistsError("Environment File not found or invalid filetype used.")
        
        # Either load agent q table, hyperparameters, or both
        if fnmatch.fnmatch(self.agent_path[0], '*.agent.yaml') and fnmatch.fnmatch(self.agent_path[1], '*.agent.csv'):
            self.agent = qAgent(self.environment.shape, loader.get_agent_parameters(self.agent_path[0]), loader.get_agent_qtable(self.agent_path[1]))
        elif fnmatch.fnmatch(self.agent_path[0], '*.agent.yaml'):
            self.agent = qAgent(self.environment.shape, loader.get_agent_parameters(self.agent_path[0]), None)
        elif fnmatch.fnmatch(self.agent_path[1], '*.agent.csv'):
            self.agent = qAgent(self.environment.shape, None, loader.get_agent_qtable(self.agent_path[1]))
        else:
            raise FileExistsError("Agent file not found or invalid filetype used.")
    
    ##
    # If enabled, start pygame viewer and environment updates.
    # def start(self, num_epochs : int, win_size : tuple = (1080, 720)):

    #     if self.show_world:
    #         # Initialize pygame internals
    #         pygame.init()
    #         self.screen = pygame.display.set_mode(win_size)
    #         self.clock = pygame.time.Clock()

    #         # Initialize other environment settings.
    #         grid_tile_width = win_size[0] / self.dimensions[0] # Width of a grid tile in pixels
    #         grid_tile_height = win_size[1] / self.dimensions[1] # Height of a grid tile in pixels

    #     self.running = True
        
    #     # Initialize Agent
    #     epoch = 0
    #     agent = qAgent(self.dimensions)

    #     # Start main event loop
    #     while self.running and epoch < num_epochs:
            
    #         if self.show_world:
    #             # Check if the user manually stopped the session
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     self.running = False
    #             self.screen.fill('white')

    #             self.draw_grid(grid_tile_width, grid_tile_height, win_size)

    #             pygame.display.flip()
    #             self.clock.tick(60)
            
    #         epoch += 1

    #     self.stop()
    
    ##
    # Save the generated world
    def save_world(self):
        np.savetxt("world.csv", self.environment, delimiter=",")