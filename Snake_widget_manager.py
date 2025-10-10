import Snake
import pygame

class Snake_widget_manager:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.game_size = 40
        self.current_screen = pygame.display.set_mode((self.game_size * 25, self.game_size * 15))
        self.default_font = pygame.font.Font(pygame.font.get_default_font(), self.game_size)

    def run_snake(self):
        self.snake = Snake.Snake(self.game_size, self.current_screen)
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.snake.change_direction(event)

            pygame.time.wait(150)
            if self.snake.get_snake_x_and_y() == (self.snake.apple_x, self.snake.apple_y):
                self.snake.grow_the_snake()
                self.snake.spawn_apple()
                self.snake.render_thinks()
            else:
                self.snake.render_thinks()

            if self.snake.is_death():
                self.is_running = False
            self.clock.tick(60)

        self.death_screen()

    def death_screen(self):
        pygame.quit()

test = Snake_widget_manager()
test.run_snake()