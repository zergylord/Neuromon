import pygame
'''Mixins'''
class Living(object):
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
        boom.image = pygame.Surface([100,100])
        boom.rect = self.rect.copy()
        boom.image.fill([255,255,255])
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

