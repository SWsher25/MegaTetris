from settings import *
import settings
from sys import exit
from os.path import join
import save_data

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
        self.music = pygame.mixer.Sound(join("sound", "tetris.mp3"))
        self.music.set_volume(0.5)
        self.music.play(-1)

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


def start_game():
    main = Main()
    main.Update()

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