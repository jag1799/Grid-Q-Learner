# AUTHOR: JAG
# DATE: [2024]
# DESCRIPTION: Main execution file.

from grid_world_controller import GridEnvironmentController

save_world : bool = False
show_world : bool = True

def main():

    world_path = '/home/jag1799/Documents/vscode_ws/Grid-Q-Learner/src/config/cfg1.world.yaml'
    agent_info = ('/home/jag1799/Documents/vscode_ws/Grid-Q-Learner/src/config/cfg1.agent.yaml',
                  '/home/jag1799/Documents/vscode_ws/Grid-Q-Learner/src/config/cfg1.agent.csv')
    controller = GridEnvironmentController(env_path=world_path, agent_path=agent_info, show_world=show_world)
    controller.start(num_epochs=controller.agent.num_epochs)
    if save_world:
        controller.save_world()

if __name__ == '__main__':
    main()