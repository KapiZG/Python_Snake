import pygame 
import random
import numpy

class Snake:
	def __init__(self, game_size, screen):
		self.screen = screen
		self.screen_border = screen.get_size()
		self.game_size = game_size
		self.body = numpy.array([[self.game_size,self.game_size,self.game_size,self.game_size]])
		self.score = 0
		self.button_pressed = ""
		self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
		self.spawn_apple()
		self.render_thinks()
		
	def change_direction(self, key):
		if key.type == pygame.KEYDOWN:
			if key.key == pygame.K_a:
				self.button_pressed = "a"
			elif key.key == pygame.K_d:
				self.button_pressed = "d"
			elif key.key == pygame.K_s:
				self.button_pressed = "s"
			elif key.key == pygame.K_w:
				self.button_pressed = "w"

	def movement(self):
		for i in range(len(self.body) - 1):
			self.body[len(self.body) - 1 - i] = numpy.copy(self.body[len(self.body) - 2 - i])
			pygame.draw.rect(self.screen, (255,255,255), self.body[len(self.body) - i - 1], 2)
		if self.button_pressed == "d":		
			self.body[0][0] += self.game_size
		elif self.button_pressed == "s":
			self.body[0][1] += self.game_size
		elif self.button_pressed == "a":
			self.body[0][0] -= self.game_size
		elif self.button_pressed == "w":
			self.body[0][1] -= self.game_size
		pygame.draw.rect(self.screen, (255,0,0), self.body[0], 2)

	
	def is_death(self):
		if self.body[0][0] >= self.screen_border[0] or self.body[0][1] >= self.screen_border[1] or self.body[0][0] < 0 or self.body[0][1] < 0:
			return True
		for i in range(len(self.body) - 1):
			if (self.body[0] == self.body[len(self.body) - 1 - i]).all():
				return True
		
	def get_snake_x_and_y(self):
		return (self.body[0][0], self.body[0][1])
	
	def grow_the_snake(self):
		self.score += 1
		self.body = numpy.append(self.body, [self.body[len(self.body) - 1]], 0)
		if self.button_pressed == "d":		
			self.body[len(self.body) - 2][0] += self.game_size
		elif self.button_pressed == "s":
			self.body[len(self.body) - 2][1] += self.game_size
		elif self.button_pressed == "a":
			self.body[len(self.body) - 2][0] -= self.game_size
		elif self.button_pressed == "w":
			self.body[len(self.body) - 2][1] -= self.game_size
		
	def spawn_apple(self):
		self.apple_x = random.randint(0, self.screen_border[0] / self.game_size - 4) * self.game_size + self.game_size
		self.apple_y = random.randint(0, self.screen_border[1] / self.game_size - 4) * self.game_size + self.game_size

	def render_thinks(self):
		self.screen.fill((72,144,50))
		self.movement()
		self.render_score()
		pygame.draw.rect(self.screen, (255,0,0), [self.apple_x, self.apple_y, self.game_size, self.game_size])
		pygame.display.flip()

	def render_score(self):
		text = self.font.render("Score: " + str(self.score), True, (255,0,0))
		text_position = text.get_rect().center = (pygame.display.get_window_size()[0] - (pygame.surface.Surface.get_size(text)[0] + 17), pygame.surface.Surface.get_size(text)[1])
		self.screen.blit(text, text_position)
