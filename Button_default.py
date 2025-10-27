import pygame
from Snake_data import Game_data as Data

class Button_default:
    DEFAULT_BUTTON_WIDTH = int(0.3 * Data.window_resolution[0])
    # DEFAULT_BUTTON_HEIGHT = int(0.1 * Data.window_resolution[1])
    DEFAULT_BUTTON_COLOR = (255, 255, 255)
    # DEFAULT_TEXT_SIZE = int(0.5 * DEFAULT_BUTTON_HEIGHT)
    DEFAULT_TEXT_COLOR = (0,0,0)

    def __init__(self, screen, button_position, text = "", text_color = DEFAULT_TEXT_COLOR, button_color = DEFAULT_BUTTON_COLOR, button_width = DEFAULT_BUTTON_WIDTH):
        self.screen = screen
        self.text_color = text_color
        self.button_position = button_position
        self.button_color = button_color
        self.button_width = button_width
        self.button_height = int(self.button_width * 0.2)
        self.text = text

        self.font = pygame.font.Font(pygame.font.get_default_font(), int(0.5 * self.button_height))

        self.position_text_on_button()

    def render_button(self):
        if self.is_mouse_on_button():
            pygame.draw.rect(self.screen, tuple(int(color/2) for color in self.button_color), [self.button_position[0], self.button_position[1], self.button_width, self.button_height])
        else:
            pygame.draw.rect(self.screen, self.button_color, [self.button_position[0], self.button_position[1], self.button_width, self.button_height])
        self.screen.blit(self.font.render(self.text, True, self.text_color), self.text_position)
    
    def position_text_on_button(self):
        text_x = self.button_position[0] + int((self.button_width / 2)) - int((self.font.size(self.text)[0] / 2))
        text_y = self.button_position[1] + int((self.button_height / 2)) - int((self.font.size(self.text)[1] / 2))
        self.text_position = (text_x, text_y)

    def is_mouse_on_button(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if mouse_x >= self.button_position[0] and mouse_x <= self.button_position[0] + self.button_width  and mouse_y >= self.button_position[1] and mouse_y <= self.button_position[1] + self.button_height:
            return True
        else:
            return False
    
    def get_Text(self):
        return self.text.lower()

    @staticmethod
    def center_div(object_width = DEFAULT_BUTTON_WIDTH):
        return int((Data.window_resolution[0] * 0.5) - (object_width * 0.5))
    
class Input_text:
    def __init__(self, screen, button_position, text = "", button_width = Button_default.DEFAULT_BUTTON_WIDTH):
        self.is_active = False
        self.screen = screen
        self.text_color = (0,0,0)
        self.button_position = button_position
        self.button_color = (255,255,255)
        self.button_width = button_width
        self.button_height = int(self.button_width * 0.2)
        self.text = ""

        self.font = pygame.font.Font(pygame.font.get_default_font(), int(0.5 * self.button_height))

        self.position_text_on_button()

    def render_button(self):
        if self.is_mouse_on_button():
            pygame.draw.rect(self.screen, tuple(int(color/2) for color in self.button_color), [self.button_position[0], self.button_position[1], self.button_width, self.button_height])
        else:
            pygame.draw.rect(self.screen, self.button_color, [self.button_position[0], self.button_position[1], self.button_width, self.button_height])
        self.screen.blit(self.font.render(self.text, True, self.text_color), self.text_position)

    def position_text_on_button(self):
        text_x = self.button_position[0] + int((self.button_width * 0.01))
        text_y = self.button_position[1] + int((self.button_height / 2)) - int((self.font.size(self.text)[1] / 2))
        self.text_position = (text_x, text_y)

    def is_mouse_on_button(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        if mouse_x >= self.button_position[0] and mouse_x <= self.button_position[0] + self.button_width  and mouse_y >= self.button_position[1] and mouse_y <= self.button_position[1] + self.button_height:
            return True
        else:
            return False

    def on_click(self):
        if self.is_mouse_on_button() and not self.is_active:
            self.is_active = True
            self.text += "|"
        elif self.is_active:
            self.is_active = False
            self.text = self.text[:-1]

    def get_user_input(self, input):
        if self.is_active and input.type == pygame.KEYUP:
            if input.key == pygame.K_BACKSPACE:
                self.text = self.text[:-2] + "|"
            else:
                self.text = self.text[:-1] + pygame.key.name(input.key) + "|"
