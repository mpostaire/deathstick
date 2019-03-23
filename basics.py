
import pygame
import time
from pygame.locals import *
MAX_FPS = 60
clock = None
frame_count = 0

actors = None

def main():
    # Initialise screen
    global clock
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((150, 50))
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    #Game delta


    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        
        delta = clock.tick(60)
        global frame_count
        frame_count = frame_count + 1

        background.fill((250, 250, 250))
        if frame_count % 2 == 0:
            text = font.render("General Kenobi", 1, (255, 0, 0))
        else:
            text = font.render("Hello there", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)
        

        
        #beginning of the logic

        
        
        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == '__main__': main()
