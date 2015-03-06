import sys, pygame
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from Panoptir import *
from Slogun import *
from GameObject import *
from pygame import key as key
from globals import *

from rlglue.environment.Environment import Environment
from rlglue.environment import EnvironmentLoader
from rlglue.types import Observation
from rlglue.types import Action
from rlglue.types import Reward_observation_terminal
class World(Environment):
    def env_init(self):
            return "VERSION RL-Glue-3.0"
    def __init__(self,p1Type,p2Type):
        self.clock = pygame.time.Clock()
        self.killMe = set()
        self.players = set()
        self.bullets = pygame.sprite.Group()
        self.everybody = pygame.sprite.Group()
        #setup players

        p1 = Panoptir(p1Type)
        p1.rect.centerx = 500
        p1.rect.centery = 500
        self.everybody.add(p1)
        self.players.add(p1)
        if p1Type == 2:
            self.agent = p1

        p2 = Panoptir(p2Type)
        p2.rect.centerx = 500
        self.everybody.add(p2)
        self.players.add(p2)
        if p2Type == 2:
            self.agent = p2

        self.baddies = pygame.sprite.Group()
        enemy = pygame.sprite.Sprite()
        enemy.image = pygame.image.load("butterfly.jpg")
        enemy.rect = enemy.image.get_rect()
        enemy.rect = enemy.rect.move([300,300])
        enemy.radius = enemy.rect.height/2
        #self.baddies.add(enemy)
        #self.everybody.add(enemy)

        self.effects = pygame.sprite.Group()

        self.screen = pygame.display.set_mode(size)#,pygame.FULLSCREEN)
        self.background = pygame.image.load("floor.jpg")
        self.background = pygame.transform.scale(self.background,size)
    def start(self):
        for p in self.players:
            p.start(self)
    def env_start(self):
        self.start()
        returnObs=Observation()
        returnObs.intArray=[1]
        return returnObs
    def step(self):
        '''
        single step of logic and rendering, currently called 60 times per second
        '''
        self.clock.tick(fps)
        print self.clock.get_fps()
        for p in self.players:
            p.step(self)
            if (p.rect.left < 0 and p.velo[0] < 0) or (p.rect.right > width and p.velo[0]>0):
                p.velo[0] = 0
            if (p.rect.top < 0 and p.velo[1] < 0) or (p.rect.bottom > height and p.velo[1]>0):
                p.velo[1] = 0
        for b in self.bullets:
            b.step()
            if getattr(b,'bounce',False):
                if (b.rect.left < 0 and b.velo[0] < 0) or (b.rect.right > width and b.velo[0]>0):
                    b.velo[0] *= -1
                if (b.rect.top < 0 and b.velo[1] < 0) or (b.rect.bottom > height and b.velo[1]>0):
                    b.velo[1] *= -1

        self.environmentalActions()
        self.resolveConflicts()
        self.render()
    def environmentalActions(self):
        '''control anything neither player can directly influence
            currently: invisible walls contain players to the field
        '''
        for p in self.players:
            if (p.rect.left < 0 ):
                p.rect.left = 0
            if (p.rect.right > width ):
                p.rect.right = width
            if (p.rect.top < 0):
                p.rect.top = 0 
            if (p.rect.bottom > height):
                p.rect.bottom = height
    def env_step(self,action):
        self.agent.action = action
        self.step()
        pixels = pygame.surfarray.array2d(screen)
        theObs=Observation()
        theObs.intArray=misc.imresize(pixels,(84,84)).flatten().tolist()
        
        returnRO=Reward_observation_terminal()
        returnRO.r=1 #reward goes here
        returnRO.o=theObs
        returnRO.terminal= 0
        
        return returnRO


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
            collSprites = pygame.sprite.spritecollide(p,self.everybody,False,pygame.sprite.collide_rect)
            for c in collSprites:
                if p is c: #sprite always contained in the group
                    continue
                p.damageToTake +=  getattr(c,'damage',0)
                if not getattr(c,'passThrough',True):
                    dx = p.rect.centerx-c.rect.centerx + np.random.rand() -.5
                    dy = p.rect.centery-c.rect.centery + np.random.rand() -.5
                    delta = pygame.math.Vector2(dx,dy) #cur distance between sprite centers
                    desiredDis = p.radius + c.radius + 3 # how far away sprite must be to avoid collision
                    delta.scale_to_length(desiredDis) 
                    p.rect.centerx += delta.x
                    p.rect.centery += delta.y
                if getattr(c,'breakable',False):
                    c.deathAnimation(self)
                    self.killMe.add(c)

                #print p.health
            if p.health < 0:
                self.killMe.add(p)
    def resolveEffects(self):
        'handle spell effects, and other time dependent game state'
        curTime = pygame.time.get_ticks()
        for e in self.effects:
            if curTime > e.killTime:
                self.killMe.add(e)

    def resolveDeath(self):
        'handle the removal of sprites and other objects from the game world'
        for k in self.killMe:
            if k in self.players:
                self.players.remove(k)
            k.kill()
        self.killMe.clear()
    def render(self):
        'was done in main'
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        curPressed = key.get_pressed()
        if curPressed[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        if curPressed[pygame.K_p]:
            pixels = np.array(pygame.surfarray.array2d(screen))
            plt.imshow(pixels)
            plt.show()
        self.screen.blit(background,[0,0])
        self.everybody.draw(self.screen)
        self.effects.draw(self.screen)
        pygame.display.flip()
if __name__=="__main__":
    pygame.init()
    if len(sys.argv) > 1:
        useGlue = (sys.argv[1] == 'True')
    else:
        useGlue = False
    black = 0,0,0
    screen = pygame.display.set_mode(size)#,pygame.FULLSCREEN)
    background = pygame.image.load("floor.jpg")
    background = pygame.transform.scale(background,size)
    count = 0
    if len(sys.argv) > 2:
        p1Type = int(sys.argv[2])
    else:
        p1Type = 0
    if len(sys.argv) > 3:
        p2Type = int(sys.argv[3])
    else:
        p2Type = 1
    if useGlue:
        EnvironmentLoader.loadEnvironment(World(p1Type,2))
    else:
        world = World(p1Type,p2Type)
        world.start()
        while True:
            world.step()
