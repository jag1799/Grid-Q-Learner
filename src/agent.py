# AUTHOR: JAG
# TIME: [2024]
# DESCRIPTION: Agent class where the Q-Learning algorithm sits.

import numpy as np

class qAgent():

    '''
    - **dim**: *tuple*
        - Dimensions of the environment.  Used to create the Q-Table.
    - **reward_row**: *int*
        - Row that contains the reward.  Unknown the agent, but used for rewarding it.
    - **reward_column**: *int*
        - Column that contains the reward.  Unknown to the agent, but used for rewarding it.
    - **params**: *dict*
        - Dictionary containing loaded parameters.
    - **qTable**: *np.array* = None
        - Optional parameter containing a pre-existing Q-Table.  Must be loaded from main driver before use.
    '''
    def __init__(self, dim : tuple, reward_row : int, reward_column : int, params : dict, qTable : np.array = None) -> None:
        self.reward_row = reward_row
        self.reward_column = reward_column
        self.dimensions = dim
        self.epsilon = 0
        self.epsilon_decay = 0
        self.gamma = 0
        self.alpha = 0
        self.min_epsilon = 0
        self.num_epochs = 0

        # These will be constant variables
        self.num_actions = 4 # Up, Down, Left, Right
        self.num_states = dim[0] * dim[1] # Row for each possible position in the environment

        # Initialize parameters and Q-Table
        self._load_agent_params_(params)
        self._init_q_table_(qTable)

        # Dynamic Values
        self.current_q_state = 0
        self.current_env_state = [0, 0]
        self.reward = 0

    ##
    # Stores the agent parameters for training.
    def _load_agent_params_(self, params):
        if params != None:
            try:
                self.epsilon     = params['epsilon']
                self.gamma       = params['gamma']
                self.alpha       = params['alpha']
                self.num_epochs  = params['num_epochs']
                self.min_epsilon = params['min_exploration_probability']
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
        t_reward = self.perform_action(action)

        next_q_row = (self.current_q_state + 1) % self.num_states

        self.q_table[self.current_q_state, action] += self.alpha * (t_reward + self.gamma * np.max(self.q_table[next_q_row]))

        self.current_q_state = next_q_row

    ##
    # Chooses an action using the Greedy epsilon Method
    def choose_action(self):
        if np.random.randint(0, 1) < self.epsilon:
            action = np.random.randint(0, self.num_actions - 1) # No known best actions, so choose one and explore
            if self.epsilon > self.min_epsilon: # Allow for a small constant probability for the agent to continue exploring to avoid local minima over time.
                self.epsilon -= self.alpha # Decrease the exploration probability slightly.
        else:
            action = np.argmax(self.q_table[self.current_q_state, :]) # Select the best action in the current row
        return action

    def perform_action(self, action : int) -> int:
        if action == 0: # Move up
            # Check boundary condition
            if self.current_env_state[0] == 0: # Keep the agent from moving up beyond the screen
                return -0.001
            self.current_env_state[0] -= 1
        elif action == 1: # Move Down
            if self.current_env_state[0] == self.dimensions[0]-1: # Keep agent from moving down beyond the screen
                return -0.001
            self.current_env_state[0] += 1
        elif action == 2: # Move Right:
            if self.current_env_state[1] == self.dimensions[1]-1: # Keep agent from moving right off the screen.
                return -0.001
            self.current_env_state[1] += 1
        elif action == 3: # Move Left:
            if self.current_env_state[1] == 0: # Keep agent from moving left off the screen
                return -0.001
            self.current_env_state[1] -= 1

        # Target was found, reward the agent
        if self.current_env_state[0] == self.reward_row and self.current_env_state[1] == self.reward_column:
            return 1
        return 0

    def reset(self):
        self.current_env_state = [0, 0]
        self.current_q_state = 0