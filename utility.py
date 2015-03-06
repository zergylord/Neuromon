import pygame
def LoadImage(filename,size = None):
    img = pygame.image.load(filename)
    if not size == None:
        img = pygame.transform.scale(img,size)
    backColor = img.get_at((0,0))
    img.set_colorkey(backColor)
    return img,img.get_rect()
