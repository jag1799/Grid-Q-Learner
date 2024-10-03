# AUTHOR: JAG
# TIME: [2024]
# DESCRIPTION: Agent class where the Q-Learning algorithm sits.

import numpy as np


class qAgent():

    def __init__(self, dim : tuple, params : dict = None, qTable : np.array = None) -> None:
        self.dimensions = dim
        self.num_actions = 4 # Up, Down, Left, Right
        self.num_states = dim[0] * dim[1] # Row for each possible position in the environment

        self.q_table = np.zeros((self.num_states, self.num_actions), dtype=np.float16)
        print(self.q_table)
    
    # Internal utility in case we need to reinitialize the Q-Table
    def init_q_table(self):
        self.q_table = np.zeros((self.num_states, self.num_actions), dtype=np.float16)
