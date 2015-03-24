import pygame
from pygame import key as key
from GameObject import *
from globals import *
def Breeding(monList):
    Breeding.pInd = [0,1] # current parents to breed
    Breeding.cInd = 0 #current parent to update
    def step():
        
        #handle input
        curPressed = key.get_pressed()
        quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    quit = True
                elif event.key == pygame.K_RETURN:
                    if len(monList) < 2:
                        print 'need at least 2 breedable mon to have a child!'
                        continue
                    child = conceive()
                    print len(monList)
                    par1 = monList[Breeding.pInd[0]]
                    par2 = monList[Breeding.pInd[1]]

                    monList.remove(par1)
                    monList.remove(par2)
                    monList.append(child)
                    renderMonList()
                    print 'you pressed enter'
                elif event.key == pygame.K_1:
                    changeParent(0)
                elif event.key == pygame.K_2:
                    changeParent(1)
                elif event.key == pygame.K_3:
                    changeParent(2)
                elif event.key == pygame.K_4:
                    changeParent(3)
                elif event.key == pygame.K_0:
                    pygame.display.update()
        return monList,quit

    def changeParent(val):
        if Breeding.pInd[1-Breeding.cInd] == val: #can't be both parents!
            return
        if val >= len(monList):
            return
        Breeding.pInd[Breeding.cInd] = val 
        renderStats(Breeding.cInd,val)
        Breeding.cInd = 1 - Breeding.cInd
        print Breeding.pInd
    def renderStats(slot,ind):
        mon = monList[ind]
        screen.blit(background,[0,0])
        count = 0
        top = 100
        vertSpace = 10
        barLength = 200
        barHeight = 30
        left = slot*(width/2)+barLength
        totalHeight = 0
        for m in mon.move.viewvalues():
            moveText,rect = font.render(m.name(),(255,255,255))
            screen.blit(moveText,[left+5,top+totalHeight+vertSpace])
            totalHeight += rect.height + vertSpace
            for p in m.param:
                pVal = ((m.param[p]-m._pMean[p])/m._pStd[p])*(barLength/3.0) #can display up to 3 std each direction
                if pVal < 0:
                    pVal *= -1
                    neg = 1
                else:
                    neg = 0
                bar = pygame.surface.Surface([pVal, barHeight])
                bar.fill([254*neg+1,254*(1-neg)+1,1])
                pHor = left-pVal*neg
                pVert = top+totalHeight+vertSpace
                screen.blit(bar,[pHor,pVert])
                pText,rect = font.render(p,(125,125,125))
                screen.blit(pText,[pHor+(5+pVal)*(1-neg)-(rect.width+5)*neg,pVert])
                count += 1
                totalHeight += barHeight + vertSpace
        vertBar = pygame.surface.Surface([10,totalHeight])
        screen.blit(vertBar,[left-5,top])
        pygame.display.update(pygame.Rect(left-barLength,top,barLength*2,totalHeight))
    def renderMonList():
        #render GUI
        screen.blit(background,[0,0])
        print str(monList)
        monNameText,rect = font.render(str(monList),(255,255,255))
        screen.blit(monNameText,[0,0])
        pygame.display.update(0,0,width,rect.height) #refresh whole hor section of screen, since don't track max hor size
    def conceive():
        ''' -merge the stats and Moves of the parents
            they die, but a new Neuromon is birthed
            -moves are randomly picked between the two parents
            -move parameters are randomly assigned and then shifted
            towards those of the selected parent (and the other to a lesser degree)
        '''
        moveList = []
        for m in MOVETYPES:
            winningPar = Breeding.pInd[np.random.randint(2)]
            move = monList[winningPar].move.get(m)
            if not move == None:
                newMove = move.__class__()#new instance of class
                for p in newMove.param:
                    newMove.param[p] += .25*(move.param[p] - newMove.param[p])
                    if monList[1-winningPar].move[m] == move:
                        newMove.param[p] += .1*(monList[1-winningPar].move[m].param[p] - newMove.param[p])
                moveList.append(newMove)
        baby = VarMon(moveList,monList[Breeding.pInd[0]].imageFileName)
        #select default parents
        Breeding.pInd[0] = 0
        Breeding.pInd[1] = 1
        return baby
    #main excution f
    quit = False

    font = pygame.freetype.SysFont('',18)
    screen = pygame.display.get_surface()
    background = pygame.image.load("floor.jpg").convert()
    background = pygame.transform.scale(background,size)
    screen.blit(background,[0,0])
    pygame.display.update()
    renderMonList()
    while not quit:
        monList,quit = step()
    return monList

