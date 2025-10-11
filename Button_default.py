import pygame

class Button_default:
    DEFAULT_BUTTON_WIDTH = 200
    DEFAULT_BUTTON_HEIGHT = 40
    def __init__(self, screen, button_position: tuple[int, int], text = "", font_size = 20, text_color = (0,0,0), button_color = (255, 255, 255), button_width = DEFAULT_BUTTON_WIDTH, button_height = DEFAULT_BUTTON_HEIGHT):
        self.screen = screen
        self.text_color = text_color
        self.button_position = button_position
        self.button_color = button_color
        self.button_width = button_width
        self.button_height = button_height
        self.text = text

        self.font = pygame.font.Font(pygame.font.get_default_font(), font_size)

        self.position_text_on_button()



    def render_button(self):
        pygame.draw.rect(self.screen, self.button_color, [self.button_position[0], self.button_position[1], self.button_width, self.button_height])
        self.screen.blit(self.font.render(self.text, True, self.text_color), self.text_position)


    
    def position_text_on_button(self):
        text_x = self.button_position[0] + int((self.button_width / 2)) - int((self.font.size(self.text)[0] / 2))
        text_y = self.button_position[1] + int((self.button_height / 2)) - int((self.font.size(self.text)[1] / 2))
        self.text_position = (text_x, text_y)

    def is_click(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if mouse_x >= self.button_position[0] and mouse_x <= self.button_position[0] + self.button_width  and mouse_y >= self.button_position[1] and mouse_y <= self.button_position[1] + self.button_height:
            return True
        else:
            return False