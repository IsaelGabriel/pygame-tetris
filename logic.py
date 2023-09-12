import pygame
import main
import random

BLOCK_SIZE = 32

GAME_RECT_POS = (100, 64)
GAME_RECT_SIZE = (main.SCREEN_WIDTH - (2 * GAME_RECT_POS[0]), main.SCREEN_HEIGHT - (2 * GAME_RECT_POS[1]))
GAME_RECT_COLOR = "#161616"

START_X = (GAME_RECT_SIZE[0] / 2) - (2 * BLOCK_SIZE)
START_Y = 0 #- BLOCK_SIZE / 2

SAMPLE_TETRAMINOES: dict = {
    "yellow": 0b11001100, # Block
    "purple": 0b11100100, # T
    "orange": 0b00101110, # L
    "blue":   0b10001110, # Reverse L
    "cyan":   0b11110000, # Straight
    "red":    0b11000110, # Z
    "green":  0b01101100  # S
}

game_rect: pygame.Rect = pygame.Rect(GAME_RECT_POS, GAME_RECT_SIZE)

class Tetramino:
    def __init__(self, seed, x: int, y: int, color: str):
        global BLOCK_SIZE
        self._seed = seed
        self.color = color
        self.movement_locked = False
        self._rect_list = []
        binary_seed = bin(seed)[2:]
        while len(binary_seed) != 8:
            binary_seed = "0" + binary_seed
        for i in range(8):
            if(binary_seed[i] != '0'):
                rect_position = (0, 0)

                if(i < 4):
                    #print(i)
                    rect_position = (x + BLOCK_SIZE*i, y)
                else:
                    rect_position = (x + BLOCK_SIZE*(i-4), y + BLOCK_SIZE)

                self._rect_list.append(pygame.Rect(rect_position, (BLOCK_SIZE, BLOCK_SIZE)))
    
    @property
    def x(self):
        return self.rect_list[0].x
    
    @x.setter
    def x(self, new_x: float):
        x_difference = new_x - self.x
        for rect in self._rect_list:
            rect.x += x_difference

    @property
    def y(self):
        return self._rect_list[0].y
    
    @y.setter
    def y(self, new_y: float):
        global game_rect
        y_difference = new_y - self.y
        inside_game_rect: bool = True
        y_offset = 0
        for rect in self._rect_list:
            rect.y += y_difference
            if not game_rect.contains(rect):
                inside_game_rect = False
                if y_difference >= 0:
                    self.movement_locked = True
                if abs(game_rect.bottom - rect.bottom) > abs(y_offset):
                    y_offset = game_rect.bottom - rect.bottom
        for rect in self._rect_list:
            rect.y += y_offset
        


    def render(self, screen: pygame.Surface):
        for rect in self._rect_list:
            pygame.draw.rect(screen, self.color, rect)

tetramino_list: list[Tetramino] = []

def generate_tetramino():
    global GAME_RECT_POS, tetramino_list
    index: int = random.randint(0, 6)
    color: str = list(SAMPLE_TETRAMINOES.keys())[index]
    tetramino_list.append(Tetramino(SAMPLE_TETRAMINOES[color], GAME_RECT_POS[0] + START_X, GAME_RECT_POS[1] + START_Y, color))

def start():
    global tetramino_list
    generate_tetramino()

counter: float = 0.0

def tick(delta: float):
    global counter
    counter += delta
    if counter >= 1.0:
        if not tetramino_list[-1].movement_locked:
            tetramino_list[-1].y += BLOCK_SIZE / 2

        counter = 0.0

def render(screen: pygame.Surface):
    pygame.draw.rect(screen, GAME_RECT_COLOR, game_rect)
    for t in tetramino_list:
        t.render(screen)