from settings import *

class Preview:
    def __init__(self):
        self.dispaly_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDHT - PADDING, PADDING))
        

    def Update(self):
        self.dispaly_surface.blit(self.surface, self.rect)