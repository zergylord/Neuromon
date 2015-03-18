import pygame
from pygame import key as key
from GameObject import *
from globals import *
def Breeding(monList):
    def step():
        #render GUI
        pygame.display.update()
        screen.blit(background,[0,0])
        screen.blit(pygame.Surface((100,200)),[0,0])
        monNameText,_ = font.render(str(monList),(255,255,255))
        screen.blit(monNameText,[0,0])
        #handle input
        curPressed = key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True
                else:
                    return False
    #main excution f
    quit = False
    font = pygame.freetype.SysFont('',18)
    screen = pygame.display.get_surface()
    background = pygame.image.load("floor.jpg").convert()
    background = pygame.transform.scale(background,size)
    while not quit:
        quit = step()

