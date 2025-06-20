from settings import *

from pygame.image import load
from os import path

class Preview:
    """
    Класс предпросмотра следующих фигур (справа от игрового поля).
    """
    def __init__(self):
        self.dispaly_surface = pygame.display.get_surface()
        # Создаём отдельную поверхность для предпросмотра
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_FRACTION))
        self.rect = self.surface.get_rect(topright = (WINDOW_WIDHT - PADDING, PADDING))
        
        # shapes
        #self.next_shapes = next_shapes
        #self.shape_surfaces = {shape: load("../graphics/T.png") for shape in TETROMINOS.keys()}

        # Загружаем спрайты для всех фигур из PREVIEW_SPRITES (пути в settings.py)
        self.shape_surfaces = {shape: load(path.join(PREVIEW_SPRITES[shape])).convert_alpha() for shape in TETROMINOS.keys()}

        # image position data
        # Высота между фигурами предпросмотра
        self.increment_height = self.surface.get_height() / 3

    def display_pieces(self, shapes):
        """
        Отрисовывает три следующих фигуры на панели предпросмотра.
        """
        for i, shape in enumerate(shapes):
            #print(shape)
            shape_surface = self.shape_surfaces[shape]
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            rect = shape_surface.get_rect(center=(x, y))
            self.surface.blit(shape_surface, rect)

    def Update(self, next_shapes):
        """
        Обновляет предпросмотр: очищает поверхность, рисует новые фигуры, рисует рамку.
        """
        self.surface.fill(GRAY)
        self.display_pieces(next_shapes)
        self.dispaly_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.dispaly_surface, LINE_COLOR, self.rect, 2, 2)