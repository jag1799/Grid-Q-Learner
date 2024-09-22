import numpy as np
import yaml

class Loader():

    """
    - **env_preset_path**: *str*, *soft-required*
        - Relative or absolute path to an existing CSV file with a created world. Required if an **env_params_path** is not provided.
    - **agent_preset_path**: *str*, *soft-required*
        - Relative or absolute path to an existing CSV file containing a Q-Table.  Required if **agent_params_path** is not provided.
    - **env_params_path**: *str*, *soft-required*
        - Relative or absolute path to an existing YAML file containing parameters for a world.  Required if **env_preset_path** is not provided.
    - **agent_params_path**: *str*, *soft-required*
        - Relative or absolute path to an existing YAML file containing parameters for an agent. Required if **agent_preset_path** is not provided.
    """
    def __init__(self,
                 env_preset_path : str = None,
                 agent_preset_path : str = None,
                 env_params_path : str = None, 
                 agent_params_path: str = None):
        self.env_preset_path = env_preset_path
        self.agent_preset_path = agent_preset_path
        self.env_params_path = env_params_path
        self.agent_params_path = agent_params_path
    
    ##
    # Parses a yaml file and reads the environment's user defined parameters for a new environment.
    def get_world_parameters(self) -> dict:
        env_content : dict = {}
        with open(self.env_params_path, "r") as file:
            env_content = yaml.load(file, Loader=yaml.Loader)
        file.close()

        return env_content

    def load_world(self):
        return np.loadtxt()
    ##
    # Parses a yaml file and reads the agent's user defined hyperparameters in.
    def get_agent_file(self) -> dict:
        agent_content : dict = {}
        with open(self.agent_params_path, "r") as file:
            agent_content = yaml.load(self.agent_params_path, Loader=yaml.Loader)
        file.close()

        return agent_content