import pygame
import main
import random

BLOCK_SIZE = 32

GAME_RECT_SIZE = (BLOCK_SIZE * 10, BLOCK_SIZE * 17)
GAME_RECT_POS = ((main.SCREEN_WIDTH - GAME_RECT_SIZE[0]) / 2, (main.SCREEN_HEIGHT - GAME_RECT_SIZE[1]) / 2)
GAME_RECT_COLOR = "#161616"

START_X = 3 * BLOCK_SIZE
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

FALL_SPEED: int = 32
MOVE_SPEED: int = BLOCK_SIZE

game_rect: pygame.Rect = pygame.Rect(GAME_RECT_POS, GAME_RECT_SIZE)

class Tetramino:
    def __init__(self, seed, x: int, y: int, color: str):
        global BLOCK_SIZE
        self._seed = seed
        self.color = color
        self.movement_locked = False
        self.rotation: int = 0
        self._rect_list = []
        self.topleft: pygame.math.Vector2 = pygame.math.Vector2(x, y)
        binary_seed = bin(seed)[2:]
        while len(binary_seed) != 8:
            binary_seed = "0" + binary_seed
        max_x = 0
        max_y = 0
        for i in range(8):
            if(binary_seed[i] != '0'):
                rect_position = (0, 0)

                if(i < 4):
                    #print(i)
                    rect_position = (x + BLOCK_SIZE*i, y)
                else:
                    rect_position = (x + BLOCK_SIZE*(i-4), y + BLOCK_SIZE)

                self._rect_list.append(pygame.Rect(rect_position, (BLOCK_SIZE, BLOCK_SIZE)))
                
                max_x = max(self._rect_list[-1].right, max_x)
                max_y = max(self._rect_list[-1].bottom, max_y)
        self.center: pygame.math.Vector2 = pygame.math.Vector2(x + max_x, y + max_y) * 0.5

    @property
    def x(self):
        return self.topleft.x
    
    @x.setter
    def x(self, new_x: float):
        global game_rect
        x_difference = new_x - self.x
        offset = 0.0
        for rect in self._rect_list:
            rect.x += x_difference
            if not game_rect.contains(rect):
                if x_difference > 0 and game_rect.right - rect.right < offset:
                    offset = game_rect.right - rect.right
                elif x_difference < 0 and game_rect.left - rect.left > offset:
                    offset = game_rect.left - rect.left
        
        if offset != 0:
            for rect in self._rect_list:
                rect.x += offset
                
        self.center.x += x_difference + offset
        self.topleft.x += x_difference + offset

    @property
    def y(self):
        return self.topleft.y
    
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
                    y_offset = game_rect.bottom - rect.bottom
        for rect in self._rect_list:
            rect.y += y_offset
        self.center.y += y_difference + y_offset
        self.topleft.y += y_difference + y_offset

    def render(self, screen: pygame.Surface):
        for rect in self._rect_list:
            pygame.draw.rect(screen, self.color, rect)

    def rotate(self):
        self.rotation += 1
        if(self.rotation > 3):
            self.rotation = 0
        topleft = self.center.copy()
        bottomright = self.center.copy()
        for rect in self._rect_list:
            center_distance: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
            center_distance.x = self.center.x - rect.centerx
            center_distance.y = self.center.y - rect.centery
            #print(self.center)
            #print(rect.center)

            x_mult = 1
            y_mult = 1

            if center_distance.x <= 0:
                y_mult = -1
            
            if center_distance.y >= 0:
                x_mult = -1



            rect.centerx = self.center.x + (abs(center_distance.y) * x_mult)
            rect.centery = self.center.y + (abs(center_distance.x) * y_mult)
            if rect.top < topleft.y:
                topleft.y = rect.top
            if rect.left < topleft.x:
                topleft.x = rect.left
            if rect.bottom > bottomright.y:
                bottomright.y = rect.bottom
            if rect.right > bottomright.x:
                bottomright.x = rect.right
        self.topleft = topleft.copy()
        self.center.x = (topleft.x + bottomright.x) / 2
        self.center.y = (topleft.y + bottomright.y) / 2
        #self.y = self.y

tetramino_list: list[Tetramino] = []
counter: float = 0.0
move_counter: float = 0.0
holding_down = False

def generate_tetramino():
    global GAME_RECT_POS, tetramino_list
    index: int = random.randint(0, 6)
    color: str = list(SAMPLE_TETRAMINOES.keys())[index]
    tetramino_list.append(Tetramino(SAMPLE_TETRAMINOES[color], GAME_RECT_POS[0] + START_X, GAME_RECT_POS[1] + START_Y, color))

def start():
    generate_tetramino()

def tick(delta: float):
    global counter, move_counter, holding_down, FALL_SPEED, MOVE_SPEED
    keys = pygame.key.get_pressed()
    holding_down = keys[pygame.K_DOWN]
    
    counter += delta if not holding_down else delta * 4
    if counter >= 1.0:
        if not tetramino_list[-1].movement_locked:
            tetramino_list[-1].y += FALL_SPEED
        if tetramino_list[-1].movement_locked:
            generate_tetramino()

        counter = 0.0

    move_counter += delta
    if move_counter >= 0.25:
        if not tetramino_list[-1].movement_locked:
            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                tetramino_list[-1].x -= MOVE_SPEED
            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                tetramino_list[-1].x += MOVE_SPEED
        
        move_counter = 0.0


def rotate():
    global tetramino_list
    if not tetramino_list[-1].movement_locked:
        tetramino_list[-1].rotate()

def render(screen: pygame.Surface):
    global GAME_RECT_COLOR, game_rect, tetramino_list
    pygame.draw.rect(screen, GAME_RECT_COLOR, game_rect)
    for t in tetramino_list:
        t.render(screen)