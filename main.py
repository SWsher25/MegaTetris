from settings import *
from sys import exit

# components
from game import Game
from score import Score
from preview import Preview

class Main():
    def __init__(self):
        
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDHT, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("MegaTetris")

        # components
        self.game = Game()
        self.score = Score()
        self.preview = Preview()

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
            self.preview.Update()
            
            
            
            
            pygame.display.update()
            self.clock.tick()

if __name__ == "__main__":
    main = Main()
    main.Update()