# AUTHOR: JAG
# DATE: [2024]
# DESCRIPTION: Environment specific utilities to decrease complexity of controller and agent classes.

import pygame
import numpy as np

tile_coordinates = list()

def init_pygame_world(win_size, environment):
    screen = pygame.display.set_mode(win_size)
    clock = pygame.time.Clock()

    # Initialize other environment settings.
    grid_tile_width = win_size[0] / len(environment[0]) # Width of a grid tile in pixels. Used for columns.
    grid_tile_height = win_size[1] / len(environment) # Height of a grid tile in pixels Used for rows

    return screen, clock, grid_tile_width, grid_tile_height

def draw_agent(screen, tile_width, tile_height, current_agent_env_state):
    # Draw the agent as a circle in the correct box
    quarter_tile_width =  tile_width // 4
    quarter_tile_height =  tile_height // 4
    agent_rect = pygame.Rect(tile_coordinates[0][current_agent_env_state[1]], tile_coordinates[1][current_agent_env_state[0]], quarter_tile_width * 2, quarter_tile_height * 2)
    pygame.draw.rect(screen, (245, 0, 0), agent_rect, 50)

def draw_grid(screen, width, height, win_size):
    # NOTE: I messed up the tracking of columns and rows by using the window width for rows and height for columns.
    #       This should have been made in reverse, but the agent already tracks it that way and I don't want to try and reverse it right now.
    #       The actual method is shown below in the for loops.  The tile_coordinates list has things in reverse, so it array 0 is the columns and 1 is the rows.
    if len(tile_coordinates) == 0:
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
