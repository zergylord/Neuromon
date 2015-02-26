import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
from Panoptir import *
from World import *
from pygame import key as key
from globals import *
import rlglue.RLGlue as RLGlue
from rlglue.environment import EnvironmentLoader as EnvironmentLoader

pygame.init()


useGlue = False

velo = [0,0]
speed = 1;
black = 0,0,0


screen = pygame.display.set_mode(size)#,pygame.FULLSCREEN)
background = pygame.image.load("floor.jpg")
background = pygame.transform.scale(background,size)
count = 0
world = World()

if len(sys.argv) > 1:
    iType = sys.argv[1]
    world.players[0].iType = int(iType)

if useGlue:
    EnvironmentLoader.loadEnvironment(World())
    taskSpec = RLGlue.RL_init()
    RLGlue.RL_start()
    stepResponse = RLGlue.RL_step()
else:
    world.start()

#main game loop
while (not useGlue) or stepResponse.terminal != 1:
    #count+= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    curPressed = key.get_pressed()
    if curPressed[pygame.K_ESCAPE]:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    if curPressed[pygame.K_p]:
        pixels = np.array(pygame.surfarray.array2d(screen))
        plt.imshow(pixels)
        plt.show()

    if useGlue:
        stepResponse = RLGlue.RL_step()
    else:
        world.step()



    #screen.fill(black)
    screen.blit(background,[0,0])
    world.everybody.draw(screen)
    world.effects.draw(screen)
    pygame.display.flip()

if useGlue:
    RLGlue.RL_cleanup()
