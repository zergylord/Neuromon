import pygame
from pygame import key as key
from GameObject import *
from globals import *
def Breeding(monList):
    Breeding.pInd = [0,1] # current parents to breed
    Breeding.cInd = 0 #current parent to update
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
                    child = conceive()
                    print len(monList)
                    par1 = monList[Breeding.pInd[0]]
                    par2 = monList[Breeding.pInd[1]]

                    monList.remove(par1)
                    monList.remove(par2)
                    monList.append(child)
                    print 'you pressed enter'
                elif event.key == pygame.K_1:
                    changeParent(0)
                elif event.key == pygame.K_2:
                    changeParent(1)
                elif event.key == pygame.K_3:
                    changeParent(2)
                elif event.key == pygame.K_4:
                    changeParent(3)
        return monList,quit

    def changeParent(val):
        if Breeding.pInd[1-Breeding.cInd] == val:
            return
        Breeding.pInd[Breeding.cInd] = val 
        Breeding.cInd = 1 - Breeding.cInd
        print Breeding.pInd

    def conceive():
        ''' merge the stats and Moves of the parents
            they die, but a new Neuromon is birthed
            currently returns the first parent as the child
        '''
        moveList = []
        for i in range(6):
            move = monList[Breeding.pInd[np.random.randint(2)]].move[i]
            if not move == None:
                moveList.append(move)
        return VarMon(moveList,monList[Breeding.pInd[0]].imageFileName)
    #main excution f
    quit = False

    font = pygame.freetype.SysFont('',18)
    screen = pygame.display.get_surface()
    background = pygame.image.load("floor.jpg").convert()
    background = pygame.transform.scale(background,size)
    while not quit:
        monList,quit = step()

