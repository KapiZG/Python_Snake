import Snake
import pygame
import Button_default
import sys
import sqlite3

class Snake_widget_manager:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.db = sqlite3.connect("Snake.db")
        self.db_cursor = self.db.cursor()

        self.db_cursor.execute("Select name from sqlite_master where type='table' and name='score'")
        if self.db_cursor.fetchone() == None:
            self.db_cursor.execute("CREATE TABLE score(user_name, value)")

        self.game_size = 40
        self.background_color = (72,144,50)
        self.current_screen = pygame.display.set_mode((self.game_size * 25, self.game_size * 15))
        self.default_font = pygame.font.Font(pygame.font.get_default_font(), self.game_size)
        self.main_menu()

    def main_menu(self):
        self.current_screen.fill((255,100,100))
        self.current_screen.blit(self.default_font.render("Snake game", True, (0,0,0)),(400, 100))

        start_buton = Button_default.Button_default(self.current_screen, (400, 200), "Start game")
        setting_button = Button_default.Button_default(self.current_screen, (400, 300), "Settings")
        exit_button = Button_default.Button_default(self.current_screen, (400, 400), "Exit game")

        is_running = True
        while is_running:
            start_buton.render_button()
            setting_button.render_button()
            exit_button.render_button()
            self.clock.tick(60)
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:
                if start_buton.is_mouse_on_button():
                    self.run_snake()
                elif setting_button.is_mouse_on_button():
                    self.settings()
                elif exit_button.is_mouse_on_button():
                    self.exit_game()
            pygame.display.flip()
    
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
                snake.spawn_bomb()
                snake.render_thinks()
            else:
                snake.spawn_bomb()
                snake.render_thinks()

            if snake.is_death():
                is_running = False
            self.clock.tick(60)

            pygame.display.flip()

        self.death_screen(snake.score)

    def settings(self):
        self.current_screen.fill((255,0,0))
        go_back_button = Button_default.Button_default(self.current_screen, (400, 500), "Back")
        is_running = True
        while is_running:
            self.clock.tick(60)
            go_back_button.render_button()
            if pygame.event.poll().type == pygame.MOUSEBUTTONUP:
                if go_back_button.is_mouse_on_button():
                    self.main_menu()
            pygame.display.flip()

    def death_screen(self, score):
        pygame.event.clear()
        is_running = True

        self.db_cursor.execute("INSERT INTO score VALUES ('qweqwe', ?)", (score,))
        self.db.commit()


        self.current_screen.fill((255,100,100))
        self.current_screen.blit(self.default_font.render("You Died!!!", True, (0,0,0)), (400, 50))
        self.current_screen.blit(self.default_font.render("Your Score: " + str(score), True, (0,0,0)), (400, 100))

        self.db_cursor.execute("SELECT value FROM score ORDER BY value DESC")
        best_score = self.db_cursor.fetchone()
        self.current_screen.blit(self.default_font.render("Your best score: " + str(best_score[0]), True, (0,0,0)), (400, 150))

        retry_button = Button_default.Button_default(self.current_screen, (400,250), text="Retry")
        menu_button = Button_default.Button_default(self.current_screen, (400,350), text="Main menu")
        exit_button = Button_default.Button_default(self.current_screen, (400,450), text="Exit")

        while is_running:
            retry_button.render_button()
            menu_button.render_button()
            exit_button.render_button()

            self.clock.tick(60)
            events = pygame.event.poll()
            if events.type == pygame.MOUSEBUTTONUP:
                if retry_button.is_mouse_on_button():
                    self.run_snake()
                elif exit_button.is_mouse_on_button():
                    is_running = False
                elif menu_button.is_mouse_on_button():
                    self.main_menu()
            pygame.display.flip()
        self.exit_game()

    def exit_game(self):  
        self.db.close()
        pygame.quit()
        sys.exit()

test = Snake_widget_manager()
