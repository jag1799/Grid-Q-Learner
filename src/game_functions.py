# AUTHOR: JAG
# TIME: [2024]
# DESCRIPTION: Internal functions that control the state of the world.

import logging
import numpy as np
import pandas as pd
import random
import sys


class GridWorldController():

    def __init__(self, 
                 dimensions : tuple = (), 
                 env_path : str = None,
                 save_world : bool = False) -> None:

        self.dimensions = dimensions
        self.environment = None

        if (len(dimensions) != 0 and env_path != None):
            logging.warning("Both environment initializers set.  Using tuple definition.")
            self.environment = np.zeros(shape=(dimensions[0], dimensions[1]))
            self.insertReward()

        elif len(dimensions) == 0:
            if env_path == None:
                logging.critical("GridWorldController() must have a world to initialize!")
                sys.exit(1)
            else:
                self.load_world(env_path)
        else:
            self.environment = np.zeros(shape=(dimensions[0], dimensions[1]))
            self.insertReward()
        
        if save_world:
            self.save_world()
    
    # Load an already created world for training.
    def load_world(self, env_path : str):
        self.environment = np.loadtxt(env_path, delimiter=",", dtype=int)

    def save_world(self):
        np.savetxt("world.csv", self.environment, delimiter=",")

    def insertReward(self):
        env_rows = len(self.environment)
        env_cols = len(self.environment[0])
        self.environment[random.randint(0, env_rows-1)][random.randint(0, env_cols-1)] = 1