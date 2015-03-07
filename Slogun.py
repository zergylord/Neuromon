import pygame.key as key
import sys,pygame
import numpy as np
from GameObject import *
from operator import *
from globals import *
from utility import *
from Bot import *
from Attack import *
from Move import *

class Slogun(Mon):
    '''Move fast, shoot slow'''
    def __init__(self,iType=1):
        super(Slogun,self).__init__(iType)
        self.setupImage('eye2.jpg')
        self.attack = BounceShot(self)
        self.move = SharpWalk(self)

    def start(self,world):
        if self.iType == 0:
            pass
        elif self.iType == 1:
            ''' no bot written yet'''
            pass
        elif self.iType == 2:
            self.action = [1,1,1,1]
        else:
            raise ValueError("Not a valid player type!")


