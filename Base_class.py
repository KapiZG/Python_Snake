import pygame
from random import randint

class Base_game:
	def __init__(self, screen, game_size):
		self.screen = screen
		self.screen_border = screen.get_size()
		self.game_size = game_size
		self.active_objects = []
		self.player = None
		# Needs to be definded in subclasses 
		self.game_mode_name = None

	def init_snake_in_game(self, snake):
		self.player = snake

	def get_free_position(self):
		is_that_position_free = False
		while not is_that_position_free:
			random_position = self.get_random_position()
			is_that_position_free = self.check_is_free(random_position)
		return random_position

	def check_is_free(self, random_position):
		for prop in self.active_objects:
			if prop.is_overlaping(random_position):
				return False
		for body_part in self.player.body:
			if (body_part[0], body_part[1]) == random_position:
				return False
		return True

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

	def start_game(self, custom_game_mechanic, background_color):
		self.add_object_to_game(Apple(self.get_free_position(), self.game_size))
		while not self.player.is_snake_death:
			self.screen.fill(background_color)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				self.player.change_direction(event)

			pygame.time.wait(150)

			self.check_if_colision_happen(self.player)
			self.render_things()
			custom_game_mechanic()

			self.player.render_thinks()
			self.player.did_i_touch_myself_or_border()

			pygame.time.Clock().tick(60)

			pygame.display.flip()
		return 1

	def add_object_to_game(self, object):
		self.active_objects.append(object)

	def middle_game(self):
		pass

	def get_game_mode_name(self):
		return self.game_mode_name

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

