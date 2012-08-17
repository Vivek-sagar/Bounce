import pygame

def run_game():
	SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
	BG_COLOR = 200, 200, 100

	pygame.init()

	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0)
	clock = pygame.time.Clock()

	running = True

	while running:
		clock.tick(50)
		screen.fill(BG_COLOR)
		pygame.display.flip()

run_game()

