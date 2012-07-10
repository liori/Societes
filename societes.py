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

SCREENSIZEx = 1000
SCREENSIZEy = 600

INTERFACESIZEx = SCREENSIZEx
INTERFACESIZEy = 100

BGCOLOR = BLACK


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
        blockx, blocky = getBlockAtPixel(mousex, mousey, NUMBERBLOCKSx, NUMBERBLOCKSy)
        if blockx != None and blocky != None and mouseClicked:
            print '{}, {}'.format(blockx, blocky)
            
        
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def leftTopCoordsOfBlock(blockx, blocky):
    # Convert map coordinates to pixel coordinates.
    left = blockx * BLOCKSIZEx
    top = blocky * BLOCKSIZEy
    return (left, top)

def getBlockAtPixel(x, y, NUMBERBLOCKSx, NUMBERBLOCKSy):
    for blockx in range(NUMBERBLOCKSx):
        for blocky in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(blockx, blocky)
            blockRect = pygame.Rect(left, top, BLOCKSIZEx, BLOCKSIZEy)
            if blockRect.collidepoint(x, y):
                return (blockx, blocky)
            #elif
    return (None, None)

def getColor(theMap, blockx, blocky):
    # color value for x, y spot is stored in TheMap[x][y]['faction'].
    # This is used in drawMap.
    return theMap[blockx][blocky]['faction']

def drawMap(theMap, NUMBERBLOCKSx, NUMBERBLOCKSy):
    # Draws all the blocks.
    # This is used in main.
    for blockx in range(NUMBERBLOCKSx):
        for blocky in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(blockx, blocky)
            color = getColor(theMap, blockx, blocky)
            pygame.draw.rect(DISPLAYSURF, color, (left, top, BLOCKSIZEx, BLOCKSIZEy))

def drawInterface():
    # Draw the interface.
    # It’s used in main.
    InterfaceRect = pygame.draw.rect(DISPLAYSURF, ORANGE, (0, (SCREENSIZEy - INTERFACESIZEy), INTERFACESIZEx, INTERFACESIZEy))

def countMap(theMap):
    # Count the number of blocks in the map.
    nbCol = len(theMap)
    nbRows = len(theMap[0])
    return nbCol, nbRows



    
main()
