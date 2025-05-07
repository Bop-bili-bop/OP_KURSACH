from settings import *
import pygame
from os.path import join

class UIScreen:
    def __init__(self, surface, display_surface, font, big_font, title_font, menu_font, clock, current_score):
        self.surface = surface
        self.display_surface = display_surface
        self.font = font
        self.big_font = big_font
        self.title_font = title_font
        self.menu_font = menu_font
        self.clock = clock
        self.current_score = current_score

    def draw_pause_screen(self):
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.surface.blit(overlay, (0, 0))
        pause_text = self.font.render("Paused", True, (255, 255, 255))
        instructions_text = self.font.render("Q - Quit To Main Menu", True, (255, 255, 255))
        self.surface.blit(pause_text, pause_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2)))
        self.surface.blit(instructions_text, instructions_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 40)))

    def draw_game_over_screen(self):
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.surface.blit(overlay, (0, 0))
        title = self.big_font.render("GAME OVER", True, (255, 0, 0))
        score = self.font.render(f"Your Score: {self.current_score}", True, (255, 255, 255))
        quit_text = self.font.render("Q - Quit To Main Menu", True, (255, 255, 255))
        self.surface.blit(title, title.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 40)))
        self.surface.blit(score, score.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2)))
        self.surface.blit(quit_text, quit_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 40)))

    def draw_menu_background(self):
        menu_bg = pygame.image.load(join('..', 'graphics', 'bg.jpg')).convert()
        bg_rect = menu_bg.get_rect()
        display_rect = self.display_surface.get_rect()
        x = (display_rect.width - bg_rect.width) // 2
        y = (display_rect.height - bg_rect.height) // 2
        self.display_surface.fill((10, 10, 30))
        self.display_surface.blit(menu_bg, (x, y))

    def show_menu(self):
        options = [
            "Tetromino Mode",
            "Pentomino Mode",
            "Mixed Mode",
            "Exit Game"
        ]
        selected = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % 4
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if selected == 3:
                            pygame.quit()
                            exit()
                        else:
                            return selected + 1

            self.draw_menu_background()

            title_surf = self.title_font.render("TETRIS", True, (255, 215, 0))
            title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
            self.display_surface.blit(title_surf, title_rect)

            for idx, text in enumerate(options):
                color = (255, 215, 0) if idx == selected else (255, 255, 255)
                label = self.menu_font.render(text, True, color)
                rect = label.get_rect(center=(WINDOW_WIDTH // 2,
                                              WINDOW_HEIGHT // 2 + idx * 60))
                self.display_surface.blit(label, rect)

            pygame.display.update()
            self.clock.tick(60)
