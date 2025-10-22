import Base_class

class Bare_bone_mode_game(Base_class.Base_game):
    def __init__(self, screen, game_size):
        super().__init__(screen, game_size)
        self.game_mode_name = "bare bone mode"

    def start_game(self, background_color):
        super().start_game(lambda: None, background_color)

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

        