# AUTHOR: JAG
# DATE: [2024]
# DESCRIPTION: Main execution file.

from grid_world_control import GridWorldController

import logging

dimensions : tuple = (5, 5)
save_world : bool = False
show_world : bool = True


num_epochs : int = 100

def main():
    logging.info("Launching Application")

    path = '/home/jag1799/Documents/vscode_ws/Grid-Q-Learner/world.csv'
    controller = GridWorldController(dimensions, show_world=show_world)
    controller.start(num_epochs=num_epochs)
    if save_world:
        controller.save_world()

if __name__ == '__main__':
    main()