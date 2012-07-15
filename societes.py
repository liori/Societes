#!/usr/bin/python
# -*- coding:utf-8 -*-

import pygame, sys
from pygame.locals import *
import map1

#---COLORS-------------------------------------------------------------

#              R   G    B

WHITE =     ( 255, 255, 255)
BLACK =     (   0,   0,   0)
BLUE =      (   0,   0, 255)
GREEN =     (   0, 255,   0)
RED =       ( 255,   0,   0)
YELLOW =    ( 255, 250,  60)
ORANGE =    ( 255, 150,  30)
BROWN =     ( 150,  50,   0)

INVISIBLE = (   0,   0,   0,   0)


#----------------------------------------------------------------------

# These variables won’t change.

FPS = 30

FONT = 'freesansbold.ttf'
FONTSIZE = 16

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'


# These are the blocks sizes. They are in the configuration file “societes.conf”.
# TOLEARN: ConfigParser
conf = open('societes.conf', 'r')

conf.seek(98, 0)
BLOCKSIZEx = int(conf.read(3))
conf.seek(124, 0)
BLOCKSIZEy = int(conf.read(3))

conf.close()

#---DRAWING THE SCREEN-----------------------------------------------

SCREENSIZEx = 1000
SCREENSIZEy = 600

INTERFACESIZEx = SCREENSIZEx
INTERFACESIZEy = 100

OUTTERFINISHBUTTONSIZE = 60
OUTTERFINISHBUTTONPOSx = 920
OUTTERFINISHBUTTONPOSy = SCREENSIZEy - (OUTTERFINISHBUTTONSIZE + 20)

INNERFINISHBUTTONSIZE = OUTTERFINISHBUTTONSIZE / 2
INNERFINISHBUTTONPOSx = OUTTERFINISHBUTTONPOSx + (OUTTERFINISHBUTTONSIZE / 4)
INNERFINISHBUTTONPOSy = OUTTERFINISHBUTTONPOSy + (OUTTERFINISHBUTTONSIZE / 4)

POPTEXTRIGHT = SCREENSIZEx - 50
POPTEXTTOP = 30



#---COLORING-------------------------------------------------------------

BGCOLOR = BLACK

INTERFACEZONECOLOR = ORANGE

OUTTERFINISHBUTTONCOLOR = BROWN
INNERFINISHBUTTONCOLOR = RED


#---PLACES----------------------------------------------------------

WATER = BLUE
LAND = GREEN
YOU = RED
THE_OTHER = YELLOW

#----------------------------------------------------------------------

pygame.init()

#--MAIN-----------------------------------------------------------

def main():
    global FPSCLOCK, DISPLAYSURF, ALPHADISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    
    mousex = 0
    mousey = 0
    
    fontObj = pygame.font.Font(FONT, FONTSIZE)
    
    # What’s the map?
    theMap = map1.createMap()
    
    # Calculate stuff about the faction
    pop = calcFaction(theMap)
    
    # How big is it?
    NUMBERBLOCKSx, NUMBERBLOCKSy = countMap(theMap)
    
    # Sanity check: are all the columns equal? Otherwise there is a problem in the code, at getColor in drawMap. Allowing for columns to be unequal would complicate a lot the code, but I could try to do it, some day.
    for other_column in theMap[1:]:
        assert len(other_column) == len(theMap[0]), 'The columns aren’t equal.'
    
    # Make the screen.
    DISPLAYSURF = pygame.display.set_mode((SCREENSIZEx, SCREENSIZEy))
    ALPHADISPLAYSURF = DISPLAYSURF.convert_alpha()
    Wtf = ((BLOCKSIZEx * (NUMBERBLOCKSx)), (BLOCKSIZEy * (NUMBERBLOCKSy + INTERFACESIZEy)))
    pygame.display.set_caption('Sociétés')
    
    # Draw the map. It also takes note of the position of the map at the moment.
    drawMap(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy)
    mapPosChangex, mapPosChangey = 0, 0 # The inital map position
    slideTo = False # As of now, the map didn’t slide.
    
    mainLoop(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy, mousex, mousey, pop, fontObj, mapPosChangex, mapPosChangey, slideTo)


#---MAIN LOOP-----------------------------------------------------

def mainLoop(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy, mousex, mousey, pop, fontObj, mapPosChangex, mapPosChangey, slideTo):
    while True: # main game loop
        DISPLAYSURF.fill(BGCOLOR)
        mouseClicked = False 
        
        # The map sliding.
        if slideTo:
            if slideTo == UP:
                mapPosChangey = mapPosChangey - 1
            elif slideTo == DOWN:
                mapPosChangey = mapPosChangey + 1
            elif slideTo == LEFT:
                mapPosChangex = mapPosChangex - 1
            elif slideTo == RIGHT:
                mapPosChangex = mapPosChangex + 1
        slideTo = False
        
        updateMap(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy, mapPosChangex, mapPosChangey)


        # The map has to be smaller than the screen + the interface.
        assert NUMBERBLOCKSx * BLOCKSIZEx < 10001 and NUMBERBLOCKSy * BLOCKSIZEy < 6001, 'La carte est trop grande. La hauteur doit être moins grande que 10001 pixels et la largeur doit être moins grande que 6001 pixels.'
        
        
        # Draw the interface.
        drawInterface(fontObj, pop)
        
        
        # What happens?
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    slideTo = LEFT
                elif event.key == K_RIGHT:
                    slideTo = RIGHT
                elif event.key == K_UP:
                    slideTo = UP
                elif event.key == K_DOWN:
                    slideTo = DOWN
                    
        
        # Where did you click? Was it on a block? What block?
        smth = getSomethingAtPixel(mousex, mousey, NUMBERBLOCKSx, NUMBERBLOCKSy, OUTTERFINISHBUTTONPOSx, OUTTERFINISHBUTTONPOSy, OUTTERFINISHBUTTONSIZE)
        if type(smth) == tuple: # If it was on the map. Then take the x and the y coordinates of the region.
            smthx = smth[0]
            smthy = smth[1]
            if mouseClicked:
                print '{}, {}'.format(smthx, smthy)
        
        if smth == 'finishButtonClick' and mouseClicked:
            pop = finishTurn(pop)
        
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#-------------------------------------------------------------------------


