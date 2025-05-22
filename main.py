import pygame
import sys
from settings import *
from game import Game

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WoW Survivors")
clock = pygame.time.Clock()

# Create game instance
game = Game(screen, clock)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update and render game
    game.run()
    
    # Update display
    pygame.display.flip()
    
pygame.quit()
sys.exit()