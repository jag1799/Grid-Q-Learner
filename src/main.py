# AUTHOR: JAG
# DATE: [2024]
# DESCRIPTION: Main execution file.

from game_functions import GridWorldController

import logging

def main():
    logging.info("Launching Application")

    path = '/home/jag1799/Documents/vscode_ws/Grid-Q-Learner/world.csv'
    controller = GridWorldController((5, 5), save_world=True)
    pass

if __name__ == '__main__':
    main()