import Base_class
import Snake
import pygame
from Snake_data import Game_data as Data

class Bare_bone_mode_game(Base_class.Base_game):
    def __init__(self, screen, game_size):
        super().__init__(screen, game_size)
        self.game_mode_name = "bare bone mode"

    def start_game(self, background_color):
        super().start_game(lambda: None, background_color)
    
    def clone(self):
        return Bare_bone_mode_game(self.screen, self.game_size)

class Bomb_mode_game(Base_class.Base_game):
    
    SCORE_BETWEEN_BOMBS = 1

    def __init__(self, screen, game_size, score_between_bombs = SCORE_BETWEEN_BOMBS):
        super().__init__(screen, game_size)
        self.game_mode_name = "bomb mode"
        self.bombs = []
        self.score_required_to_spawn_bomb = score_between_bombs

    def start_game(self, background_color):
        super().start_game(self.middle_game, background_color)

    def middle_game(self, score_between_bombs = SCORE_BETWEEN_BOMBS):
        if self.score_required_to_spawn_bomb == self.player.score:
            self.active_objects.append(Base_class.Bomb(self.get_free_position(), self.game_size))
            self.score_required_to_spawn_bomb += score_between_bombs
        
    def clone(self):
        return Bomb_mode_game(self.screen, self.game_size)

class Versus_ai_mode(Base_class.Base_game):
    def __init__(self, screen, game_size):
        super().__init__(screen, game_size)
        self.game_mode_name = "versus ai mode"
        self.enemy_snake = Snake.Snake_enemy(self.game_size, self.screen, 10, (10, 10))
        
    def start_game(self, background_color):
        super().start_game(self.middle_game, background_color)
        
    def middle_game(self):
        for element in self.enemy_snake.body:
            if (self.player.body[0][0], self.player.body[0][1]) == (element[0], element[1]):
                self.player.is_snake_death = True
        self.enemy_snake.change_direction()
        self.enemy_snake.render()
        
    def clone(self):
        return Versus_ai_mode(self.screen, self.game_size)
        
class Black_out_mode(Base_class.Base_game):
    def __init__(self, screen, game_size):
        super().__init__(screen, game_size)
        self.game_mode_name = "black out mode"
        self.timer_apple = 0
        
    def start_game(self, background_color):
        super().start_game(self.middle_game, background_color)

    def middle_game(self):
        player_head_position = self.player.get_snake_x_and_y()
        pygame.draw.rect(self.screen, (0,0,0), [0,0, Data.window_resolution[0], player_head_position[1] - 2 * self.game_size])
        pygame.draw.rect(self.screen, (0,0,0), [0, player_head_position[1] + 3 * self.game_size, Data.window_resolution[0] , Data.window_resolution[1]])
        pygame.draw.rect(self.screen, (0,0,0), [0,0, player_head_position[0] - 2 * self.game_size, Data.window_resolution[1]])
        pygame.draw.rect(self.screen, (0,0,0), [player_head_position[0] + 3 * self.game_size, 0, Data.window_resolution[0] , Data.window_resolution[1]])
        self.player.render_score()
        if self.timer_apple <= 5:
            self.apple.render(self.screen)
            self.timer_apple += 1
        if self.apple.is_overlaping(self.player.get_snake_x_and_y()):
            self.timer_apple = 0

    def clone(self):
        return Black_out_mode(self.screen, self.game_size)