import numpy as np
from globals import *
class Bot(object):
    '''AI controlled agent with direct access to
    game state information
    '''
    def __init__(self,mon,world):
        pass
    def step(self,mon,world):
        '''
        returns list of length 2
        corresponding to the move actions,
        and then the attack actions
        '''
        pass

class VarBot(Bot):
    def __init__(self,mon,world):
        self.pickFoe(mon,world)
    def pickFoe(self,mon,world):
        self.foe = world.players.difference(set([mon])).pop()
    def step(self,mon,world):
        '''
        currently, iteratively perform actions associated
        with each move.
        Later, use randomized priority queue.
        '''
        ret = dict()
        for m in mon.move:
            ret[m] = mon.move[m].botStep(mon,self.foe,world)
        return ret
class BeamDig(Bot):
    def __init__(self,mon,world):
        self.pickFoe(mon,world)
    def pickFoe(self,mon,world):
        self.foe = world.players.difference(set([mon])).pop()
    def step(self,mon,world):
        #return False,[0,0],[1,1]
        #move = True
        #pew = [0,0]
        #pew[np.random.randint(2)] = np.random.randint(2)*2 -1 #one dimension will be randomly assigned 1 or -1
        #moveTo = [np.random.randint(1,width),np.random.randint(1,height)]
        horDiff = self.foe.rect.centerx - mon.rect.centerx
        vertDiff = self.foe.rect.centery - mon.rect.centery
        move = False
        moveTo = []
        pew = [0,0]
        if np.abs(vertDiff) < 20 and np.abs(horDiff) < mon.move[MOUTH].horBeamImage.get_width():
           pew[0] = np.sign(horDiff)
        elif np.abs(horDiff) < 20 and np.abs(vertDiff) < mon.move[MOUTH].horBeamImage.get_width():
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
        ret = dict()
        ret[MOUTH] = pew
        ret[ARMS] = [move,moveTo]
        return ret
