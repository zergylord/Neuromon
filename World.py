import sys, pygame
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
from Panoptir import *
from Slogun import *
from Slobeam import *
from GameObject import *
from pygame import key as key
import pygame.freetype
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
        self.font = pygame.freetype.SysFont('',18)
        self.clock = pygame.time.Clock()
        self.killMe = set()
        self.spawnMe = set()
        self.players = set()
        self.bullets = pygame.sprite.Group()
        self.everybody = pygame.sprite.Group()
        #setup players

        p1 = VarMon([SharpWalk(),BounceShot(),Shark(1,8)],'eye2.jpg',p1Type)
        p1.rect.centerx = 500
        p1.rect.centery = 500
        self.everybody.add(p1)
        self.players.add(p1)
        if p1Type == 2:
            self.agent = p1
         
        p2 = VarMon([Dig(),Beam(),Shark(1,10,2)],'eye2.jpg',p2Type,BeamDig)
        p2.rect.centerx = 500
        self.everybody.add(p2)
        self.players.add(p2)
        if p2Type == 2:
            self.agent = p2
        
        self.effects = pygame.sprite.Group()

        self.background = pygame.image.load("floor.jpg").convert()
        self.background = pygame.transform.scale(self.background,size)
        self.portraitBackground = pygame.image.load('border.jpg').convert()
        self.portraitBackground = pygame.transform.scale(self.portraitBackground,[size[0],int(size[1]/3.0)]) 
        man = pygame.image.load('MM6Man.bmp').convert()
        man = pygame.transform.scale(man,[int(size[0]*(1/8.0)),int(size[1]/4.0)])
        screen.blit(self.background,[0,0])
        screen.blit(self.portraitBackground,[0,size[1]])
        screen.blit(man,[0+int(man.get_width()/2.55),size[1]+int(man.get_height()/7.5)])
        pygame.display.update()#the only time portrait area is updated
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
        self.fps = self.clock.get_fps()
        #print self.clock.get_fps()
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
        self.agent.botAction = action
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
            if not p.alive():
                self.spawnMe.add(p)
    def resolveEffects(self):
        'handle spell effects, and other time dependent game state'
        curTime = pygame.time.get_ticks()
        for e in self.effects:
            if curTime > e.killTime:
                self.killMe.add(e)

    def resolveDeath(self):
        'handle the removal of sprites and other objects from the game world'
        for k in self.killMe:
            #if k in self.players:
            #    self.players.remove(k)
            k.kill()
        for p in self.spawnMe:
            print 'respawn!'
            self.players.remove(p)
            if p.iType == 1:
                'bot spawn!'
                bot = BeamDig
            else:
                'human spawn!'
                bot = None
            p = VarMon([Dig(),Beam(),Shark(1,10,2)],'eye2.jpg',p.iType,bot)
            p.rect.centerx = 500
            p.start(self)
            self.everybody.add(p)
            self.players.add(p)
            for play in self.players:
                play.playerChange(self)
        self.killMe.clear()
        self.spawnMe.clear()
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
        screen.blit(self.background,[0,0])
        self.everybody.draw(screen)
        self.effects.draw(screen)
        fpsDisp,_ = self.font.render(str(self.fps),(255,255,255))
        screen.blit(fpsDisp,[0,0])
        pygame.display.update(gameArea)
if __name__=="__main__":
    pygame.init()
    pygame.freetype.init()
    gameArea = pygame.Rect([0,0],size)
    if len(sys.argv) > 1:
        useGlue = (sys.argv[1] == 'True')
    else:
        useGlue = False
    black = 0,0,0
    screen = pygame.display.set_mode([size[0],int(size[1]*(4/3.0))])#,pygame.FULLSCREEN)
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
        while True or count < 300:
            world.step()
            count += 1
