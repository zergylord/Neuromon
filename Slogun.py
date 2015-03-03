import pygame.key as key
import sys,pygame
import numpy as np
from GameObject import *
from operator import *
from globals import *

class Slogun(Mon):
    '''Move fast, shoot slow'''
    speed = 200.0/fps #pixels per second
    def __init__(self,iType=1):
        super(Slogun,self).__init__(iType)
        self.setupImage('eye3.jpg')
        self.timeToShoot = -1
        self.heading = [1,0]


    def start(self,world):
        if self.iType == 0:
            pass
        elif self.iType == 1:
            self.foe = world.players.difference(set([self])).pop()
        elif self.iType == 2:
            self.action = [1,1,1,1]
        else:
            raise ValueError("Not a valid player type!")
    def getInput(self,world):
        '''
            returns:
            velo tuple in (-1,0,1)
            shoot bool
        '''
        if self.iType == 0:
            velo = [0,0]
            curPressed = key.get_pressed()
            if curPressed[pygame.K_a]:
                velo[0] = -self.speed
            if curPressed[pygame.K_d]:
                velo[0] = self.speed
            if curPressed[pygame.K_w]:
                velo[1] = -self.speed
            if curPressed[pygame.K_s]:
                velo[1] = self.speed
            if curPressed[pygame.K_SPACE]:
                shoot = True
            else:
                shoot = False
        elif self.iType == 1:
            pass
        elif self.iType == 2:
            velo = self.action[0:2]
            shoot = self.action[2]
        else:
            raise ValueError("Not a valid player type!")
        return velo,shoot
    def canShoot(self):
        return pygame.time.get_ticks() > self.timeToShoot
    def step(self,world):
        '''
        deal with movement of body and bullet
        '''
        self.update(world)
        velo, shoot = self.getInput(world)
        'set the heading'
        if velo[0] > 0:
            self.heading = [1,0]
        elif velo[0] < 0:
            self.heading = [-1,0]
        else:
            if velo[1] > 0:
                self.heading = [0,1]
            elif velo[1] < 0:
                self.heading = [0,-1]
        if shoot and self.canShoot():
            bullet = Bullet(map(mul,self.heading,[10,10]),1)
            bullet.image = pygame.Surface([100,100])
            bullet.image.fill(self.tint)
            bullet.rect = bullet.image.get_rect()
            bullet.rect.center = map(add,self.rect.center,map(mul,self.heading,[100,100])) 
            world.bullets.add(bullet)
            world.everybody.add(bullet)
            self.timeToShoot = pygame.time.get_ticks() + 1000

        self.rect = self.rect.move(velo)

