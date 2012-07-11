#!/usr/bin/python
# -*- coding:utf-8 -*-

import pygame, sys
from pygame.locals import *
from map1 import *

#---COLORS-------------------------------------------------------------

#           R   G    B

WHITE =  ( 255, 255, 255)
BLACK =  (   0,   0,   0)
BLUE =   (   0,   0, 255)
GREEN =  (   0, 255,   0)
RED =    ( 255,   0,   0)
YELLOW = ( 255, 250,  60)
ORANGE = ( 255, 150,  30)
BROWN =  ( 150,  50,   0)


#----------------------------------------------------------------------

# These variables won’t change.

FPS = 30

# These are the blocks sizes. They are in the configuration file “societes.conf”.
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

OUTTERNEXTBUTTONSIZE = 60
OUTTERNEXTBUTTONPOSx = 920
OUTTERNEXTBUTTONPOSy = SCREENSIZEy - (OUTTERNEXTBUTTONSIZE + 20)

INNERNEXTBUTTONSIZE = OUTTERNEXTBUTTONSIZE / 2
INNERNEXTBUTTONPOSx = OUTTERNEXTBUTTONPOSx + (OUTTERNEXTBUTTONSIZE / 4)
INNERNEXTBUTTONPOSy = OUTTERNEXTBUTTONPOSy + (OUTTERNEXTBUTTONSIZE / 4)



#---COLORING-------------------------------------------------------------

BGCOLOR = BLACK

INTERFACEZONECOLOR = ORANGE

OUTTERNEXTBUTTONCOLOR = BROWN
INNERNEXTBUTTONCOLOR = RED


#---PLACES----------------------------------------------------------

WATER = BLUE
LAND = GREEN
YOU = RED
THE_OTHER = YELLOW

#----------------------------------------------------------------------

pygame.init()


#------------------------------------------------------------------

def main():
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    
    mousex = 0
    mousey = 0
    
    # What’s the map?
    theMap = createMap()
    
    # How big is it?
    NUMBERBLOCKSx, NUMBERBLOCKSy = countMap(theMap)
    
    # Sanity check: are all the columns equal? Otherwise there is a problem in the code, at getColor in drawMap. Allowing for columns to be unequal would complicate a lot the code, but I could try to do it, some day.
    for other_column in theMap[1:]:
        assert len(other_column) == len(theMap[0]), 'The columns aren’t equal.'
    

    
    # Make the screen.
    DISPLAYSURF = pygame.display.set_mode((SCREENSIZEx, SCREENSIZEy))
    Wtf = ((BLOCKSIZEx * (NUMBERBLOCKSx)), (BLOCKSIZEy * (NUMBERBLOCKSy + INTERFACESIZEy)))
    pygame.display.set_caption('Sociétés')
    
    
    
    DISPLAYSURF.fill(BGCOLOR)
    
    while True: # main game loop
        mainLoop(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy, mousex, mousey)

def leftTopCoordsOfBlock(smthx, smthy):
    # Convert map coordinates to pixel coordinates.
    left = smthx * BLOCKSIZEx
    top = smthy * BLOCKSIZEy
    return (left, top)

def getSomethingAtPixel(x, y, NUMBERBLOCKSx, NUMBERBLOCKSy, OUTTERNEXTBUTTONPOSx, OUTTERNEXTBUTTONPOSy, OUTTERNEXTBUTTONSIZE):
    
    for smthx in range(NUMBERBLOCKSx):
        for smthy in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(smthx, smthy)
            blockRect = pygame.Rect(left, top, BLOCKSIZEx, BLOCKSIZEy)
            smth = (smthx, smthy)
            if blockRect.collidepoint(x, y):
                return (smth)
    
    nextButtonRect = pygame.Rect(OUTTERNEXTBUTTONPOSx, OUTTERNEXTBUTTONPOSy, OUTTERNEXTBUTTONSIZE, OUTTERNEXTBUTTONSIZE)
    if nextButtonRect.collidepoint(x, y):
        return ('nextButtonClick')
    
    return (None)

def getColor(theMap, smthx, smthy):
    # color value for x, y spot is stored in TheMap[x][y]['faction'].
    # This is used in drawMap.
    return theMap[smthx][smthy]['faction']

def drawMap(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy):
    # Draws all the blocks.
    # This is used in main.
    for smthx in range(NUMBERBLOCKSx):
        for smthy in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(smthx, smthy)
            color = getColor(theMap, smthx, smthy)
            pygame.draw.rect(DISPLAYSURF, color, (left, top, BLOCKSIZEx, BLOCKSIZEy))

#----INTERFACE DRAWING--------------

def drawInterface():
    # Draw the interface.
    # It’s used in main.
    interfaceZone()
    nextButton()

def interfaceZone():
    InterfaceRect = pygame.draw.rect(DISPLAYSURF, INTERFACEZONECOLOR, (0, (SCREENSIZEy - INTERFACESIZEy), INTERFACESIZEx, INTERFACESIZEy))

def nextButton():
    OutterNextButton = pygame.draw.rect(DISPLAYSURF, OUTTERNEXTBUTTONCOLOR, (OUTTERNEXTBUTTONPOSx, OUTTERNEXTBUTTONPOSy, OUTTERNEXTBUTTONSIZE, OUTTERNEXTBUTTONSIZE))
    InnerNextButton = pygame.draw.rect(DISPLAYSURF, INNERNEXTBUTTONCOLOR, (INNERNEXTBUTTONPOSx, INNERNEXTBUTTONPOSy, INNERNEXTBUTTONSIZE, INNERNEXTBUTTONSIZE))





#-----------------------------------------

def countMap(theMap):
    # Count the number of blocks in the map.
    nbCol = len(theMap)
    nbRows = len(theMap[0])
    return nbCol, nbRows

def mainLoop(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy, mousex, mousey):
        mouseClicked = False 
        
        # Draw the map.
        drawMap(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy)
        # The map has to be smaller than the screen + the interface.
        assert NUMBERBLOCKSx * BLOCKSIZEx < 1001 and NUMBERBLOCKSy * BLOCKSIZEy < 601, 'La carte est trop grande. La hauteur doit être moins grande que 1001 pixels et la largeur doit être moins grande que 601 pixels.'
        
        # Draw the interface.
        drawInterface()
        
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
        
        # Where did you click? Was it on a block? What block?
        smth = getSomethingAtPixel(mousex, mousey, NUMBERBLOCKSx, NUMBERBLOCKSy, OUTTERNEXTBUTTONPOSx, OUTTERNEXTBUTTONPOSy, OUTTERNEXTBUTTONSIZE)
        if type(smth) == tuple: # If it was on the map.
            smthx = smth[0]
            smthy = smth[1]
            if mouseClicked:
                print '{}, {}'.format(smthx, smthy)
        
        if smth == 'nextButtonClick' and mouseClicked:
            print 'nextButtonClick'
        
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
main()
