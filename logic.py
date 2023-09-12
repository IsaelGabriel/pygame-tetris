import pygame

BLOCK_SIZE = 32;

sample_tetraminoes: dict = {
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

test_tetraminoes = []

y = 0
for color, seed in sample_tetraminoes.items():
    test_tetraminoes.append(Tetramino(int(seed), 0, y, color))
    y += BLOCK_SIZE * 2

def tick(delta: float):
    pass

def render(screen: pygame.Surface):
    for t in test_tetraminoes:
        t.render(screen)