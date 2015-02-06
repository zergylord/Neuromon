import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
from pygame import key as key
pygame.init()

size = width, height = 800, 600
velo = [0,0]
speed = 1;
black = 0,0,0


screen = pygame.display.set_mode(size)

sprite = pygame.sprite.Sprite()
sprite.image = pygame.image.load("butterfly.jpg")
sprite.rect = sprite.image.get_rect()
sprite.radius = sprite.rect.height/2
sprite.health = 3;
everybody = pygame.sprite.Group(sprite)

enemy = pygame.sprite.Sprite()
enemy.image = pygame.image.load("butterfly.jpg")
enemy.rect = enemy.image.get_rect()
enemy.rect = enemy.rect.move([300,300])
enemy.radius = enemy.rect.height/2
baddies = pygame.sprite.Group(enemy)
everybody.add(enemy)

temp = pygame.sprite.Sprite()
temp.image = pygame.image.load("butterfly.jpg")
temp.rect = temp.image.get_rect()
count = 0
timeToMove = -1
while count < 100:
    #count+= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    sprite.rect = sprite.rect.move(velo)
    curPressed = key.get_pressed()
    if curPressed[pygame.K_ESCAPE]:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    if curPressed[pygame.K_LEFT]:
        velo[0] = -speed
    elif curPressed[pygame.K_RIGHT]:
        velo[0] = speed
    else:
        velo[0] = 0
    if curPressed[pygame.K_UP]:
        velo[1] = -speed
    elif curPressed[pygame.K_DOWN]:
        velo[1] = speed
    else:
        velo[1] = 0
    if (sprite.rect.left < 0 and velo[0] < 0) or (sprite.rect.right > width and velo[0]>0):
        velo[0] = 0
    if (sprite.rect.top < 0 and velo[1] < 0) or (sprite.rect.bottom > height and velo[1]>0):
        velo[1] = 0

    if not temp.alive() and pygame.mouse.get_pressed()[0]:
        mousePos = pygame.mouse.get_pos()
        timeToMove = pygame.time.get_ticks() + 1000
        temp.rect.centerx,temp.rect.centery = mousePos
        everybody.add(temp)
    if timeToMove > 0 and pygame.time.get_ticks() > timeToMove:
        temp.kill()
        timeToMove = -1
        sprite.rect.centerx  = mousePos[0]
        sprite.rect.centery  = mousePos[1]

    collSprites = pygame.sprite.spritecollide(sprite,baddies,False,pygame.sprite.collide_circle)
    if len(collSprites) != 0 :
        sprite.health -= 1
        dx = sprite.rect.centerx-collSprites[0].rect.centerx
        dy = sprite.rect.centery-collSprites[0].rect.centery
        delta = pygame.math.Vector2(dx,dy) #cur distance between sprite centers
        desiredDis = sprite.radius + collSprites[0].radius + 3 # how far away sprite must be to avoid collision
        delta.scale_to_length(desiredDis) 
        sprite.rect.centerx += delta.x
        sprite.rect.centery += delta.y
        print sprite.health
    screen.fill(black)
    everybody.draw(screen)
    #screen.blit(ball,sprite.rect)
    if curPressed[pygame.K_p]:
        pixels = np.array(pygame.surfarray.array2d(screen))
        plt.imshow(pixels)
        plt.show()

    pygame.display.flip()
