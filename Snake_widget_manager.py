import Snake
import pygame
from Button_default import Button_default
import sys
from Snake_database_handler import Snake_database_handler
import Base_game_modes

class Snake_widget_manager:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Snake")
		self.clock = pygame.time.Clock()

		self.database = Snake_database_handler()

		self.game_size = 40
		self.background_color = (72,144,50)
		self.current_screen = pygame.display.set_mode((self.game_size * 25, self.game_size * 15))
		self.default_font = pygame.font.Font(pygame.font.get_default_font(), self.game_size)
		self.main_menu()

	def main_menu(self):
		self.current_screen.fill((255,100,100))
		self.current_screen.blit(self.default_font.render("Snake game", True, (0,0,0)),(400, 100))

		start_buton = Button_default(self.current_screen, (400, 200), "Start game")
		setting_button = Button_default(self.current_screen, (400, 300), "Settings")
		exit_button = Button_default(self.current_screen, (400, 400), "Exit game")

		is_running = True
		while is_running:
			start_buton.render_button()
			setting_button.render_button()
			exit_button.render_button()
			self.clock.tick(60)
			if pygame.event.poll().type == pygame.MOUSEBUTTONUP:
				if start_buton.is_mouse_on_button():
					self.select_game()
				elif setting_button.is_mouse_on_button():
					self.settings()
				elif exit_button.is_mouse_on_button():
					self.exit_game()
			pygame.display.flip()

	def select_game(self):
		self.current_screen.fill((62, 110, 56))

		self.current_screen.blit(self.default_font.render("Select a Game Mode", True, (255,255,255)), (300, 100))


		adventure_mode = Button_default(self.current_screen, (200, 200), "Adventure Mode")
		bare_bone_mode = Button_default(self.current_screen, (200, 300), "Bare Bone Mode")
		bomb_mode = Button_default(self.current_screen, (200, 400), "Bomb Mode")

		buttons = [adventure_mode, bare_bone_mode, bomb_mode]
		for button in buttons:
			if self.database.is_score_exist(button.get_Text()):
				score_value = str(self.database.get_best_game_score(button.get_Text()))
			else:
				score_value = "-"
			self.current_screen.blit(self.default_font.render("Best Score: " + score_value, True, (255,255,255)), (500, button.button_position[1]))
		
		return_button = Button_default(self.current_screen, (400, 500), "Return")
		buttons.append(return_button)

		pygame.display.flip()

		while True:
			for button in buttons:
				button.render_button()
			self.clock.tick(60)
			events = pygame.event.poll()
			if events.type == pygame.MOUSEBUTTONUP:
				if adventure_mode.is_mouse_on_button():
					pass
				elif bare_bone_mode.is_mouse_on_button():
					self.run_snake(Base_game_modes.Bare_bone_mode_game(self.current_screen, self.game_size))
				elif bomb_mode.is_mouse_on_button():
					self.run_snake(Base_game_modes.Bomb_mode_game(self.current_screen, self.game_size))
				elif return_button.is_mouse_on_button():
					self.main_menu()
			pygame.display.flip()

	def run_snake(self, game):
		snake = Snake.Snake(self.game_size, self.current_screen)

		game.init_snake_in_game(snake)
		game.start_game(self.background_color)

		self.death_screen(snake.score, game.get_game_mode_name())

	def settings(self):
		self.current_screen.fill((255,0,0))
		go_back_button = Button_default(self.current_screen, (400, 500), "Back")
		is_running = True
		while is_running:
			self.clock.tick(60)
			go_back_button.render_button()
			if pygame.event.poll().type == pygame.MOUSEBUTTONUP:
				if go_back_button.is_mouse_on_button():
					self.main_menu()
			pygame.display.flip()

	def death_screen(self, score, mode_name):
		pygame.event.clear()
		is_running = True

		self.database.insert_game_score(mode_name, score)

		self.current_screen.fill((255,100,100))
		self.current_screen.blit(self.default_font.render("You Died!!!", True, (0,0,0)), (400, 50))
		self.current_screen.blit(self.default_font.render("Your Score: " + str(score), True, (0,0,0)), (400, 100))

		self.current_screen.blit(self.default_font.render("Your best score: " + str(self.database.get_best_game_score(mode_name)), True, (0,0,0)), (400, 150))

		retry_button = Button_default(self.current_screen, (400,250), text="Retry")
		menu_button = Button_default(self.current_screen, (400,350), text="Main menu")
		exit_button = Button_default(self.current_screen, (400,450), text="Exit")

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
		self.database.close_database()
		pygame.quit()
		sys.exit()

test = Snake_widget_manager()
