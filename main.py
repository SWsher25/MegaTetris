from settings import *
import settings
from sys import exit
from os.path import join
import save_data
import os

# components
from game import Game
from score import Score
from preview import Preview
from menu import Menu, SettingsMenu

from random import choice

data = save_data.load_data()
for key, value in data.items():
    setattr(settings, key, value)

class Main():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("MegaTetris")

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # components
        self.game = Game(self.get_next_shape, self.update_score)
        # Передаём стартовые значения в Score
        self.score = Score(
            score=self.game.current_score,
            level=self.game.current_level,
            lines=self.game.current_lines
        )
        self.preview = Preview()

        # audio
        self.music = pygame.mixer.Sound(settings.MUSIC_PATH)
        self.music.set_volume(save_data.load_data().get("MUSIC_VOLUME", settings.DEFAULT_MUSIC_VOLUME))
        self.music.play(-1)

        # font
        self.font = pygame.font.SysFont(settings.FONT_MAIN, settings.FONT_MAIN_SIZE)
        self.title_font = pygame.font.SysFont(settings.FONT_MAIN, settings.FONT_TITLE_SIZE, bold=True)
        bg_path = os.path.join(os.path.dirname(__file__), settings.MENU_BG_PATH)
        button_sprite_path = settings.BUTTON_SPRITE_PATH

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def Update(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False  # выйти из игрового цикла

            if self.game.game_over: running = False

            # Display
            self.display_surface.fill(GRAY)

            # components
            self.game.Update()
            self.score.Update()
            self.preview.Update(self.next_shapes)
            pygame.display.update()
            self.clock.tick()

    def stop_music(self):
        if hasattr(self, "music"):
            self.music.stop()


def start_game():
    main = Main()
    main.Update()
    main.stop_music()  # Остановить музыку после выхода из игрового цикла

def open_settings():
    settings_menu = SettingsMenu(menu.Update)
    settings_menu.Update()

def exit_game():
    pygame.quit()
    exit()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))
    menu = Menu(start_game, open_settings, exit_game)
    while True:
        menu.Update()