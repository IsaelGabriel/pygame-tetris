import pygame
import main
import random

BLOCK_SIZE = 32

ROWS = 18
COLUMNS = 10

GAME_RECT_SIZE = (BLOCK_SIZE * COLUMNS, BLOCK_SIZE * ROWS)
GAME_RECT_POS = ((main.SCREEN_WIDTH - GAME_RECT_SIZE[0]) / 2, 0) #(main.SCREEN_HEIGHT - GAME_RECT_SIZE[1]) / 2)
GAME_RECT_COLOR = "#161616"


START_X = 0 # 3 * BLOCK_SIZE
START_Y = -BLOCK_SIZE * 2 #1 * BLOCK_SIZE #- BLOCK_SIZE / 2

static_blocks = [[]] * ROWS

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
        self.colliding = False
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
        global BLOCK_SIZE, GAME_RECT_POS, game_rect, static_blocks
        if self.movement_locked: return
        x_difference = new_x - self.x
        
        border_offset = 0.0
        collision_offset = 0.0
        for rect in self._rect_list:
            collision_rect: pygame.Rect
            if x_difference > 0:
                collision_rect = pygame.Rect(rect.left, rect.top, rect.w + x_difference, rect.h)
            else:
                collision_rect = pygame.Rect(rect.left + x_difference, rect.top, rect.w - x_difference, rect.h)

            for row in static_blocks:
                for block in row:
                    if collision_rect.colliderect(block):
                        rect_difference = block.left - collision_rect.right
                        if x_difference < 0: rect_difference = block.right - collision_rect.left
                        if abs(rect_difference) > abs(collision_offset):
                            collision_offset = rect_difference

            rect.x += x_difference

        for rect in self._rect_list:

            rect.x += collision_offset

            if not game_rect.contains(rect):
                right_difference = game_rect.right - rect.right
                left_difference =  game_rect.left - rect.left
                center_difference = game_rect.centerx - rect.centerx
                if center_difference < 0 and right_difference < border_offset:
                    border_offset = right_difference
                elif center_difference > 0 and left_difference  > border_offset:
                    border_offset = left_difference 
            
            rect.left -= (rect.left - GAME_RECT_POS[0]) % BLOCK_SIZE
        
        if border_offset != 0:
            for rect in self._rect_list:
                rect.x += border_offset
                
        self.center.x += x_difference + border_offset + collision_offset
        self.topleft.x += x_difference + border_offset + collision_offset

    @property
    def y(self):
        return self.topleft.y
    
    @y.setter
    def y(self, new_y: float):
        global game_rect, static_blocks
        if self.movement_locked: return
        y_difference = new_y - self.y
        y_border_offset = 0
        y_collision_offset = 0
        self.colliding = False
        for rect in self._rect_list:
            if y_difference > 0:
                collision_rect = pygame.Rect(rect.left, rect.top, rect.w, rect.h + y_difference)
                for row in static_blocks:
                    for block in row:
                        difference = -(collision_rect.bottom - block.top)
                        if collision_rect.colliderect(block) and difference < y_collision_offset:
                            self.colliding = True
                            y_collision_offset = difference

            rect.y += y_difference
            

        for rect in self._rect_list:
            rect.y += y_collision_offset
            if not game_rect.contains(rect):
                    if rect.bottom > game_rect.bottom:
                        self.movement_locked = True
                        if game_rect.bottom - rect.bottom < y_border_offset:
                            y_border_offset = game_rect.bottom - rect.bottom
        
        for rect in self._rect_list:
            rect.y += y_border_offset
        self.center.y += y_difference + y_border_offset + y_collision_offset
        self.topleft.y += y_difference + y_border_offset + y_collision_offset

    def render(self, screen: pygame.Surface):
        for rect in self._rect_list:
            pygame.draw.rect(screen, self.color, rect)

    def rotate(self):
        global static_blocks
        collided = False
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

            for row in static_blocks:
                for block in row:
                    if rect.colliderect(block):
                        collided = True
            
        if collided:
            for rect in self._rect_list:
                center_distance: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
                center_distance.x = self.center.x - rect.centerx
                center_distance.y = self.center.y - rect.centery
                x_mult = 1
                y_mult = 1

                if center_distance.x >= 0:
                    y_mult = -1
                
                if center_distance.y <= 0:
                    x_mult = -1

                rect.centerx = self.center.x + (abs(center_distance.y) * x_mult)
                rect.centery = self.center.y + (abs(center_distance.x) * y_mult)

            return
        
        top = self._rect_list[0].top
        bottom = self._rect_list[0].bottom
        left = self._rect_list[0].left
        right = self._rect_list[0].right

        for rect in self._rect_list:
            if rect.top < top:
                top = rect.top
            if rect.left < left:
                left = rect.left
            if rect.bottom > bottom:
                bottom = rect.bottom
            if rect.right > right:
                right = rect.right
        self.topleft = pygame.math.Vector2(left, top)
        self.center.x = (left + right) / 2
        self.center.y = (top + bottom) / 2
        self.y = self.y
        self.x = self.x