def leftTopCoordsOfBlock(smthx, smthy):
    # Convert map coordinates to pixel coordinates.
    left = smthx * BLOCKSIZEx
    top = smthy * BLOCKSIZEy
    return (left, top)

def getSomethingAtPixel(x, y, NUMBERBLOCKSx, NUMBERBLOCKSy, OUTTERFINISHBUTTONPOSx, OUTTERFINISHBUTTONPOSy, OUTTERFINISHBUTTONSIZE):
    
    for smthx in range(NUMBERBLOCKSx):
        for smthy in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(smthx, smthy)
            blockRect = pygame.Rect(left, top, BLOCKSIZEx, BLOCKSIZEy)
            smth = (smthx, smthy)
            if blockRect.collidepoint(x, y):
                return (smth)
    
    nextButtonRect = pygame.Rect(OUTTERFINISHBUTTONPOSx, OUTTERFINISHBUTTONPOSy, OUTTERFINISHBUTTONSIZE, OUTTERFINISHBUTTONSIZE)
    if nextButtonRect.collidepoint(x, y):
        return ('finishButtonClick')
    
    return (None)





#---MAP------------------------------------------------------

def getColor(theMap, smthx, smthy):
    # color value for x, y spot is stored in TheMap[x][y]['faction'].
    # This is used in drawMap.
    return theMap[smthx][smthy]['faction']

def drawMap(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy):
    # Draws all the blocks.
    # This is used in main.
    for smthx in range(NUMBERBLOCKSx):
        for smthy in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(smthx, smthy) # smthx - 1 MALADE !!!!
            color = getColor(theMap, smthx, smthy)
            pygame.draw.rect(DISPLAYSURF, color, (left, top, BLOCKSIZEx, BLOCKSIZEy))

def countMap(theMap):
    # Count the number of blocks in the map.
    nbCol = len(theMap)
    nbRows = len(theMap[0])
    return nbCol, nbRows

def updateMap(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy, mapPosChangex, mapPosChangey):
    # Update the map after a sliding (moving camera)
    for smthx in range(NUMBERBLOCKSx):
        for smthy in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(smthx + mapPosChangex, smthy + mapPosChangey)
            color = getColor(theMap, smthx, smthy)
            pygame.draw.rect(DISPLAYSURF, color, (left, top, BLOCKSIZEx, BLOCKSIZEy))

#---STRICTLY GAME RELATED STUFF------------------------------

def calcFaction(theMap):
    yourRegions = []
    for col in theMap:
        for region in col:
            if region['faction'] == YOU:
                yourRegions.append(region)
    
    pop = 0
    for region in yourRegions:
        pop = pop + region['pop']
    
    return pop

def finishTurn(pop):
    # Oulah la flexibilité…
    pop = pop * 1.10
    pop = int(round(pop, 0))
    return pop

#----INTERFACE DRAWING--------------

def drawInterface(fontObj, pop):
    # Draw the interface.
    # It’s used in main.
    interfaceZone()
    finishButton()
    someText(fontObj, pop)

def interfaceZone():
    InterfaceRect = pygame.draw.rect(DISPLAYSURF, INTERFACEZONECOLOR, (0, (SCREENSIZEy - INTERFACESIZEy), INTERFACESIZEx, INTERFACESIZEy))

def finishButton():
    OutterFinishButton = pygame.draw.rect(DISPLAYSURF, OUTTERFINISHBUTTONCOLOR, (OUTTERFINISHBUTTONPOSx, OUTTERFINISHBUTTONPOSy, OUTTERFINISHBUTTONSIZE, OUTTERFINISHBUTTONSIZE))
    InnerFinishButton = pygame.draw.rect(DISPLAYSURF, INNERFINISHBUTTONCOLOR, (INNERFINISHBUTTONPOSx, INNERFINISHBUTTONPOSy, INNERFINISHBUTTONSIZE, INNERFINISHBUTTONSIZE))

def someText(fontObj, pop):
    popTextSurface = fontObj.render('Population: {}'.format(pop), True, WHITE, INVISIBLE)
    popTextRect = popTextSurface.get_rect()
    popTextRect.right = POPTEXTRIGHT
    popTextRect.top = POPTEXTTOP
    DISPLAYSURF.blit(popTextSurface, popTextRect)


    
#-----------------------------------------



    
main()
