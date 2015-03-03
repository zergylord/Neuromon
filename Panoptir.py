import pygame.key as key
import sys,pygame
import numpy as np
from GameObject import *
from globals import *


class Panoptir(Mon):
    'first monster type'
    beamDuration = 1000
    baseMoveDuration = 100 
    distMoveDuration = 5000 #proportional to distance traveled

    horBeamImage = pygame.Surface([300,50])
    horBeamImage.fill([255,20,70])
    vertBeamImage = pygame.Surface([50,300])
    vertBeamImage.fill([255,20,70])
    def __init__(self, iType=1):
        super(Panoptir,self).__init__(iType)
        self.setupImage('eye.jpg')
        self.beam = pygame.sprite.Sprite()
        self.beam.image = self.horBeamImage 
        self.beam.rect = self.beam.image.get_rect()
        self.beam.horOffset = self.beam.rect.width/2 + self.rect.width/2 + 1
        self.beam.vertOffset = self.beam.rect.width/2 + self.rect.height/2 + 1
        self.beam.radius = self.beam.rect.height/2

        self.temp = FragileObject()
        self.temp.image = pygame.Surface([100,100])
        self.temp.image.fill(self.tint)
        self.temp.rect = self.temp.image.get_rect()
        self.temp.radius = self.temp.rect.height/2

        self.timeToMove = -1
        self.moveCooldown = 0
        self.pew = [0,0]
    def start(self,world):
        if self.iType == 0:
            pass
        elif self.iType == 1:
            self.foe = world.players.difference(set([self])).pop()
        elif self.iType == 2:
            self.action = [1,1,0,1,1]
        else:
            raise ValueError("Not a valid player type!")

    def getInput(self,world):
        '''
            returns:
            move bool
            pew one-hot tuple
            mousePos pixel-space tuple

        '''
        if self.iType == 0:
            move = pygame.mouse.get_pressed()[0]
            pew = [0,0]
            curPressed = key.get_pressed()
            if curPressed[pygame.K_a]:
                pew[0] = -1
            elif curPressed[pygame.K_d]:
                pew[0] = 1
            elif curPressed[pygame.K_w]:
                pew[1] = -1
            elif curPressed[pygame.K_s]:
                pew[1] = 1
            return move,pew,pygame.mouse.get_pos()
        elif self.iType == 1:
            #return False,[0,0],[1,1]
            #move = True
            #pew = [0,0]
            #pew[np.random.randint(2)] = np.random.randint(2)*2 -1 #one dimension will be randomly assigned 1 or -1
            #moveTo = [np.random.randint(1,width),np.random.randint(1,height)]
            horDiff = self.foe.rect.centerx - self.rect.centerx
            vertDiff = self.foe.rect.centery - self.rect.centery
            move = False
            moveTo = []
            pew = [0,0]
            if np.abs(vertDiff) < 20 and np.abs(horDiff) < self.horBeamImage.get_width():
               pew[0] = np.sign(horDiff)
            elif np.abs(horDiff) < 20 and np.abs(vertDiff) < self.horBeamImage.get_width():
               pew[1] = np.sign(vertDiff)
            else:
                move = True
                coin = np.random.randint(2)
                if coin == 0:
                    x = np.random.randint(1,width)
                    y = self.foe.rect.centery
                else:
                    x = self.foe.rect.centerx
                    y = np.random.randint(1,height)
                moveTo = [x,y]
            return move,pew,moveTo
        elif self.iType == 2:
            move = self.action[0]
            pew = self.action[1:3]
            assert 0 in pew
            moveTo = self.action[3:5]
            return move,pew,moveTo
        else:
            raise ValueError("Not a valid player type!")
    def step(self,world):
        '''
            modifies the world object based on the action set of Panoptir. Action selection 
            delegated to getInput()
        '''
        self.update(world)
        move, pew,mousePos = self.getInput(world)
        #check for movement events
        if not self.temp.alive():
            if self.timeToMove > 0: #temp died before movement, cancel movement
                self.timeToMove = -1
                self.moveCooldown = pygame.time.get_ticks() + 1000 #can't move again for a second
            elif move and pygame.time.get_ticks() > self.moveCooldown: #start movement
                moveDis = np.linalg.norm(np.subtract(mousePos,self.rect.center))
                self.timeToMove = pygame.time.get_ticks() + self.baseMoveDuration + self.distMoveDuration*(moveDis/width)
                self.temp.rect.centerx,self.temp.rect.centery = mousePos
                world.everybody.add(self.temp)
            else: #not moving
                self.damageToTake += 1.0/(fps) #penalty not moving
        if self.timeToMove > 0 and pygame.time.get_ticks() > self.timeToMove: #complete movement
            self.rect.centerx  = self.temp.rect.centerx
            self.rect.centery  = self.temp.rect.centery
            self.temp.kill()
            self.timeToMove = -1
            self.moveCooldown = pygame.time.get_ticks() + 100 #small delay between moves
            self.damageToTake += -1 #bonus for completing a move
        #check for attack events
        if self.beam.alive():
            if pygame.time.get_ticks() > self.beamCutoffTime:
                self.beam.kill()
        elif self.timeToMove < 0 and (pew[0] != 0 or pew[1] !=0): #if attack command sent and not mid-move
                if pew[0] != 0:
                    self.beam.image = self.horBeamImage
                else:
                    self.beam.image = self.vertBeamImage
                self.beam.rect = self.beam.image.get_rect()
                self.beam.rect.centerx  = self.rect.centerx + pew[0]*self.beam.horOffset
                self.beam.rect.centery  = self.rect.centery + pew[1]*self.beam.vertOffset
                self.beam.damage = 5.0/(fps*self.beamDuration/1000)
                self.beam.passThrough = True
                world.everybody.add(self.beam)
                self.beamCutoffTime = pygame.time.get_ticks() + self.beamDuration
                if self.timeToMove > 0:
                    self.timeToMove = self.beamCutoffTime #delay move until attack finishes 
                else:
                    self.moveCooldown = self.beamCutoffTime #can't start a move during an attack
    def kill(self):
        self.temp.kill()
        self.beam.kill()







