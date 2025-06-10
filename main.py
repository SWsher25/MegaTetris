from settings import *
from sys import exit
from os.path import join

# components
from game import Game
from score import Score
from preview import Preview

from random import choice

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
        self.score = Score()
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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Display
            self.display_surface.fill(GRAY)

            # components
            self.game.Update()
            self.score.Update()
            self.preview.Update(self.next_shapes)
            
            
            
            
            pygame.display.update()
            self.clock.tick()

if __name__ == "__main__":
    main = Main()
    main.Update()