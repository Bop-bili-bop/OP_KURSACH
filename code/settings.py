﻿import pygame

# Game size
COLUMNS = 10
ROWS = 20
CELL_SIZE = 40
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

# side bar size
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

# window
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# game behaviour
UPDATE_START_SPEED = 200
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

# Colors
YELLOW = '#f1e60d'
RED = '#e51b20'
BLUE = '#204b9b'
GREEN = '#65b32e'
PURPLE = '#7b217f'
CYAN = '#6cc6d9'
ORANGE = '#f07e13'
PINK = '#f389f5'
CORAL = '#f68187'
SKY_BLUE = '0098dc'
BIEGE = 'f6ca9f'
GRAY = '#1C1C1C'
LINE_COLOR = '#FFFFFF'

# shapes
TETROMINOS = {
	'T_Tetromino': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': BIEGE},
	'O_Tetromino': {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': YELLOW},
	'J_Tetromino': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': BLUE},
	'L_Tetromino': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': ORANGE},
	'I_Tetromino': {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': CYAN},
	'S_Tetromino': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': GREEN},
	'Z_Tetromino': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': RED}
}

SCORE_DATA = {1: 100, 2: 300, 3: 700, 4: 1500, 5: 2500}