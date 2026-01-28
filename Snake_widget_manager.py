import Snake
import pygame
from Button_default import Button_default
from Button_default import Input_text
from Button_default import Check_box
import sys
from Snake_database_handler import Snake_database_handler
import Base_game_modes
from Snake_data import Game_data as Data

class Snake_widget_manager:
	def __init__(self):
		self.database = Snake_database_handler()

		self.game_size = Data.grid_cell_size
		self.current_screen = Data().create_window()
		self.clock = pygame.time.Clock()
		self.main_menu()

	def main_menu(self):
		self.current_screen.fill((255,100,100))

		text_snake_game = Data.generate_text("Snake game", color=(0,0,0))
		self.current_screen.blit(text_snake_game, (Button_default.center_div(text_snake_game.get_width()), Data.main_menu_top_margin))

		start_buton = Button_default(self.current_screen, (Button_default.center_div(), text_snake_game.get_abs_offset()[1] + text_snake_game.get_height() + Data.minimum_top_margin + int(0.1 * Data.window_resolution[1])), "Start game")
		setting_button = Button_default(self.current_screen, (Button_default.center_div(), start_buton.button_position[1] + Data.minimum_top_margin), "Settings")
		exit_button = Button_default(self.current_screen, (Button_default.center_div(), setting_button.button_position[1] + Data.minimum_top_margin), "Exit game")

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
		self.current_screen.fill(Data.select_background_color)

		text_select_game_mode = Data.generate_text("Select a Game Mode")
		
		self.current_screen.blit(text_select_game_mode, (Button_default.center_div(text_select_game_mode.get_width()), Data.select_top_margin))

		adventure_mode = Button_default(self.current_screen, (int(Button_default.center_div() * 0.1),  text_select_game_mode.get_abs_offset()[1] + Data.minimum_top_margin + int(0.1 * Data.window_resolution[1])), "Adventure Mode", button_width=int(Button_default.DEFAULT_BUTTON_WIDTH * 0.75))
		bare_bone_mode = Button_default(self.current_screen, (int(Button_default.center_div() * 0.1), adventure_mode.button_position[1] + Data.minimum_top_margin), "Bare Bone Mode", button_width=int(Button_default.DEFAULT_BUTTON_WIDTH * 0.75))
		bomb_mode = Button_default(self.current_screen, (int(Button_default.center_div() * 1.5), adventure_mode.button_position[1] + Data.minimum_top_margin), "Bomb Mode", button_width=int(Button_default.DEFAULT_BUTTON_WIDTH * 0.75))
		# vs_mode = Button_default(self.current_screen, (int(Button_default.center_div() * 0.1), bomb_mode.button_position[1] + Data.minimum_top_margin), "Versus Ai Mode", button_width=int(Button_default.DEFAULT_BUTTON_WIDTH * 0.75))

		black_out_mode = Button_default(self.current_screen, (int(Button_default.center_div() * 1.5),  text_select_game_mode.get_abs_offset()[1] + Data.minimum_top_margin + int(0.1 * Data.window_resolution[1])), "Black Out Mode", button_width=int(Button_default.DEFAULT_BUTTON_WIDTH * 0.75))
		# button_mode = Button_default(self.current_screen, (int(Button_default.center_div() * 1.5), adventure_mode.button_position[1] + Data.minimum_top_margin), "Buttons Mode", button_width=int(Button_default.DEFAULT_BUTTON_WIDTH * 0.75))
		# not_definded = Button_default(self.current_screen, (int(Button_default.center_div() * 1.5), bare_bone_mode.button_position[1] + Data.minimum_top_margin), "None", button_width=int(Button_default.DEFAULT_BUTTON_WIDTH * 0.75))
		# multiplayer_mode = Button_default(self.current_screen, (int(Button_default.center_div() * 1.5), bomb_mode.button_position[1] + Data.minimum_top_margin), "Multiplayer", button_width=int(Button_default.DEFAULT_BUTTON_WIDTH * 0.75))

		buttons = [adventure_mode, bare_bone_mode, bomb_mode, black_out_mode]
		for button in buttons:
			if self.database.is_score_exist(button.get_Text()):
				score_value = str(self.database.get_best_game_score(button.get_Text()))
			else:
				score_value = "-"
			score_text = Data.generate_text(str("Best Score: " + score_value), font_size=int(Data.text_size * 0.75))
			self.current_screen.blit(score_text, (button.button_position[0] + button.button_width + Data.select_score_left_margin, button.button_position[1]))
		
		return_button = Button_default(self.current_screen, (Button_default.center_div(), int(Data.window_resolution[1] * 0.85)), "Return")
		buttons.append(return_button)

		pygame.display.flip()

		while True:
			for button in buttons:
				button.render_button()
			self.clock.tick(60)
			events = pygame.event.poll()
			if events.type == pygame.MOUSEBUTTONUP:
				if adventure_mode.is_mouse_on_button():
					self.run_snake(Base_game_modes.Adventure_mode(self.current_screen, self.game_size))
				elif bare_bone_mode.is_mouse_on_button():
					self.run_snake(Base_game_modes.Bare_bone_mode_game(self.current_screen, self.game_size))
				elif bomb_mode.is_mouse_on_button():
					self.run_snake(Base_game_modes.Bomb_mode_game(self.current_screen, self.game_size))
				elif return_button.is_mouse_on_button():
					self.main_menu()
				# elif vs_mode.is_mouse_on_button():
				# 	self.run_snake(Base_game_modes.Versus_ai_mode(self.current_screen, self.game_size))
				elif black_out_mode.is_mouse_on_button():
					self.run_snake(Base_game_modes.Black_out_mode(self.current_screen, self.game_size))
			pygame.display.flip()

	def run_snake(self, game):
		snake = Snake.Snake(self.game_size, self.current_screen)
		game = game.clone()
		game.init_snake_in_game(snake)
		game.start_game(Data.gameplay_background_color)

		self.death_screen(snake.score, game)

	def settings(self):
		self.current_screen.fill((41,189,193))

		text_input_text = Data.generate_text("Text input tester", color=(0,0,0))
		input_text = Input_text(self.current_screen, (int(Data.window_resolution[0] * 0.03), int(Data.window_resolution[1] * 0.15)))
		accept_button = Button_default(self.current_screen, (input_text.button_width + int(Data.window_resolution[0] * 0.02) + input_text.button_position[0] , int(Data.window_resolution[1] * 0.15)), "Accept tekst")
		text = Data.generate_text("")

		gridButton = Check_box(self.current_screen, (int(Data.window_resolution[0] * 0.125), int(Data.window_resolution[1] * 0.45) ), Data.show_grid, "grid")

		resolution_text = Data.generate_text("Resolution:", color=(0,0,0))
		resolution1 = Button_default(self.current_screen, (int(Data.window_resolution[0] * 0.03), int(Data.window_resolution[1] * 0.70)), "1600x900")
		resolution2 = Button_default(self.current_screen, (resolution1.button_position[0] + resolution1.button_width + int(Data.window_resolution[0] * 0.02), int(Data.window_resolution[1] * 0.70)), "1920x1080")
		resolution3 = Button_default(self.current_screen, (resolution2.button_position[0] + resolution2.button_width + int(Data.window_resolution[0] * 0.02), int(Data.window_resolution[1] * 0.70)), "2560x1440")

		go_back_button = Button_default(self.current_screen, (int(Button_default.center_div()), int(Data.window_resolution[1] * 0.85)), "Back")

		is_running = True
		while is_running:
			self.clock.tick(60)
			go_back_button.render_button()
			gridButton.render_check_box()
			accept_button.render_button()
			input_text.render_button()
			resolution1.render_button()
			resolution2.render_button()
			resolution3.render_button()
			user_input = pygame.event.poll()
			if user_input.type == pygame.MOUSEBUTTONUP:
				input_text.on_click()
				if go_back_button.is_mouse_on_button():
					self.main_menu()
				elif accept_button.is_mouse_on_button():
					text = Data.generate_text(input_text.text, color=(200,0,0))
				elif resolution1.is_mouse_on_button():
					self.database.change_settings("resolution", "1600x900")
				elif resolution2.is_mouse_on_button():
					self.database.change_settings("resolution", "1920x1080")
				elif resolution3.is_mouse_on_button():
					self.database.change_settings("resolution", "2560x1440")
				elif gridButton.is_mouse_on_check_box():
					gridButton.on_click()
					Data.show_grid = not Data.show_grid
					self.database.change_settings("grid", Data.show_grid)

			self.current_screen.blit(text_input_text, (int(Data.window_resolution[0] * 0.03), int(Data.window_resolution[1] * 0.05)))	
			self.current_screen.blit(text, (int(Data.window_resolution[0] * 0.03), int(Data.window_resolution[1] * 0.30)))
			self.current_screen.blit(resolution_text, (int(Data.window_resolution[0] * 0.03), int(Data.window_resolution[1] * 0.60)))
			input_text.get_user_input(user_input)
			pygame.display.flip()

	def death_screen(self, score, game_mode):
		pygame.event.clear()
		is_running = True

		self.database.insert_game_score(game_mode.get_game_mode_name(), score)

		self.current_screen.fill((255,100,100))

		death_text = Data.generate_text("You Died!!!", color=(0,0,0))
		self.current_screen.blit(death_text, (Button_default.center_div(death_text.get_width()), Data.death_top_margin))

		current_score_text = Data.generate_text("Your Score: " + str(score), color=(0,0,0))
		self.current_screen.blit(current_score_text, (Button_default.center_div(current_score_text.get_width()), death_text.get_abs_offset()[1] + Data.minimum_top_margin))

		best_score_text = Data.generate_text("Your best score: " + str(self.database.get_best_game_score(game_mode.get_game_mode_name())), color=(0,0,0))
		self.current_screen.blit(best_score_text, (Button_default.center_div(best_score_text.get_width()), current_score_text.get_abs_offset()[1] + Data.minimum_top_margin + current_score_text.get_height()))

		retry_button = Button_default(self.current_screen, (Button_default.center_div(), best_score_text.get_abs_offset()[1] + Data.minimum_top_margin + best_score_text.get_height() + int(0.1 * Data.window_resolution[1])), text="Retry")
		menu_button = Button_default(self.current_screen, (Button_default.center_div(), retry_button.button_position[1] + Data.minimum_top_margin), text="Main menu")
		exit_button = Button_default(self.current_screen, (Button_default.center_div(), menu_button.button_position[1] + Data.minimum_top_margin), text="Exit")

		while is_running:
			retry_button.render_button()
			menu_button.render_button()
			exit_button.render_button()

			self.clock.tick(60)
			events = pygame.event.poll()
			if events.type == pygame.MOUSEBUTTONUP:
				if retry_button.is_mouse_on_button():
					self.run_snake(game_mode)
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
