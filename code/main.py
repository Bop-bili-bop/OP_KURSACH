import sys
from menu import *
#components
from game import Game
from score import Score
from preview import Preview
from random import choice, randint

class Main:
	def __init__(self):

		# general
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Tetris')

		self.title_font = font_init(96)
		self.menu_font = font_init(36)
		self.ui = UIScreen(
			surface=None,  # не потрібно
			display_surface=self.display_surface,
			font=self.menu_font,
			big_font=None,  # не потрібно
			title_font=self.title_font,
			menu_font=self.menu_font,
			clock=self.clock,
			current_score=0
		)
		# show main menu and pick level
		self.level = self.ui.show_menu()  # 1, 2 або 3

		if self.level == 1:
			self.shapes_list = list(TETROMINOS.keys())
		elif self.level == 2:
			self.shapes_list = list(PENTOMINOS.keys())
		else:
			self.shapes_list = list(SHAPE.keys())

		#shapes
		self.next_shapes = [choice(self.shapes_list) for shape in range(3)]
		#components
		self.game = Game(self.get_next_shape, self.update_score)
		self.score = Score()
		self.preview = Preview()



	def update_score(self, lines, score, level):
		self.score.lines = lines
		self.score.score = score
		self.score.level = level

	def get_next_shape(self):
		next_shape = self.next_shapes.pop(0)
		self.next_shapes.append(choice(self.shapes_list))
		return next_shape

	def run(self):
		while True:
			self.game.quit_to_menu = False  # reset the flag before game starts

			while not self.game.quit_to_menu:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				self.display_surface.fill(GRAY)
				self.game.run()
				self.score.run()
				self.preview.run(self.next_shapes)
				pygame.display.update()
				self.clock.tick()

			# when game is over or user quits to menu
			self.level = self.ui.show_menu()

			# update shape list
			if self.level == 1:
				self.shapes_list = list(TETROMINOS.keys())
			elif self.level == 2:
				self.shapes_list = list(PENTOMINOS.keys())
			else:
				self.shapes_list = list(SHAPE.keys())

			# reinitialize components
			self.next_shapes = [choice(self.shapes_list) for shape in range(3)]
			self.game = Game(self.get_next_shape, self.update_score)
			self.score = Score()
			self.preview = Preview()

if __name__ == '__main__':
	main = Main()
	main.run()