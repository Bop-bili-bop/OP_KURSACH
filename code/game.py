import pygame.display
from timer import Timer
from menu import *
from shapemino import *
from utils import *

class Game:
    def __init__(self, get_next_shape, update_score):
        self.quit_to_menu = False

        # general
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))
        self.sprites = pygame.sprite.Group()
        # score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

        # font
        self.big_font = font_init(32)
        self.font = font_init(20)
        self.ui = UIScreen(
            surface=self.surface,
            display_surface=self.display_surface,
            font=self.font,
            big_font=self.big_font,
            title_font=None,
            menu_font=None,
            clock=None,
            current_score=self.current_score
        )


        # game state
        self.paused = False
        self.game_over = False

        # game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # current mino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        first_shape = self.get_next_shape()
        if first_shape in PENTOMINOS:
            self.current_mino = Pentomino(
                first_shape,
                self.sprites,
                self.create_new_mino,
                self.field_data
            )
        else:
            self.current_mino = Tetromino(
                first_shape,
                self.sprites,
                self.create_new_mino,
                self.field_data
            )

        # timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(self.down_speed, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()

        # audio
        music_path = join('..', 'sounds', 'music.wav')
        self.music = pygame.mixer.music
        self.music.load(music_path)
        self.music.set_volume(0.2)
        self.music.play(-1)
        self.line_clear_sound = pygame.mixer.Sound(join('..', 'sounds', 'line_clear_effect.wav'))
        self.line_clear_sound.set_volume(0.1)
        self.landing_sound = pygame.mixer.Sound(join('..', 'sounds', 'landing.wav'))
        self.landing_sound.set_volume(0.1)
        self.game_over_sound = pygame.mixer.Sound(join('..', 'sounds', 'game_over_effect.wav'))
        self.game_over_sound.set_volume(0.1)

    def check_game_over(self):
        for block in self.current_mino.blocks:
            if block.pos.y < 0:
                self.game_over = True
                self.landing_sound.stop()
                self.line_clear_sound.stop()

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        if self.current_score > 200:
            self.current_level += 1
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def create_new_mino(self):
        self.landing_sound.play()
        self.check_game_over()
        if self.game_over:
            return
        self.check_finished_rows()
        next_shape = self.get_next_shape()
        if next_shape in PENTOMINOS:
            self.current_mino = Pentomino(
                next_shape,
                self.sprites,
                self.create_new_mino,
                self.field_data
            )
        else:
            self.current_mino = Tetromino(
                next_shape,
                self.sprites,
                self.create_new_mino,
                self.field_data
            )

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.current_mino.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)

        self.surface.blit(self.line_surface, (0, 0))
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_p] and not self.game_over:
            self.paused = not self.paused
            pygame.time.wait(200)
        if self.paused and keys[pygame.K_q]:
            self.quit_to_menu = True
            return
        if self.game_over:
            self.music.stop()
            if keys[pygame.K_q]:
                self.quit_to_menu = True  # ← instead of exit()
                return
            return

        if self.paused:
            return

        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.current_mino.move_horizontal(-1)
                self.timers['horizontal move'].activate()

            if keys[pygame.K_RIGHT]:
                self.current_mino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.current_mino.rotate()
                self.timers['rotate'].activate()

        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed

    def check_finished_rows(self):
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                for block in self.field_data[delete_row]:
                    block.kill()
                    self.line_clear_sound.play()

                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.calculate_score(len(delete_rows))

    def run(self):
        self.input()
        if self.paused and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        elif not self.paused and not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        if not self.paused and not self.game_over:
            self.timer_update()
            self.sprites.update()
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        self.draw_grid()
        if self.game_over:
            self.music.stop()
            self.ui.current_score = self.current_score
            self.ui.draw_game_over_screen()
            self.timers['vertical move'].deactivate()
            self.timers['horizontal move'].deactivate()
            self.timers['rotate'].deactivate()
        elif self.paused:
            self.ui.draw_pause_screen()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

