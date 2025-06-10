from settings import *

class Score:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDHT - PADDING, WINDOW_HEIGHT - PADDING))
        

    def Update(self):
        self.display_surface.blit(self.surface, self.rect)