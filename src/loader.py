import numpy as np
import yaml

class Loader():

    def __init__(self):
        pass
    
    ##
    # Parses a yaml file and reads the environment's user defined parameters for a new environment.
    def get_world_parameters(self, env_params_path : str) -> dict:
        env_content : dict = {}
        try:
            with open(env_params_path, "r") as file:
                env_content = yaml.load(file, Loader=yaml.Loader)
            file.close()
        except:
            raise FileNotFoundError

        keys = env_content.keys()
        if 'rows' not in keys and 'columns' not in keys:
            raise LookupError            

        return env_content
    
    ##
    # Parses a yaml file and reads the agent's user defined hyperparameters in.
    def get_agent_parameters(self, agent_params_path : str) -> dict:
        agent_content : dict = {}
        try:
            with open(agent_params_path, "r") as file:
                agent_content = yaml.load(agent_params_path, Loader=yaml.Loader)
            file.close()
        except:
            raise FileNotFoundError        

        return agent_content

    ##
    # Loads a grid world preset from a CSV file.
    def load_world_preset(self, env_preset_path : str):
        return np.loadtxt(env_preset_path, delimiter=',', dtype=int)