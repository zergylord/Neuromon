'''
TODO: use self.params dict exclusively, getting rid of individual parameter attributes
'''
from globals import *
from GameObject import *
from utility import *
from operator import *
import pygame
import pygame.key as key
import numpy as np
import inspect
class Move(object):
    @classmethod
    def _sample(cls,param):
        return np.random.normal(cls._pMean[param],cls._pStd[param])
    def _paramGen(self):
        for p in self.__class__.paramList:
            self.param[p] = self.__class__._sample(p)
    def __init__(self):
        ''' setup anything not tied to a specfic Mon
            e.g. hyperparameters
        '''
        self.param = dict()
        self._paramGen()
    @staticmethod
    def name():
        return 'Move'
    def botStep(self,mon,foe,world):
        pass
    def bind(self,mon):
        ''' call to bind to an inited Mon'''
        pass
    def handleMove(self,mon,world):
        pass
    def getHumanInput(self):
        pass
    def getInput(self,mon):
        if mon.iType == 0:
            ret = self.getHumanInput()
        elif mon.iType == 1 or mon.iType == 2:
            ret = mon.botAction[self.slot]
        else:
            raise ValueError("Not a valid player type!")
        return ret
    def kill(self):
        pass
class SharpWalk(Move):
    '''
        speed: pixels per second movement
    '''
    numActions = 2 
    slot = LEGS
    paramList = ['speed']
    _pMean = {'speed':100}
    _pStd = {'speed':20}
    @staticmethod
    def name():
        return 'Sharp Walk'
    def __init__(self):
        super(SharpWalk,self).__init__()
    def bind(self,mon):
        pass
    def handleMove(self,mon,world):
        velo = self.getInput(mon)
        'set the heading'
        if velo[0] > 0:
            mon.setHeading([1,0])
        elif velo[0] < 0:
            mon.setHeading([-1,0])
        else:
            if velo[1] > 0:
                mon.setHeading([0,1])
            elif velo[1] < 0:
                mon.setHeading([0,-1])
        mon.rect = mon.rect.move(velo)
        mon.velo = velo #just for the world to know about
    def getHumanInput(self):
        '''
            returns:
            velo tuple in (-1,0,1)
        '''
        velo = [0,0]
        curPressed = key.get_pressed()
        if curPressed[pygame.K_LEFT]:
            velo[0] = -self.param['speed']/fps 
        if curPressed[pygame.K_RIGHT]:
            velo[0] = self.param['speed']/fps 
        if curPressed[pygame.K_UP]:
            velo[1] = -self.param['speed']/fps 
        if curPressed[pygame.K_DOWN]:
            velo[1] = self.param['speed']/fps 
        return velo
class Shark(Move):
    '''
        You move or you die.
        Movement grants health
        you take damage while staying still
    '''
    slot = SKIN
    paramList = ['dps','heal','smallPen']
    _pMean = {'dps':1,'heal':30,'smallPen':1}
    _pStd = {'dps':.1,'heal':3,'smallPen':.1}
    @staticmethod
    def name():
        return 'Shark Skin'
    def __init__(self):
        '''
        dps: damage always taken
        heal: healing per 'unit' of movement
        smallPen: penalty to small movements e.g. 4 basically requires moving maxDist
        '''
        super(Shark,self).__init__()
        self.maxDis = float(pow(np.linalg.norm(size),self.param['smallPen']))
    def bind(self,mon):
        self.prevPos = mon.rect.center
    def handleMove(self,mon,world):
        curPos = mon.rect.center
        moveDis = pow(np.linalg.norm(np.subtract(curPos,self.prevPos)),self.param['smallPen'])/self.maxDis #% of dis squared
        mon.damageToTake += (moveDis*-self.param['heal'] + self.param['dps']/fps)
        self.prevPos = curPos
class Dig(Move):
    '''
    baseChargeup: time from click until move in ms
    distChargeup: additional chargeup time in ms due to distance-to-travel
    baseCooldown: time required between finishing one move and starting another
    cancelCooldown: cooldown when hole destoryed before movement

    '''
    slot = ARMS
    paramList = ['baseChargeup','distChargeup','baseCooldown','cancelCooldown']
    _pMean = {'baseChargeup':100,'distChargeup':5000,'baseCooldown':100,'cancelCooldown':1000}
    _pStd = {'baseChargeup':10,'distChargeup':500,'baseCooldown':10,'cancelCooldown':100}
    @staticmethod
    def name():
        return 'Dig Tunnel'
    def __init__(self):
        super(Dig,self).__init__()


        self.hole = FragileObject()
        self.hole.image,self.hole.rect = LoadImage('hole2.png',[100,100]) 
        self.hole.radius = self.hole.rect.height/2

        self.chargeup = -1
        self.cooldown = 0
    def bind(self,mon):
        pass
    def botStep(self,mon,foe,world):
        move = True
        coin = np.random.randint(2)
        if coin == 0:
            x = np.random.randint(1,width)
            y = foe.rect.centery
        else:
            x = foe.rect.centerx
            y = np.random.randint(1,height)
        moveTo = [x,y]
        return [move,moveTo]

    def handleMove(self,mon,world):
        #check for movement events
        move,mousePos = self.getInput(mon)
        if not self.hole.alive():
            if self.chargeup > 0: #hole died before movement, cancel movement
                self.chargeup = -1
                self.cooldown = pygame.time.get_ticks() + self.param['cancelCooldown'] #can't move again for a second
            elif move and pygame.time.get_ticks() > self.cooldown: #start movement
                moveDis = np.linalg.norm(np.subtract(mousePos,mon.rect.center))
                self.chargeup = pygame.time.get_ticks() + self.param['baseChargeup'] + self.param['distChargeup']*(moveDis/width)
                self.hole.rect.centerx,self.hole.rect.centery = mousePos
                world.everybody.add(self.hole)
        if self.chargeup > 0 and pygame.time.get_ticks() > self.chargeup: #complete movement
            mon.rect.centerx  = self.hole.rect.centerx
            mon.rect.centery  = self.hole.rect.centery
            self.hole.kill()
            self.chargeup = -1
            self.cooldown = pygame.time.get_ticks() + self.param['baseCooldown'] #small delay between moves
    def getHumanInput(self):
        '''
            returns:
            move bool
            mousePos pixel-space tuple

        '''
        move = pygame.mouse.get_pressed()[0]
        return move,pygame.mouse.get_pos()
    def kill(self):
        self.hole.kill()
