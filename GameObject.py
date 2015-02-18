import pygame
class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super(GameObject,self).__init__()
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
