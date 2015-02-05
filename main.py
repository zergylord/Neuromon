import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
from Panoptir import *
from pygame import key as key
pygame.init()

size = width, height = 800, 600
velo = [0,0]
speed = 1;
black = 0,0,0


screen = pygame.display.set_mode(size)



count = 0

#setup players
player = Panoptir()
everybody = pygame.sprite.Group(player.sprite)
players = [player]

enemy = pygame.sprite.Sprite()
enemy.image = pygame.image.load("butterfly.jpg")
enemy.rect = enemy.image.get_rect()
enemy.rect = enemy.rect.move([300,300])
baddies = pygame.sprite.Group(enemy)
everybody.add(enemy)

#main game loop
while count < 100:
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

    for p in players:
        p.act(everybody)
        if (p.sprite.rect.left < 0 and p.velo[0] < 0) or (p.sprite.rect.right > width and p.velo[0]>0):
            p.velo[0] = 0
        if (p.sprite.rect.top < 0 and p.velo[1] < 0) or (p.sprite.rect.bottom > height and p.velo[1]>0):
            p.velo[1] = 0


    pygame.sprite.spritecollide(player.sprite,baddies,True)
    screen.fill(black)
    everybody.draw(screen)
    pygame.display.flip()
