import pygame.key as key
import sys,pygame
import numpy as np
from GameObject import *
from globals import *
from utility import *
from Bot import *
from Attack import *
from Move import *


class Panoptir(Mon):
    'first monster type'

    def __init__(self, iType=1):
        super(Panoptir,self).__init__(iType)
        self.setupImage('eye.jpg')
        self.attack = Beam(self)
        self.move = Dig(self)
    def start(self,world):
        if self.iType == 0:
            pass
        elif self.iType == 1:
            self.bot = BeamDig(self,world)
        elif self.iType == 2:
            self.action = [1,1,0,1,1]
        else:
            raise ValueError("Not a valid player type!")








