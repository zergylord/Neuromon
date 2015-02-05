import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
from Panoptir import *
from pygame import key as key
from globals import *
class World:
    def __init__(self):
        #setup players
        player = Panoptir()
        self.everybody = pygame.sprite.Group(player.sprite)
        self.players = [player]

        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.image.load("butterfly.jpg")
        enemy.rect = enemy.image.get_rect()
        enemy.rect = enemy.rect.move([300,300])
        self.baddies = pygame.sprite.Group(enemy)
        self.everybody.add(enemy)
    def step(self):
        'single step of logic and rendering'
        for p in self.players:
            p.act(self)
            if (p.sprite.rect.left < 0 and p.velo[0] < 0) or (p.sprite.rect.right > width and p.velo[0]>0):
                p.velo[0] = 0
            if (p.sprite.rect.top < 0 and p.velo[1] < 0) or (p.sprite.rect.bottom > height and p.velo[1]>0):
                p.velo[1] = 0
        self.environmentalActions()
        self.resolveConflicts()
        self.render()
    def environmentalActions(self):
        'control anything neither player can directly influence'
        pass
    def resolveConflicts(self):
        'handle conflicts between the results of all state changes' 
        self.resolveCollisions()
        self.resolveEffects()
        self.resolveDeath()
    def resolveCollisions(self):
        'handle collisions between objects'
        pygame.sprite.spritecollide(self.players[0].sprite,self.baddies,True)
    def resolveEffects(self):
        'handle spell effects, and other time dependent game state'
        pass
    def resolveDeath(self):
        'handle the removal of sprites and other objects from the game world'
        pass
    def render(self):
        'draw Everything'
        pass
