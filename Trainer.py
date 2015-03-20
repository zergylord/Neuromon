from itertools import count
import pygame
from pygame import key as key
import numpy as np
from globals import *
class Trainer(object):
    number = count()
    world = None
    def __init__(self,human = False):
        self.neuroballs = 3
        self.num = self.number.next()
        self.mon = []
        self.curMon = 0 #index to mon in use
        self.score = 0
        self.keysPressed = 323*[0]
        self.human = human
    def step(self):
        if self.human:
            curPressed = key.get_pressed()
            if not self.keysPressed[pygame.K_c] and curPressed[pygame.K_c]:
                self.catchAttempt()
            self.keysPressed = curPressed
    def setCurMon(self,ind):
        self.curMon = ind
        self.mon[ind].rect.centery = np.random.randint(1,size[1])
        self.mon[ind].rect.centerx = np.random.randint(1,size[0]/2.0)
        self.mon[ind].start(self.world)
        self.world.everybody.add(self.mon[ind])
        self.world.players.add(self.mon[ind])
    def getCurMon(self):
        return self.mon[self.curMon]
    def loseCurMon(self):
        self.getCurMon().kill()
        self.world.players.remove(self.getCurMon())
        self.mon.remove(self.getCurMon())
        if len(self.mon) > 0:
            self.setCurMon(0)
        else:
            print 'player' + str(self.num) + ' is out of neuromon!'
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    def catchAttempt(self):
        otherTrainer = self.world.trainers[1-self.num]
        otherMon = otherTrainer.getCurMon()
        print otherMon
        ' remove mon from board and from other trainer'
        #print otherMon in self.world.everybody
        otherTrainer.loseCurMon()
        ' add mon to this trainer'
        self.mon.append(otherMon)
        print self.world.everybody
        

