# AUTHOR: JAG
# DATE: [2024]
# DESCRIPTION: Main execution file.

from grid_world_controller import GridEnvironmentController
from loader import Loader

save_world   : bool = False
show_world   : bool = True
save_q_table : bool = False

def main():

    world_load_path = ''
    world_save_path = ''

    # Format must be ('*.agent.yaml', '*.agent.csv') if both filetypes are being included.  Otherwise,
    # leave an empty string for whichever file is not being used. Ex ('*.agent.yaml', '')
    agent_load_info = ('', '')
    agent_save_path = ''

    loader = Loader()
    controller = GridEnvironmentController(loader, env_path=world_load_path, agent_path=agent_load_info, show_world=show_world)
    controller.start(num_epochs=controller.agent.num_epochs)

    if save_world:
        loader.save_world(controller.environment, world_save_path)

    if save_q_table:
        loader.save_q_table(controller.agent.q_table, agent_save_path)

if __name__ == '__main__':
    main()