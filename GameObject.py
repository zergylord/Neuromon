import pygame
import pickle
import pygame.freetype
import numpy as np
from globals import *
from utility import *
'''Mixins'''
class Living(object):
    ''' remember to call setup() method! Not in init due to or'''
    def __init__(self):
        super(Living,self).__init__()
    def setupHealthBar(self):
        '''must be called after sprite has been placed'''
        self.healthBar = self.frame.subsurface(pygame.Rect(self.rect.top,self.rect.left,self.rect.width,10))
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
        self.fainted = False
        self.passThrough = False
        self.font = pygame.freetype.SysFont('',18) 
        self.textDur = 0
        self.damageToTake = 0
        self.tint = [50,20,iType*127,50]
        self.health = 10
        self.iType = iType
        self.heading = [1,0] #which cardinal direction you face
        self.velo = [0,0]
        self.rotImages = 4*[None]
        self.frame = pygame.surface.Surface([250,250])
        self.frame.set_colorkey(self.frame.get_at((0,0)))
    def setupImage(self,filename):
        self.image = pygame.image.load(filename).convert()
        self.image = pygame.transform.scale(self.image,[125,75])
        self.image.fill(self.tint,None,pygame.BLEND_ADD)
        backColor = self.image.get_at((0,0))
        self.image.set_colorkey(backColor)
        self.rect = self.image.get_rect()
        self.radius = self.rect.height/2
        self.setupHealthBar()
        self.rotImages[0] = self.image
        self.rotImages[1] = pygame.transform.rotate(self.image,2*90)
        self.rotImages[2] = pygame.transform.rotate(self.image,3*90)
        self.rotImages[3] = pygame.transform.rotate(self.image,90)
    def setHeading(self,head):
        self.heading = head
        pos = self.rect.center
        if head[0] == 1:
            self.image = self.rotImages[0]
        elif head[0] == -1:
            self.image = self.rotImages[1]
        elif head[1] == 1:
            self.image = self.rotImages[2]
        elif head[1] == -1:
            self.image = self.rotImages[3]
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self,world):
        '''
            handles changes in state and there effects
            e.g. health change leads to new tint
        '''
        if self.damageToTake != 0:
            self.health = np.min([10,self.health-self.damageToTake])
            self.updateHealthBar()
            if self.damageToTake > 1:
                self.textSurf,_ = self.font.render(str(self.damageToTake),[255,255,255])
                self.textDur = 1*fps
            if self.textDur > 0:
                self.image.blit(self.textSurf,[0,0])
                self.textDur -= 1
            self.damageToTake = 0
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
        for m in self.move.viewvalues():
            m.handleMove(self,world)
        #self.attack.handleAttack(self,world)
    def kill(self):
        '''remove any child objects'''
        for m in self.move.viewvalues():
            m.kill()
        super(Mon,self).kill()
    def playerChange(self,world):
        '''
        handles changes the state of the mon when
        the mons in play change
        '''
        if self.iType == 1:
            self.bot.pickFoe(self,world)
class VarMon(Mon):
    def __init__(self,moveList,imageFileName,iType=0,bot=None):
        super(VarMon,self).__init__(iType)
        self.imageFileName = imageFileName
        self.setupImage(imageFileName)
        self.move = dict()
        self.chargeup = []
        self.cooldown = []
        for m in moveList:
            if self.move.get(m.slot) is not None:
                continue
            m.bind(self)
            self.move[m.slot] = m
        self.bot = bot
    def getMoveProp(self,propName):
        ret = []
        for m in self.move.viewvalues():
            if hasattr(m,propName):
                ret.append(getattr(m,propName))
        return ret
    def setMoveProp(self,propName,vals):
        count = 0
        for m in self.move.viewvalues():
            if hasattr(m,propName):
                setattr(m,propName,vals[count])
                count += 1
    def save(self,f):
        print 'saving'
        moveSlots = []
        moveClasses = []
        moveParams = []
        for m in self.move.viewvalues():
            moveSlots.append(m.slot)
            moveClasses.append(m.__class__)
            moveParams.append(m.param)

        pickle.dump((moveSlots,moveClasses,moveParams),f)
    '''
    def load(self):
        print 'loading mon params'
        f = open( "save.p", "rb" ) 
        _,_,moveParams = pickle.load(f)
        ind = 0
        for m in self.move.viewvalues():
            m.param = moveParams[ind]
            ind += 1
    '''
    def start(self,world):
        if self.iType == 0:
            pass
        elif self.iType == 1:
            self.bot = self.bot(self,world)
        elif self.iType == 2:
            self.botAction = [1,1,0,1,1] #TODO:fix this
        else:
            raise ValueError("Not a valid player type!")
      




