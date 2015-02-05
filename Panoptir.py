import pygame.key as key
import sys,pygame

class Panoptir:
    'first monster type'
    iType = 0 #0=human,1=bot,2=brain
    temp = pygame.sprite.Sprite()
    temp.image = pygame.image.load("butterfly.jpg")
    temp.rect = temp.image.get_rect()
    timeToMove = -1
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load("butterfly.jpg")
    sprite.rect = sprite.image.get_rect()
    velo = [0,0]
    def __init__(self, iType=0):
        pass
    def act(self,everybody):
        curPressed = key.get_pressed()
        if curPressed[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        if not self.temp.alive() and pygame.mouse.get_pressed()[0]:
            mousePos = pygame.mouse.get_pos()
            self.timeToMove = pygame.time.get_ticks() + 1000
            self.temp.rect.centerx,self.temp.rect.centery = mousePos
            everybody.add(self.temp)
        if self.timeToMove > 0 and pygame.time.get_ticks() > self.timeToMove:
            self.sprite.rect.centerx  = self.temp.rect.centerx
            self.sprite.rect.centery  = self.temp.rect.centery
            self.temp.kill()
            self.timeToMove = -1



