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
    def _setParams(cls,self):
        for p in self.paramNames:
            if getattr(self,p) == None:
                setattr(self,p,cls._paramGen(p))
    @staticmethod
    def _paramGen(paramName):
        ''' should specify how to generate random values for each parameter'''
        pass
    def __init__(self):
        ''' setup anything not tied to a specfic Mon
            e.g. hyperparameters
        '''
        frame,_,_,_,_,_ = inspect.getouterframes(inspect.currentframe())[1]
        args, _, _, _ = inspect.getargvalues(frame)
        self.paramNames = args[1:]
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
    @staticmethod
    def _paramGen(paramName):
        if paramName == 'speed':
            return np.random.normal(200,20)
    def __init__(self,speed = None):
        super(SharpWalk,self).__init__()
        self.speed = speed
        SharpWalk._setParams(self)#parameter setting boilerplate needed for all Moves
        self.speed /= fps #pixels per second
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
            velo[0] = -self.speed
        if curPressed[pygame.K_RIGHT]:
            velo[0] = self.speed
        if curPressed[pygame.K_UP]:
            velo[1] = -self.speed
        if curPressed[pygame.K_DOWN]:
            velo[1] = self.speed
        return velo
class Shark(Move):
    '''
        You move or you die.
        Movement grants health
        you take damage while staying still
    '''
    slot = SKIN
    @staticmethod
    def _paramGen(paramName):
        if paramName == 'dps':
            return np.random.normal(1,.1)
        if paramName == 'heal':
            return np.random.normal(30,3)
        if paramName == 'smallPen':
            return np.random.normal(1,.1)
    def __init__(self,dps = None,heal = None,smallPen = None):
        '''
        dps: damage always taken
        heal: healing per 'unit' of movement
        smallPen: penalty to small movements e.g. 4 basically requires moving maxDist
        '''
        super(Shark,self).__init__()
        self.dps = dps
        self.heal = heal
        self.smallPen = smallPen
        Shark._setParams(self)#parameter setting boilerplate needed for all Moves
        self.maxDis = float(pow(np.linalg.norm(size),self.smallPen))
    def bind(self,mon):
        self.prevPos = mon.rect.center
    def handleMove(self,mon,world):
        curPos = mon.rect.center
        moveDis = pow(np.linalg.norm(np.subtract(curPos,self.prevPos)),self.smallPen)/self.maxDis #% of dis squared
        mon.damageToTake += (moveDis*-self.heal + self.dps/fps)
        self.prevPos = curPos
class Dig(Move):
    '''
    baseChargeup: time from click until move in ms
    distChargeup: additional chargeup time in ms due to distance-to-travel
    baseCooldown: time required between finishing one move and starting another
    cancelCooldown: cooldown when hole destoryed before movement

    '''
    slot = ARMS
    @staticmethod
    def _paramGen(paramName):
        if paramName == 'baseChargeup':
            return np.random.normal(100,10)
        if paramName == 'distChargeup':
            return np.random.normal(5000,500)
        if paramName == 'baseCooldown':
            return np.random.normal(100,10)
        if paramName == 'cancelCooldown':
            return np.random.normal(1000,100)
    def __init__(self,baseChargeup = None,distChargeup = None,baseCooldown = None,cancelCooldown = None):
        super(Dig,self).__init__()
        self.baseChargeup = baseChargeup
        self.distChargeup = distChargeup
        self.baseCooldown = baseCooldown
        self.cancelCooldown = cancelCooldown
        Dig._setParams(self)


        self.hole = FragileObject()
        self.hole.image,self.hole.rect = LoadImage('hole2.png',[100,100]) 
        self.hole.radius = self.hole.rect.height/2

        self.chargeup = -1
        self.cooldown = 0
    def bind(self,mon):
        pass
    def handleMove(self,mon,world):
        #check for movement events
        move,mousePos = self.getInput(mon)
        if not self.hole.alive():
            if self.chargeup > 0: #hole died before movement, cancel movement
                self.chargeup = -1
                self.cooldown = pygame.time.get_ticks() + self.cancelCooldown #can't move again for a second
            elif move and pygame.time.get_ticks() > self.cooldown: #start movement
                moveDis = np.linalg.norm(np.subtract(mousePos,mon.rect.center))
                self.chargeup = pygame.time.get_ticks() + self.baseChargeup + self.distChargeup*(moveDis/width)
                self.hole.rect.centerx,self.hole.rect.centery = mousePos
                world.everybody.add(self.hole)
        if self.chargeup > 0 and pygame.time.get_ticks() > self.chargeup: #complete movement
            mon.rect.centerx  = self.hole.rect.centerx
            mon.rect.centery  = self.hole.rect.centery
            self.hole.kill()
            self.chargeup = -1
            self.cooldown = pygame.time.get_ticks() + self.baseCooldown #small delay between moves
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
    @staticmethod
    def _paramGen(paramName):
        if paramName == 'baseCooldown':
            return np.random.normal(1000,100)
        if paramName == 'size':
            return int(max(10,np.random.normal(100,50)))
        if paramName == 'damage':
            return max(.1,np.random.normal(1,.5))
        if paramName == 'speed':
            return max(0,np.random.normal(10,5))
    def __init__(self,baseCooldown = None, size = None,damage = None, speed = None):
        super(BounceShot,self).__init__()
        self.baseCooldown = baseCooldown
        self.size = size
        self.damage = damage
        self.speed = speed
        BounceShot._setParams(self)
        self.cooldown = -1
    def bind(self,mon):
        pass
    def canShoot(self):
        return pygame.time.get_ticks() > self.cooldown
    def handleMove(self,mon,world):
        shoot = self.getInput(mon)
        if shoot and self.canShoot():
            bullet = Bullet(map(mul,mon.heading,[self.speed,self.speed]),self.damage)
            bSize = [self.size,self.size]
            bullet.image,bullet.rect = LoadImage('energy-ball.jpg',bSize)
            halfHead = map(mul,mon.heading,[.5,.5])
            offset = map(mul,halfHead,mon.rect.size)
            offset = map(add,offset,map(mul,halfHead,bSize))
            bullet.rect.center = map(add,mon.rect.center,offset) 
            world.bullets.add(bullet)
            world.everybody.add(bullet)
            self.cooldown = pygame.time.get_ticks() + self.baseCooldown
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
    @staticmethod
    def _paramGen(paramName):
        if paramName == 'duration':
            return np.random.normal(1000,500)
        if paramName == 'damage': #total damage over full duration
            return max(.1,np.random.normal(5,2))
    def __init__(self,duration = None,damage = None):
        super(Beam,self).__init__()
        self.damage = damage
        self.duration = duration
        Beam._setParams(self)
        print self.duration
        self.beam = pygame.sprite.Sprite()
        self.beam.image = self.horBeamImage 
        self.beam.rect = self.beam.image.get_rect()
        self.beam.radius = self.beam.rect.height/2
    def bind(self,mon):
        self.beam.horOffset = self.beam.rect.width/2 + mon.rect.width/2 + 1
        self.beam.vertOffset = self.beam.rect.width/2 + mon.rect.height/2 + 1

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
                self.beam.damage = self.damage/(fps*self.duration/1000.0)
                self.beam.passThrough = True
                world.everybody.add(self.beam)
                self.beamCutoffTime = pygame.time.get_ticks() + self.duration
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
