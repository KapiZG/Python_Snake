import pygame 
import random
import copy
import numpy

game_size = 40
pygame.init()
screen = pygame.display.set_mode((game_size * 20, game_size * 15))
clock = pygame.time.Clock()
running = True
position_x = 10
position_y = 10
last_time_pressed = ""
size = 1
score = 0
screen_border = screen.get_size()

class Snake:
	def __init__(self, screen_border, game_size):
		self.game_size = game_size
		self.body = numpy.array([[self.game_size,self.game_size,self.game_size,self.game_size]])
		self.screen_border = screen_border
		

	def movement(self, screen, current_direction):
		for i in range(len(self.body) - 1):
			self.body[len(self.body) - 1 - i] = self.body[len(self.body) - 2 - i]
			print("test2", self.body)
			pygame.draw.rect(screen, (255,255,255), self.body[i - 1], 2)
		if current_direction == "d":		
			self.body[0][0] += self.game_size
		elif current_direction == "s":
			self.body[0][1] += self.game_size
		elif current_direction == "a":
			self.body[0][0] -= self.game_size
		elif current_direction == "w":
			self.body[0][1] -= self.game_size
		pygame.draw.rect(screen, (255,0,0), self.body[0], 2)

	
	def is_death(self):
		if self.body[0][0] >= self.screen_border[0] or self.body[0][1] >= self.screen_border[1] or self.body[0][0] < 0 or self.body[0][1] < 0:
			return True
		if len(numpy.unique(self.body)) < len(self.body):
			print("Death", self.body)
			return True
		
	def get_snake_x_and_y(self):
		return (self.body[0][0], self.body[0][1])
	
	def grow_the_snake(self, current_direction):
		self.body = numpy.append(self.body, [self.body[len(self.body) - 1]], 0)
		if current_direction == "d":		
			self.body[len(self.body) - 2][0] += self.game_size
		elif current_direction == "s":
			self.body[len(self.body) - 2][1] += self.game_size
		elif current_direction == "a":
			self.body[len(self.body) - 2][0] -= self.game_size
		elif current_direction == "w":
			self.body[len(self.body) - 2][1] -= self.game_size
		


def spawn_apple():
	x = random.randint(0, screen_border[0] / game_size - 4)
	x = x * game_size + game_size
	y = random.randint(0, screen_border[1] / game_size - 4)
	y = y * game_size + game_size
	return x,y



screen.fill((0,255,0))	
apple_x, apple_y = spawn_apple()
pygame.draw.rect(screen, (0,0,0), [apple_x,apple_y, game_size, game_size])
pygame.display.flip()
snake = Snake(screen_border, game_size)
while running:
	if snake.is_death():
		del snake
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				last_time_pressed = "a"
			elif event.key == pygame.K_d:
				last_time_pressed = "d"
			elif event.key == pygame.K_s:
				last_time_pressed = "s"
			elif event.key == pygame.K_w:
				last_time_pressed = "w"
			elif event.key == pygame.K_k:
				snake.death(screen)

	screen.fill((72,144,50))	
	# print(snake.get_snake_x_and_y(), " ", (apple_x, apple_y))

	snake.movement(screen, last_time_pressed)
	pygame.time.wait(150)
	if snake.get_snake_x_and_y() == (apple_x, apple_y):
		apple_x, apple_y = spawn_apple()
		snake.grow_the_snake(last_time_pressed)

	pygame.draw.rect(screen, (0,0,0), [apple_x, apple_y, game_size, game_size])

	pygame.display.flip()
	clock.tick(60)

pygame.quit()


