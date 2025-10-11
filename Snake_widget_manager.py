import Snake
import pygame
import Button_default
import sys

class Snake_widget_manager:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.game_size = 40
        self.background_color = (72,144,50)
        self.current_screen = pygame.display.set_mode((self.game_size * 25, self.game_size * 15))
        self.default_font = pygame.font.Font(pygame.font.get_default_font(), self.game_size)
        self.main_menu()

    def main_menu(self):
        self.current_screen.fill((255,100,100))

        self.current_screen.blit(self.default_font.render("Snake game", True, (0,0,0)),(400, 100))

        start_buton = Button_default.Button_default(self.current_screen, (400, 200), "Start game")
        start_buton.render_button()

        setting_button = Button_default.Button_default(self.current_screen, (400, 300), "Settings")
        setting_button.render_button()

        exit_button = Button_default.Button_default(self.current_screen, (400, 400), "Exit game")
        exit_button.render_button()

        pygame.display.flip()
        is_running = True
        while is_running:
            self.clock.tick(60)
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:
                if start_buton.is_click():
                    self.run_snake()
                elif setting_button.is_click():
                    pass
                elif exit_button.is_click():
                    self.exit_game()
    
    def run_snake(self):
        snake = Snake.Snake(self.game_size, self.current_screen)
        is_running = True
        while is_running:
            self.current_screen.fill(self.background_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                snake.change_direction(event)

            pygame.time.wait(150)
            if snake.get_snake_x_and_y() == (snake.apple_x, snake.apple_y):
                snake.grow_the_snake()
                snake.spawn_apple()
                snake.render_thinks()
            else:
                snake.render_thinks()

            if snake.is_death():
                is_running = False
            self.clock.tick(60)

            pygame.display.flip()

        self.death_screen(snake.score)

    def death_screen(self, score):
        pygame.event.clear()
        is_running = True

        self.current_screen.fill((255,100,100))

        self.current_screen.blit(self.default_font.render("Your Score: " + str(score), True, (0,0,0)), (400, 100))

        retry_button = Button_default.Button_default(self.current_screen, (400,200), text="retry")
        retry_button.render_button()

        exit_button = Button_default.Button_default(self.current_screen, (400,300), text="exit")
        exit_button.render_button()
        pygame.display.flip()
        while is_running:
            self.clock.tick(60)
            events = pygame.event.poll()
            if events.type == pygame.MOUSEBUTTONUP:
                if retry_button.is_click():
                    self.run_snake()
                elif exit_button.is_click():
                    is_running = False
        self.exit_game()

    def exit_game(self):  
        pygame.quit()
        sys.exit()

test = Snake_widget_manager()
