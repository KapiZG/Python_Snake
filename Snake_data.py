import pygame

class Game_data:

    # store how many cells are on x axis
    grid_size = 25

    window_resolution = (1600, 900)

    #size of one cell
    grid_cell_size = int(window_resolution[0] / grid_size)

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

    def __init__(self):
        pass

    def create_window(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        return pygame.display.set_mode(self.window_resolution)
    
    @staticmethod
    def generate_text(text, font_size = text_size, color = (255,255,255)):
        return pygame.font.Font(pygame.font.get_default_font(), font_size).render(text, True, color)