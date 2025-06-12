from settings import *
from os.path import join
import save_data
import pygame

class Score:
    def __init__(self, score=0, level=1, lines=0):
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDHT - PADDING, WINDOW_HEIGHT - PADDING))
        self.font = pygame.font.SysFont("arial", 28)
        self.increment_height = self.surface.get_height() // 5  # теперь 5 строк

        # data
        self.score = score
        self.level = level
        self.lines = lines

    def display_text(self, pos, text, color="white"):
        text_surface = self.font.render(f"{text[0]}: {text[1]}", True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)

    def Update(self):
        self.surface.fill(GRAY)
        data = save_data.load_data()
        last_score = data.get("LAST_SCORE", 0)
        high_score = data.get("HIGH_SCORE", 0)

        fields = [
            ("Score", self.score, "white"),
            ("Level", self.level, "white"),
            ("Lines", self.lines, "white"),
            ("Last Score", last_score, "white"),
            ("Record", high_score, "white"),
        ]

        for i, (label, value, color) in enumerate(fields):
            x = self.surface.get_width() // 2
            y = self.increment_height / 2 + i * self.increment_height
            self.display_text((x, y), (label, value), color)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)