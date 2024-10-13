# AUTHOR: JAG
# DATE: [2024]
# DESCRIPTION: Central Controlling class for agent and environment capabilities.

from agent import qAgent
from loader import Loader
import grid_world_environment_utils

import fnmatch
import numpy as np
import pygame
import random
import sys

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
            env_rows = len(self.environment)
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
            self.agent = qAgent(self.environment.shape,
                                loader.get_agent_parameters(self.agent_path[0]),
                                loader.get_agent_qtable(self.agent_path[1]))
        elif fnmatch.fnmatch(self.agent_path[0], '*.agent.yaml'):
            self.agent = qAgent(self.environment.shape, loader.get_agent_parameters(self.agent_path[0]), None)
        elif fnmatch.fnmatch(self.agent_path[1], '*.agent.csv'):
            self.agent = qAgent(self.environment.shape, None, loader.get_agent_qtable(self.agent_path[1]))
        else:
            raise FileExistsError("Agent file not found or invalid filetype used.")

    ##
    # If enabled, agent training or testing
    def start(self, num_epochs : int, win_size : tuple = (1080, 720)):
        if self.show_world:
            # Initialize pygame internals
            pygame.init()
            self.screen, self.clock, grid_tile_width, grid_tile_height = grid_world_environment_utils.init_pygame_world(win_size, self.environment)

        running = True

        # Start main event loop
        for epoch in range(num_epochs):
            while running and self.environment[self.agent.current_env_state[0], self.agent.current_env_state[1]] != 1:
                self.agent.learn()

                if self.show_world:
                    # Check if the user manually stopped the session
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    self.screen.fill('white')

                    grid_world_environment_utils.draw_grid(self.screen, grid_tile_width, grid_tile_height, win_size)
                    grid_world_environment_utils.draw_agent(self.screen, grid_tile_width, grid_tile_height, self.agent.current_env_state)

                    pygame.display.flip()
                    self.clock.tick(60)

                if self.environment[self.agent.current_env_state[0], self.agent.current_env_state[1]] == 1:
                    print("Reward found!")

            if running == False:
                self.stop()

            epoch += 1

        self.stop()

    def stop(self):
        try:
            pygame.quit()
        except:
            sys.exit(-1)
    ##
    # Save the generated world
    def save_world(self):
        np.savetxt("world.csv", self.environment, delimiter=",")