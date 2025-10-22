import sqlite3
import pygame

class Snake_database_handler:
	def __init__(self):
		self.db = sqlite3.connect("Snake.db")
		self.db_cursor = self.db.cursor()

		self.db_cursor.execute("Select name from sqlite_master where type='table' and name='score'")
		if self.db_cursor.fetchone() == None:
			self.db_cursor.execute("CREATE TABLE score(mode, value)")

	def insert_game_score(self, game_mode, score):
		self.db_cursor.execute("INSERT INTO score VALUES (?, ?)", (game_mode, score))
		self.db.commit()

	def get_best_game_score(self, game_mode):
		self.db_cursor.execute("SELECT value FROM score WHERE mode = ? ORDER BY value DESC", (game_mode,))
		return self.db_cursor.fetchone()[0]
	
	def is_score_exist(self, game_mode):
		self.db_cursor.execute("SELECT * FROM score WHERE mode = ?", (game_mode,))
		return not (self.db_cursor.fetchone() == None)

	def close_database(self):
		self.db.close()