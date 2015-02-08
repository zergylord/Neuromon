import pygame.key as key
import sys,pygame

class Panoptir:
    'first monster type'
    velo = [0,0] #never used due to Panoptirs movement type
    health = 10
    iType = 0 #0=human,1=bot,2=brain

    beam = pygame.sprite.Sprite()
    beam.image = pygame.image.load("butterfly.jpg")
    beam.rect = beam.image.get_rect()

    temp = pygame.sprite.Sprite()
    temp.image = pygame.image.load("butterfly.jpg")
    temp.rect = temp.image.get_rect()
    timeToMove = -1
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load("butterfly.jpg")
    sprite.rect = sprite.image.get_rect()
    sprite.radius = sprite.rect.height/2
    pew = [0,0]
    def __init__(self, iType=0):
        pass
    def act(self,world):
        curPressed = key.get_pressed()
        #check for movement events
        if not self.temp.alive() and pygame.mouse.get_pressed()[0]:
            mousePos = pygame.mouse.get_pos()
            self.timeToMove = pygame.time.get_ticks() + 1000
            self.temp.rect.centerx,self.temp.rect.centery = mousePos
            world.everybody.add(self.temp)
        if self.timeToMove > 0 and pygame.time.get_ticks() > self.timeToMove:
            self.sprite.rect.centerx  = self.temp.rect.centerx
            self.sprite.rect.centery  = self.temp.rect.centery
            self.temp.kill()
            self.timeToMove = -1
        #check for attack events
        pew = [0,0]
        offset = 100
        if self.beam.alive():
            if pygame.time.get_ticks() > self.beamCutoffTime:
                self.beam.kill()
        else:
            if curPressed[pygame.K_LEFT]:
                pew[0] = -1
            elif curPressed[pygame.K_RIGHT]:
                pew[0] = 1
            elif curPressed[pygame.K_UP]:
                pew[1] = -1
            elif curPressed[pygame.K_DOWN]:
                pew[1] = 1
            if (pew[0] != 0 or pew[1] !=0): #if attack command sent
                self.beam.rect.centerx  = self.sprite.rect.centerx + pew[0]*offset
                self.beam.rect.centery  = self.sprite.rect.centery + pew[1]*offset
                self.beam.damage = 1
                self.beam.passThrough = True
                world.everybody.add(self.beam)
                self.beamCutoffTime = pygame.time.get_ticks() + 1000