tetramino_list: list[Tetramino] = []
counter: float = 0.0
move_counter: float = 0.0
holding_down = False

def get_static_blocks():
    global BLOCK_SIZE, GAME_RECT_POS, ROWS, tetramino_list, static_blocks
    static_blocks = [[] for _ in range(ROWS)]
    for tetramino in tetramino_list:
        if not tetramino.movement_locked: continue
        if len(tetramino._rect_list) == 0:
            del(tetramino)
        else:
            for rect in tetramino._rect_list:
                row = int((rect.top - GAME_RECT_POS[1]) / BLOCK_SIZE)
                static_blocks[row].append(rect)
    #print(static_blocks)

def generate_tetramino():
    global GAME_RECT_POS, BLOCK_SIZE
    global tetramino_list, static_blocks

    index: int = random.randint(0, 6)
    color: str = list(SAMPLE_TETRAMINOES.keys())[index]
    tetramino_list.append(Tetramino(SAMPLE_TETRAMINOES[color], GAME_RECT_POS[0] + START_X, GAME_RECT_POS[1] + START_Y, color))

    get_static_blocks()

    excluded_rows = []

    for row in range(ROWS):
        if len(static_blocks[row]) >= COLUMNS:
            excluded_rows.append(row)

    for row in range(ROWS):
        for rect in static_blocks[row]:
            for tetramino in tetramino_list:
                if not tetramino.movement_locked: continue
                if not rect in tetramino._rect_list: continue
                rect.top = int(rect.top)
                offset = (rect.top - GAME_RECT_POS[1]) % BLOCK_SIZE
                if offset < GAME_RECT_SIZE[1] / 2:
                    rect.top -= offset
                else:
                    rect.top += offset

                #row = int((rect.top - GAME_RECT_POS[1]) / BLOCK_SIZE)
                if row in excluded_rows:
                    tetramino._rect_list.remove(rect)
                    break
    
    for row in range(ROWS):
        for rect in static_blocks[row]:
                #if (rect.top - GAME_RECT_POS[1]) % BLOCK_SIZE != 0: print(rect.top)
                rect.top = int(rect.top)
                for exc_row in excluded_rows:
                    if row < exc_row:
                        rect.top += BLOCK_SIZE

    get_static_blocks()
    # cu



def start():
    get_static_blocks()
    generate_tetramino()

def tick(delta: float):
    global BLOCK_SIZE, FALL_SPEED, MOVE_SPEED, GAME_RECT_POS, ROWS, COLUMNS
    global counter, move_counter, holding_down
    keys = pygame.key.get_pressed()
    holding_down = keys[pygame.K_DOWN]

    counter += delta if not holding_down else delta * 10
    if counter >= 1.0:
        if not tetramino_list[-1].movement_locked:
            if tetramino_list[-1].colliding:
                tetramino_list[-1].movement_locked = True
            else:
                tetramino_list[-1].y += FALL_SPEED
        elif tetramino_list[-1].movement_locked:
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
    global GAME_RECT_COLOR, game_rect, tetramino_list, static_blocks
    pygame.draw.rect(screen, GAME_RECT_COLOR, game_rect)
    for tetramino in tetramino_list:
        tetramino.render(screen)