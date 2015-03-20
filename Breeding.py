import pygame
from pygame import key as key
from GameObject import *
from globals import *
def Breeding(monList):
    def step():
        #render GUI
        pygame.display.update()
        screen.blit(background,[0,0])
        screen.blit(pygame.Surface((100,200)),[0,0])
        monNameText,_ = font.render(str(monList),(255,255,255))
        screen.blit(monNameText,[0,0])
        #handle input
        curPressed = key.get_pressed()
        quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    quit = True
                elif event.key == pygame.K_RETURN:
                    child = conceive(pInd)
                    print len(monList)
                    par1 = monList[pInd[0]]
                    par2 = monList[pInd[1]]

                    monList.remove(par1)
                    monList.remove(par2)
                    monList.append(child)
                    print 'you pressed enter'
                elif event.key == pygame.K_1:
                    print 'you pressed 1'
                elif event.key == pygame.K_2:
                    print 'you pressed 2'
                elif event.key == pygame.K_3:
                    print 'you pressed 3'
                elif event.key == pygame.K_4:
                    print 'you pressed 4'
        return monList,quit

    def conceive(pInd):
        ''' merge the stats and Moves of the parents
            they die, but a new Neuromon is birthed
            currently returns the first parent as the child
        '''

        return monList[pInd[0]]
    #main excution f
    quit = False
    pInd = [0,1]
    font = pygame.freetype.SysFont('',18)
    screen = pygame.display.get_surface()
    background = pygame.image.load("floor.jpg").convert()
    background = pygame.transform.scale(background,size)
    while not quit:
        print len(monList)
        monList,quit = step()

