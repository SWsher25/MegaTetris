import settings
from settings import *
from random import choice
from sys import exit
from os.path import join

from timer import Timer
import save_data

class Game:

    def __init__(self, get_next_shape, update_score):
        
        # general
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        # game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # test
        #self.block = Block(self.sprites, pygame.Vector2(3, 5), RED)

        # tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)
        
        #score
        self.current_level = settings.START_LEVEL
        self.current_score = 0
        self.current_lines = 0

        # Тайминги с учётом уровня
        self.down_speed = UPDATE_START_SPEED * (settings.SPEEDUP_COEFF ** (self.current_level - 1))
        self.move_wait_time = MOVE_WAIT_TIME
        self.rotate_wait_time = ROTATE_WAIT_TIME * (settings.SPEEDUP_COEFF ** (self.current_level - 1))
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            "vertical move": Timer(self.down_speed, True, self.move_down),
            "horizontal move": Timer(self.move_wait_time),
            "rotate": Timer(self.rotate_wait_time)
        }
        self.timers["vertical move"].activate()

        

        # sound
        self.landing_sound = pygame.mixer.Sound(settings.LANDING_SOUND_PATH)
        self.landing_sound.set_volume(save_data.load_data().get("EFFECTS_VOLUME", settings.DEFAULT_EFFECTS_VOLUME))

        # game over flag
        self.game_over = False

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_level

        # every 10 lines increase level
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            # Пересчитываем все тайминги!
            self.down_speed *= settings.SPEEDUP_COEFF
            self.down_speed_faster = self.down_speed * 0.3
            self.move_wait_time *= settings.SPEEDUP_COEFF
            #self.rotate_wait_time *= settings.SPEEDUP_COEFF
            self.timers["vertical move"].duration = self.down_speed
            self.timers["horizontal move"].duration = self.move_wait_time
            self.timers["rotate"].duration = self.rotate_wait_time

        self.update_score(self.current_lines, self.current_score, self.current_level)
        
    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                data = save_data.load_data()
                data["LAST_SCORE"] = self.current_score
                if self.current_score > data.get("HIGH_SCORE", 0):
                    data["HIGH_SCORE"] = self.current_score
                save_data.save_data(data)
                #exit()
                self.game_over = True

    def create_new_tetromino(self):
        
        #sound
        self.landing_sound.play()

        self.check_game_over()
        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(), 
            self.sprites, 
            self.create_new_tetromino,
            self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.Update()

    def move_down(self):
        self.tetromino.move_down()
        #print("timer")

    def draw_grid(self):

        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0, y), (self.surface.get_width(), y))

        self.surface.blit(self.line_surface, (0, 0))

    def Input(self):
        keys = pygame.key.get_pressed()

        # horizontal movement
        if not self.timers["horizontal move"].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers["horizontal move"].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers["horizontal move"].activate()

        # rotation
        if not self.timers["rotate"].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers["rotate"].activate()

        # down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers["vertical move"].duration = self.down_speed_faster
            
        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers["vertical move"].duration = self.down_speed
                
    def check_finished_rows(self):

        #get full row undexers
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:

                #delete full rows
                for block in self.field_data[delete_row]:
                    block.kill()

                #move blocks down
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1
                            #block.rect.y += CELL_SIZE

            #rebuild the field data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
               self.field_data[int(block.pos.y)][int(block.pos.x)] = block
        
            # update_score
            self.calculate_score(len(delete_rows))

    def Update(self):

        self.Input()

        # update the timer
        self.timer_update()

        self.sprites.update()
        
        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        
        # display
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
        
        # update the display
        #pygame.display.update()            


class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):

        # setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]["shape"]
        self.color = TETROMINOS[shape]["color"]
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        # create blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    

    # collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False
    
    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    # movement
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount
               # block.rect.x += CELL_SIZE * amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
                #block.rect.y += CELL_SIZE
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

            # landing sound
            self.music = pygame.mixer.Sound(join("sound", "landing.wav"))
            self.music.set_volume(save_data.load_data().get("EFFECTS_VOLUME", settings.DEFAULT_MUSIC_VOLUME))
            self.music.play()

    # rotate
    def rotate(self):
        #print("rotate")
        if self.shape != "O":

            # 1. pivot point
            pivot_pos = self.blocks[0].pos

            # 2. new block positions
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # 3. collisions check
            for pos in new_block_positions:
                #horizontal
                if pos.x < 0 or pos.x >= COLUMNS:
                    return
                
                # vectical / floor check
                if pos.y >= ROWS:
                    return
                
                #field check -> collision with other pieces
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return
                
                
            
            # implement new positions
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):

        # general
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):
        # distance = self.pos - pivot_pos
        # rotated = distance.rotate(90)
        # new_pos = pivot_pos + rotated
        # return new_pos
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True
        
        if field_data[int(self.pos.y)][x]:
            return True
        
    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True
        
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        # self.pos -> self.rect
        #self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)
        self.rect.topleft = self.pos * CELL_SIZE
