import pygame
from Snake_database_handler import Snake_database_handler

class Game_data:

    window_resolution = [int(x) for x in Snake_database_handler().get_settings("resolution").split("x")]

    #gameplay grid data
    grid_size = 25
    grid_cell_size = int(window_resolution[0] / grid_size)
    grid_offset = (int((window_resolution[0] % grid_cell_size)/2), int((window_resolution[1] % grid_cell_size)/2))

    minimum_top_margin = int(0.15 * window_resolution[1])
    text_size = int(0.075 * window_resolution[1])

    # Main menu data
    main_menu_background_color = (72,144,50)
    main_menu_top_margin = int(0.2 * window_resolution[1])

    #Select game mode data
    select_background_color = (62, 110, 56)
    select_top_margin = int(0.075 * window_resolution[1])
    select_score_left_margin = int(0.01 * window_resolution[0])

    # gameplay data
    gameplay_background_color = (72,144,50)

    # death screen data
    death_top_margin = int(0.05 * window_resolution[1])

    # Setings data
    show_grid = bool(Snake_database_handler().get_settings("grid"))

    def __init__(self):
        pass

    def create_window(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        return pygame.display.set_mode(self.window_resolution)
    
    @staticmethod
    def generate_text(text, font_size = text_size, color = (255,255,255)):
        return pygame.font.Font(pygame.font.get_default_font(), font_size).render(text, True, color)