import pygame
import main
import random

BLOCK_SIZE = 32
START_X = (main.SCREEN_WIDTH / 2) - (2 * BLOCK_SIZE)
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

class Tetramino:
    def __init__(self, seed, x: int, y: int, color: str):
        global BLOCK_SIZE
        self.seed = seed
        self.color = color
        self.rect_list = []
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

                self.rect_list.append(pygame.Rect(rect_position, (BLOCK_SIZE, BLOCK_SIZE)))
    
    def render(self, screen: pygame.Surface):
        for rect in self.rect_list:
            pygame.draw.rect(screen, self.color, rect)

tetramino_list: list[Tetramino] = []

def generate_tetramino():
    global tetramino_list
    index: int = random.randint(0, 6)
    color: str = list(SAMPLE_TETRAMINOES.keys())[index]
    tetramino_list.append(Tetramino(SAMPLE_TETRAMINOES[color], START_X, START_Y, color))

def start():
    global tetramino_list
    generate_tetramino()

counter: float = 0.0

def tick(delta: float):
    global counter
    counter += delta
    if counter >= 1.0:
        del(tetramino_list[0])

        generate_tetramino()

        counter = 0.0

def render(screen: pygame.Surface):
    for t in tetramino_list:
        t.render(screen)