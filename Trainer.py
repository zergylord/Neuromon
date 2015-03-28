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
    def newKeyPress(self,curPressed,k):
        '''
        check if button was just pressed
        TODO: move key handling to a utility module
        '''
        return not self.keysPressed[k] and curPressed[k]

    def step(self):
        if self.human:
            curPressed = key.get_pressed()
            if self.newKeyPress(curPressed,pygame.K_c):
                self.catchAttempt()
            if self.newKeyPress(curPressed,pygame.K_1):
                self.switchToMon(0)
            if self.newKeyPress(curPressed,pygame.K_2):
                self.switchToMon(1)
            if self.newKeyPress(curPressed,pygame.K_3):
                self.switchToMon(2)
            if self.newKeyPress(curPressed,pygame.K_4):
                self.setCurMon(3)
                self.switchToMon(3)
            self.keysPressed = curPressed
    def switchToMon(self,ind):
        '''
        When you have a Mon already out, return it to hand
        and put out a different one
        '''
        if ind >= len(self.mon):
            print 'you dont have that many neuromon'
            return
        elif self.curMon == ind:
            print 'switching to the same mon...'
            return
        #remove curMon from play
        self.getCurMon().kill()
        self.world.players.remove(self.getCurMon())
        #switch to new mon
        self.setCurMon(ind)
        #let the other player know about the swap
        self.world.trainers[1-self.num].getCurMon().playerChange(self.world)
        


    def setCurMon(self,ind):
        '''
        Called only when sending out a mon
        and you dont already have one out
        '''
        if ind >= len(self.mon):
            print 'you dont have that many neuromon'
            return
        self.curMon = ind
        self.mon[ind].rect.centery = np.random.randint(1,size[1])
        self.mon[ind].rect.centerx = np.random.randint(1,size[0]/2.0)
        self.mon[ind].start(self.world)
        self.world.everybody.add(self.mon[ind])
        self.world.players.add(self.mon[ind])
    def getCurMon(self):
        return self.mon[self.curMon]
    def getBreedableMon(self):
        '''
        gets all of the mons in Mon that are fit for breeding.
        currently just all mon that aren't the current one, but
        later might include being of age.
        '''
        breedable = self.mon[:] #copy list
        breedable.remove(self.getCurMon())
        return breedable
    def setBreedableMon(self,bMon):
        '''
        edits the Mon list s.t. bMon are the only breedable Mons in it
        '''
        nonBreedable = self.getCurMon()
        self.mon = bMon
        self.mon.insert(self.curMon,nonBreedable)


    def loseCurMon(self):
        '''
        Removes Mon from play and from the Trainers hand
        Returns: LastMonDead? bool
        '''
        self.getCurMon().kill()
        self.world.players.remove(self.getCurMon())
        self.mon.remove(self.getCurMon())
        if len(self.mon) > 0:
            self.setCurMon(0)
            return False
        else:
            print 'player' + str(self.num) + ' is out of neuromon!'
            return True
            #pygame.event.post(pygame.event.Event(pygame.QUIT))
    def catchAttempt(self):
        if len(self.mon) >= 4:
            print 'you already have 4 neuromon!'
            return
        otherTrainer = self.world.trainers[1-self.num]
        otherMon = otherTrainer.getCurMon()
        print otherMon
        ' remove mon from board and from other trainer'
        #print otherMon in self.world.everybody
        lost = otherTrainer.loseCurMon()
        if lost:
            self.world.createEnemyTrainer()
            otherTrainer.getCurMon().start(self.world)
        ' add mon to this trainer'
        otherMon.iType = 0
        self.mon.append(otherMon)
        print self.world.everybody
        

