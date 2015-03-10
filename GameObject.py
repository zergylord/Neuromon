import pygame
import numpy as np
from utility import *
'''Mixins'''
class Living(object):
    ''' remember to call setup() method! Not in init due to or'''
    def __init__(self):
        super(Living,self).__init__()
    def setupHealthBar(self):
        '''must be called after sprite has been placed'''
        self.healthBar = self.image.subsurface(pygame.Rect(self.rect.top,self.rect.left,self.rect.width,10))
        self.healthBar.fill([1,255,1])
    def updateHealthBar(self):
        ''' healthbar damage viz'''
        self.healthBar.fill([255,1,1])
        r = self.healthBar.get_rect()
        self.healthBar.fill([1,255,1],pygame.Rect(r.top,r.left,r.width*(self.health/10.0),r.height))

class Dying(object):
    def __init__(self):
        super(Dying,self).__init__()
    def deathAnimation(self,world):
        ''' placeholder death animation
            should be a method, but isn't since
            the parent is a Sprite
            Also needs a timer and a kill
        '''
        boom = pygame.sprite.Sprite()
        boom.image,_ = LoadImage('explosion.png',[75,75])
        boom.rect = self.rect.copy()
        boom.killTime = pygame.time.get_ticks() + 1000 #1 second duration
        world.effects.add(boom)
''' Game Object Heirarchy'''
class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super(GameObject,self).__init__()
class FragileObject(GameObject,Dying):
    def __init__(self):
        super(GameObject,self).__init__()
        self.breakable = True
class Bullet(FragileObject):
    def __init__(self,velo,damage):
        super(Bullet,self).__init__()
        self.velo = velo
        self.damage = damage
        self.bounce = True
    def step(self):
        self.rect = self.rect.move(self.velo)

class Mon(GameObject,Living,Dying):
    def __init__(self,iType):
        super(Mon,self).__init__()
        self.passThrough = False
        self.damageToTake = 0
        self.tint = [50,20,iType*127,50]
        self.health = 10
        self.iType = iType
        self.heading = [1,0] #which cardinal direction you face
        self.velo = [0,0]
    def setupImage(self,filename):
        self.image = pygame.image.load(filename).convert()
        self.image = pygame.transform.scale(self.image,[75,75])
        self.image.fill(self.tint,None,pygame.BLEND_ADD)
        backColor = self.image.get_at((0,0))
        self.image.set_colorkey(backColor)
        self.rect = self.image.get_rect()
        self.radius = self.rect.height/2
        self.setupHealthBar()
    def update(self,world):
        '''
            handles changes in state and there effects
            e.g. health change leads to new tint
        '''
        if self.damageToTake != 0:
            self.health = np.min([10,self.health-self.damageToTake])
            self.damageToTake = 0
            self.updateHealthBar()
            ''' tint style damage viz'''
            #self.image.fill(self.tint,None,pygame.BLEND_SUB)
            #self.tint[0] = int(np.max([0,np.min([(1.0-self.health/10.0)*255,255])]))
            #self.image.fill(self.tint,None,pygame.BLEND_ADD)
            #backColor = self.image.get_at((0,0))
            #self.image.set_colorkey(backColor)
    def step(self,world):
        '''
        update health, movement, and attack
        '''
        self.update(world)
        if self.iType == 1:
            self.botAction = self.bot.step(self,world)
        for m in self.move:
            if m == None:
                continue
            m.handleMove(self,world)
        #self.attack.handleAttack(self,world)
    def kill(self):
        '''remove any child objects'''
        for m in self.move:
            if m is None:
                continue
            m.kill()
class VarMon(Mon):
    def __init__(self,moveList,imageFileName,iType=0,bot=None):
        super(VarMon,self).__init__(iType)
        self.setupImage(imageFileName)
        self.move = 6*[None]
        self.chargeup = []
        self.cooldown = []
        for m in moveList:
            if self.move[m.slot] is not None:
                continue
            m.bind(self)
            self.move[m.slot] = m
        self.bot = bot
    def getMoveProp(self,propName):
        ret = []
        for m in self.move:
            if hasattr(m,propName):
                ret.append(m.cooldown)
        return ret
    def setMoveProp(self,propName,vals):
        count = 0
        for m in self.move:
            if hasattr(m,propName):
                m.cooldown = vals[count]
                count += 1

    def start(self,world):
        if self.iType == 0:
            pass
        elif self.iType == 1:
            self.bot = self.bot(self,world)
        elif self.iType == 2:
            self.botAction = [1,1,0,1,1] #TODO:fix this
        else:
            raise ValueError("Not a valid player type!")
      




