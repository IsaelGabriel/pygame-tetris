import pygame
import logic

SCREEN_WIDTH: int = 800 # px 
SCREEN_HEIGHT: int = 600 # px
FRAME_RATE: int = 60 # FPS
REFRESH_COLOR: str = '#2A2A2A'

def main():
    global SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE, REFRESH_COLOR
    # start pygame
    pygame.init()
    pygame.display.set_caption("Tetraminoes")
    game_screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True

    delta: float = 0.0

    logic.start()

    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                    break
                case pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        logic.rotate()


        # Tick
        logic.tick(delta)

        # Clear screen
        game_screen.fill(REFRESH_COLOR)    

        # Render    

        logic.render(game_screen)

        # End rendering
        pygame.display.flip()
        
        delta = game_clock.tick(FRAME_RATE) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()