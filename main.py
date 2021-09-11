import pygame
import random
import time

from random import * 

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

FRAME_DELAY = 0.3 # seconds

MAX_STRAND_LENGTH = 30 # max char length - the strands can not grow beyond this.
MAX_RAIN_SPEED = 50 # pixels per tick
MIN_RAIN_SPEED= 25 # pixels per tick


RAIN_SPAWN_RATE = 4 # spawn rate x / tick

ANTI_ALIASING = 1
FONT_SIZE = 16 

SYMBOLS = 'abcdefghjijklnmopqrstuvwxyz'

class Strand:
    """ a string of text where the characters mutate randomly """ 
    def __init__(self, row, column):
        self.chars = list(''.join([choice(SYMBOLS) for x in range(0,4)]))
        self.row = row
        self.column = column
        self.lifetime = 0
        self.mutate_rate = 3
        self.max_strand_length = randint(0, MAX_STRAND_LENGTH)
        self.rain_speed = randint(MIN_RAIN_SPEED, MAX_RAIN_SPEED)

    def grow(self):
        self.chars.append(choice('abcdefghijklmnop'))

    def tick(self):
        """ react to a game tick event """ 
        self.lifetime += 1 
        if len(self.chars) < self.max_strand_length:
            self.grow()
        else:
            self.row += 1 # mutate the start row so it falls even if it doesn't shrink
        if self.lifetime % self.mutate_rate == 0:
            self.random_mutation()


    def random_mutation(self):
        for i in range(0, len(self.chars)):
            self.chars[i] = choice('abcdef')


    def render(self, screen):
        font = pygame.font.SysFont('dejavusansmono', FONT_SIZE)
        for idx, char in enumerate(self.chars):
            # we have to create "shades of green depending on the how close to the head the char is"
            char_color = GREEN
            if idx == len(self.chars) - 1:
                char_color = WHITE
            char_surface = font.render(char, ANTI_ALIASING, char_color)
            offset = self.row
            screen.blit(char_surface, (self.column, self.row + idx * FONT_SIZE)) # draw in {x,y}
            pygame.display.update()

        


class Matrix:
    """ the actual matrix, with random strands of text 'raining' down""" 
    def __init__(self, screen, rows, cols, height, width):
        self.frame = 0
        self.screen = screen
        self.screen.fill(BLACK)
        self.rows = rows
        self.cols = cols
        self.height = height
        self.width = width
        self.strands = [Strand(10,10)]
        self.strand_spawnrate = 1 # seconds? ms? to determine


    def spawn(self):
        pass

    def tick(self):
        """ react to a game tick event """ 
        self.frame += 1
        for strand in self.strands:
            strand.tick()
        if self.frame % RAIN_SPAWN_RATE == 0:
            new_strand = Strand(randint(0, self.height // 5), randint(0, self.width))
            self.strands.append(new_strand)

    def render(self):
        """ render the matrix on the screen """
        self.screen.fill(BLACK)
        for strand in self.strands:
            strand.render(self.screen)

if __name__ == '__main__':
    screen_height, screen_width = 800, 800
    size = (screen_height, screen_width)
    pygame.init()
    print(pygame.font.get_fonts())

    screen = pygame.display.set_mode(size)
    m = Matrix(screen, 30, 30, screen_height, screen_width)
    last_frame = time.time()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
        if (time.time() - last_frame) > FRAME_DELAY:
            m.tick()
            m.render()
            last_frame = time.time()
