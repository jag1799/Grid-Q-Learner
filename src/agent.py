# AUTHOR: JAG
# TIME: [2024]
# DESCRIPTION: Agent class where the Q-Learning algorithm sits.

import grid_world_environment_utils

import numpy as np

class qAgent():

    def __init__(self, dim : tuple, params : dict = None, qTable : np.array = None) -> None:
        self.dimensions = dim
        self.epsilon = 0
        self.gamma = 0
        self.alpha = 0
        self.num_epochs = 0

        # These will be constant variables
        self.num_actions = 4 # Up, Down, Left, Right
        self.num_states = dim[0] * dim[1] # Row for each possible position in the environment

        # Initialize parameters and Q-Table
        self._load_agent_params_(params)
        self._init_q_table_(qTable)

        # Dynamic Values
        self.current_q_state = [0, 0]
        self.current_env_state = [0, 0]
        self.reward = 0

    ##
    # Stores the agent parameters for training.
    def _load_agent_params_(self, params):
        if params != None:
            try:
                self.epsilon    = params['epsilon']
                self.gamma      = params['gamma']
                self.alpha      = params['alpha']
                self.num_epochs = params['num_epochs']
            except:
                raise KeyError("Params dict has invalid keys!")
        else:
            raise NotImplementedError("Params dict must be initialized for agent to function.")

    ##
    # Internal utility in case we need to reinitialize the Q-Table
    def _init_q_table_(self, qTable : np.array):
        try:
            if qTable.all() != None:
                self.q_table = qTable
        except:
            print("No Q table file found.  Initializing new Q table.")
            self.q_table = np.zeros((self.num_states, self.num_actions), dtype=np.float16)

    ##
    # Do a complete action and self update in the current time step
    def learn(self):

        action = self.choose_action()

        self.perform_action(action)

    ##
    # Chooses an action using the Greedy epsilon Method
    def choose_action(self):
        if np.random.randint(0, 1) < self.epsilon:
            action = np.random.randint(0, self.num_actions) # No known best actions, so choose one and explore
        else:
            action = np.argmax(self.q_table[self.current_q_state, :]) # Select the best action in the current row
        self.epsilon -= self.alpha # Decrease the exploration probability slightly.
        return action

    def perform_action(self, action : int):
        if action == 0: # Move up
            # Check boundary condition
            if self.current_env_state[0] == 0:
                return
            self.current_env_state[0] -= 1
        elif action == 1: # Move Down
            if self.current_env_state[0] == self.dimensions[0] - 1:
                return
            self.current_env_state[0] += 1
        elif action == 2: # Move Right:
            if self.current_env_state[1] == self.dimensions[1] - 1:
                return
            self.current_env_state[1] += 1
        elif action == 3: # Move Left:
            if self.current_env_state[1] == 0:
                return
            self.current_env_state[1] -= 1

    def measure_reward(self):
        pass

    def update_q_table(self):
        pass