class BounceShot(Move):
    slot = ARMS
    paramList = ['baseCooldown','size','damage','speed']
    _pMean = {'baseCooldown':1000,'size':100,'damage':1,'speed':10}
    _pStd = {'baseCooldown':100,'size':50,'damage':.5,'speed':5}
    @staticmethod
    def name():
        return 'Bounce Blast'
    def __init__(self):
        super(BounceShot,self).__init__()
        self.cooldown = -1
    def bind(self,mon):
        pass
    def canShoot(self):
        return pygame.time.get_ticks() > self.cooldown
    def handleMove(self,mon,world):
        shoot = self.getInput(mon)
        if shoot and self.canShoot():
            bullet = Bullet(map(mul,mon.heading,[self.param['speed'],self.param['speed']]),self.param['damage'])
            pixels = max(10,int(self.param['size']))
            bSize = [pixels,pixels]
            bullet.image,bullet.rect = LoadImage('energy-ball.jpg',bSize)
            halfHead = map(mul,mon.heading,[.5,.5])
            offset = map(mul,halfHead,mon.rect.size)
            offset = map(add,offset,map(mul,halfHead,bSize))
            bullet.rect.center = map(add,mon.rect.center,offset) 
            world.bullets.add(bullet)
            world.everybody.add(bullet)
            self.cooldown = pygame.time.get_ticks() + self.param['baseCooldown']
    def getHumanInput(self):
        '''
            returns:
            shoot bool
        '''
        curPressed = key.get_pressed()
        if curPressed[pygame.K_SPACE]:
            shoot = True
        else:
            shoot = False
        return shoot
class Beam(Move):
    beamDuration = 1000
    horBeamImage = pygame.Surface([300,50])
    horBeamImage.fill([255,20,70])
    vertBeamImage = pygame.Surface([50,300])
    vertBeamImage.fill([255,20,70])
    slot = MOUTH
    paramList = ['duration','damage']
    _pMean = {'duration':1000,'damage':5}
    _pStd = {'duration':500,'damage':2}
    @staticmethod
    def name():
        return 'Beam'
    def __init__(self):
        super(Beam,self).__init__()
        self.beam = pygame.sprite.Sprite()
        self.beam.image = self.horBeamImage 
        self.beam.rect = self.beam.image.get_rect()
        self.beam.radius = self.beam.rect.height/2
    def bind(self,mon):
        self.beam.horOffset = self.beam.rect.width/2 + mon.rect.width/2 + 1
        self.beam.vertOffset = self.beam.rect.width/2 + mon.rect.height/2 + 1

    def botStep(self,mon,foe,world):
        horDiff = foe.rect.centerx - mon.rect.centerx
        vertDiff = foe.rect.centery - mon.rect.centery
        move = False
        moveTo = []
        pew = [0,0]
        if np.abs(vertDiff) < 20 and np.abs(horDiff) < self.horBeamImage.get_width():
           pew[0] = np.sign(horDiff)
        elif np.abs(horDiff) < 20 and np.abs(vertDiff) < self.horBeamImage.get_width():
           pew[1] = np.sign(vertDiff)
        return pew

    def handleMove(self,mon,world):
        '''the only externally called method. Called every step and takes care of everything (input, resolution)'''
        pew = self.getInput(mon)
        chargeupVals = mon.getMoveProp('chargeup')
        if self.beam.alive():
            if pygame.time.get_ticks() > self.beamCutoffTime:
                self.beam.kill()
        elif (chargeupVals == [] or map(lambda x: x<0,chargeupVals) ) and (pew[0] != 0 or pew[1] !=0): #if attack command sent and not mid-move
                if pew[0] != 0:
                    self.beam.image = self.horBeamImage
                else:
                    self.beam.image = self.vertBeamImage
                self.beam.rect = self.beam.image.get_rect()
                self.beam.rect.centerx  = mon.rect.centerx + pew[0]*self.beam.horOffset
                self.beam.rect.centery  = mon.rect.centery + pew[1]*self.beam.vertOffset
                self.beam.damage = self.param['damage']/(fps*self.param['duration']/1000.0)
                self.beam.passThrough = True
                world.everybody.add(self.beam)
                self.beamCutoffTime = pygame.time.get_ticks() + self.param['duration']
                ' pause skill in progress and delay initing new skills'
                chargeupVals = map(lambda x,y: (x>0)*max(x,y),chargeupVals,len(chargeupVals)*[self.beamCutoffTime])
                cooldownVals = mon.getMoveProp('cooldown')
                cooldownVals = map(lambda x,y: (x>0)*max(x,y),cooldownVals,len(cooldownVals)*[self.beamCutoffTime])
    def getHumanInput(self):
        '''
            returns:
            pew one-hot tuple

        '''
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
        return pew
    def kill(self):
        self.beam.kill()
