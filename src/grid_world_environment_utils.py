# AUTHOR: JAG
# DATE: [2024]
# DESCRIPTION: Environment specific utilities to decrease complexity of controller and agent classes.

import pygame

tile_coordinates = list()

##
# Initialize the pygame world before drawing anything.
def init_pygame_world(win_size, environment):
    screen = pygame.display.set_mode(win_size)
    clock = pygame.time.Clock()
    global quarter_tile_width
    global quarter_tile_height

    # Initialize other environment settings.
    grid_tile_width = win_size[0] / len(environment[0]) # Width of a grid tile in pixels. Used for columns.
    grid_tile_height = win_size[1] / len(environment) # Height of a grid tile in pixels Used for rows
    quarter_tile_width = grid_tile_width // 4 # Used for the width of the agent drawing
    quarter_tile_height = grid_tile_height // 4 # Used for the height of the agent drawing

    return screen, clock, grid_tile_width, grid_tile_height

##
# Draw the agent as a rectangle in the correct grid tile
def draw_agent(screen, current_agent_env_state):
    # NOTE: I reversed tracking the row and column position in the overall system by accident.  Draw grid has been mostly rectified, but I don't really want
    #       to mess with the agent's tracking.  So tile_coordinates[0][current_agent_env_state[1]] is the agent's column position and the other is the row position.
    #       Drawing from left then top is how Pygame tracks this.
    agent_rect = pygame.Rect(tile_coordinates[0][current_agent_env_state[1]], tile_coordinates[1][current_agent_env_state[0]], quarter_tile_width * 2, quarter_tile_height * 2)
    pygame.draw.rect(screen, (245, 0, 0), agent_rect, 50)

def draw_reward(screen, reward_row, reward_col):
    reward_rect = pygame.Rect(tile_coordinates[0][reward_col], tile_coordinates[1][reward_row], quarter_tile_width * 2, quarter_tile_height * 2)
    pygame.draw.rect(screen, (0, 245, 0), reward_rect, 50)

##
# Draw the grid that the agent will traverse.  Track the start coordinates of each tile for the purpose of drawing the rewards and agent.
def draw_grid(screen, width, height, win_size):
    # NOTE: I messed up the tracking of columns and rows by using the window width for rows and height for columns.
    #       This should have been made in reverse, but the agent already tracks it that way and I don't want to try and reverse it right now.
    #       The actual method is shown below in the for loops.  The tile_coordinates list has things in reverse, so it array 0 is the columns and 1 is the rows.
    if len(tile_coordinates) == 0: # Track the tile coordinates for agent and reward drawing
        tile_coordinates.append(list())
        tile_coordinates.append(list())
        for col in range(0, win_size[0], int(width)):
            if col not in tile_coordinates[0]:
                tile_coordinates[0].append(col)
            for row in range(0, win_size[1], int(height)):
                if row not in tile_coordinates[1]:
                    tile_coordinates[1].append(row)
                rect = pygame.Rect(col, row, width, height)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
    else:
        for col in range(0, win_size[0], int(width)):
            for row in range(0, win_size[1], int(height)):
                rect = pygame.Rect(col, row, width, height)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
