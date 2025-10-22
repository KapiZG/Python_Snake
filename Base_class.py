import pygame
from random import randint

class Base_game:
	def __init__(self, screen, game_size):
		self.screen = screen
		self.screen_border = screen.get_size()
		self.game_size = game_size
		self.active_objects = []

	def get_free_position(self):
		is_that_position_free = False
		while not is_that_position_free:
			random_position = self.get_random_position()
			is_that_position_free = True
			for prop in self.active_objects:
				if prop.is_overlaping(random_position):
					is_that_position_free = False
					break
		return random_position

	def get_random_position(self):
		x = randint(0, int(self.screen_border[0] / self.game_size - 4)) * self.game_size + self.game_size
		y = randint(0, int(self.screen_border[1] / self.game_size - 4)) * self.game_size + self.game_size
		return x, y

	def check_if_colision_happen(self, player):
		for element in self.active_objects:
			element.if_touched_by_player(player, self.get_free_position())

	def render_things(self):
		for element in self.active_objects:
			element.render(self.screen)


class Object_snake:
	def __init__(self, position, game_size, color = (255,255,255)):
		self.position = position
		self.size = game_size
		self.color = color

	def get_object_position(self):
		return self.position

	def is_overlaping(self, coordinates):
		return self.position == coordinates

	def render(self, screen):
		pygame.draw.rect(screen, self.color, [self.position[0], self.position[1], self.size, self.size])

	def set_new_position(self, new_position):
		self.position = new_position

	def if_touched_by_player(self, player, function, new_position):
		if self.is_overlaping(player.get_snake_x_and_y()):
			function(player, new_position)


class Bomb(Object_snake):
	def __init__(self, position, game_size):
		super().__init__(position, game_size, (0,0,0))

	def if_touched_by_player(self, player, new_position):
		super().if_touched_by_player(player, self.on_touch, new_position)

	def on_touch(self, player, _):
		player.is_snake_death = True

class Apple(Object_snake):
	def __init__(self, position, game_size):
		super().__init__(position, game_size, (255,0,0))

	def if_touched_by_player(self, player, new_position):
		super().if_touched_by_player(player, self.on_touch, new_position)

	def on_touch(self, player, new_position):
		player.score += 1
		player.grow_the_snake()
		self.set_new_position(new_position)

