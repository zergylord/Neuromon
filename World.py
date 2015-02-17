import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
from Panoptir import *
from pygame import key as key
from globals import *
class World:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.killMe = set()
        self.players = set()
        self.everybody = pygame.sprite.Group()
        #setup players

        bot = Panoptir(1)
        bot.sprite.rect.centerx = 500
        bot.sprite.rect.centery = 500
        self.everybody.add(bot.sprite)
        self.players.add(bot)

        player = Panoptir(0)
        player.sprite.rect.centerx = 500
        self.everybody.add(player.sprite)
        self.players.add(player)

        self.baddies = pygame.sprite.Group()
        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.image.load("butterfly.jpg")
        enemy.rect = enemy.image.get_rect()
        enemy.rect = enemy.rect.move([300,300])
        enemy.radius = enemy.rect.height/2
        #self.baddies.add(enemy)
        #self.everybody.add(enemy)
    def start(self):
        for p in self.players:
            p.start(self)
    def step(self):
        '''
        single step of logic and rendering, currently called 60 times per second
        '''
        self.clock.tick(fps)
        #print self.clock.get_fps()
        for p in self.players:
            p.step(self)
            if (p.sprite.rect.left < 0 and p.velo[0] < 0) or (p.sprite.rect.right > width and p.velo[0]>0):
                p.velo[0] = 0
            if (p.sprite.rect.top < 0 and p.velo[1] < 0) or (p.sprite.rect.bottom > height and p.velo[1]>0):
                p.velo[1] = 0
        self.environmentalActions()
        self.resolveConflicts()
        self.render()
    def environmentalActions(self):
        '''control anything neither player can directly influence
            currently: invisible walls contain players to the field
        '''
        for p in self.players:
            if (p.sprite.rect.left < 0 ):
                p.sprite.rect.left = 0
            if (p.sprite.rect.right > width ):
                p.sprite.rect.right = width
            if (p.sprite.rect.top < 0):
                p.sprite.rect.top = 0 
            if (p.sprite.rect.bottom > height):
                p.sprite.rect.bottom = height


    def resolveConflicts(self):
        'handle conflicts between the results of all state changes' 
        self.resolveCollisions()
        self.resolveEffects()
        self.resolveDeath()
    def resolveCollisions(self):
        '''
        handle collisions between objects
        types of collision handled by dynamic properties
        currently (default):
            damage - how much does collision hurt? (0)
            passThrough - does collision move you? (yes)
                NOTE: COLL MOVE CURRENTLYONLY FOR CIRCLES 
            breakable - does collision kill you? (no)
        NOTE: currently collision only occur between players and stuff. Thus non-player entities can only collide with players and not each other!
        '''
        for p in self.players:
            collSprites = pygame.sprite.spritecollide(p.sprite,self.everybody,False,pygame.sprite.collide_rect)
            for c in collSprites:
                if p.sprite is c: #sprite always contained in the group
                    continue
                p.damageToTake +=  getattr(c,'damage',0)
                if not getattr(c,'passThrough',False):
                    dx = p.sprite.rect.centerx-c.rect.centerx + np.random.rand() -.5
                    dy = p.sprite.rect.centery-c.rect.centery + np.random.rand() -.5
                    delta = pygame.math.Vector2(dx,dy) #cur distance between sprite centers
                    desiredDis = p.sprite.radius + c.radius + 3 # how far away sprite must be to avoid collision
                    delta.scale_to_length(desiredDis) 
                    p.sprite.rect.centerx += delta.x
                    p.sprite.rect.centery += delta.y
                if getattr(c,'breakable',False):
                    self.killMe.add(c)
                #print p.health
            if p.health < 0:
                self.killMe.add(p)
    def resolveEffects(self):
        'handle spell effects, and other time dependent game state'
        pass
    def resolveDeath(self):
        'handle the removal of sprites and other objects from the game world'
        for k in self.killMe:
            if k in self.players:
                self.players.remove(k)
            k.kill()
        self.killMe.clear()
    def render(self):
        'draw Everything'
        pass
