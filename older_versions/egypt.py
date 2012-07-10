#!/usr/bin/python
# -*- coding:utf-8 -*-

import pygame, sys, random
from pygame.locals import *
from map1 import *

#---COLORS-------------------------------------------------------------

#           R   G    B

WHITE =  ( 255, 255, 255)
BLUE =   (   0,   0, 255)
GREEN =  (   0, 255,   0)
RED =    ( 255,   0,   0)
YELLOW = ( 255, 220,  50)


#----------------------------------------------------------------------

# These variables won’t change.

FPS = 30

# These are the blocks sizes.
BLOCKSIZEy = 150
BLOCKSIZEx = 150
# These are the numbers of blocks.
NUMBERBLOCKSx = 3
NUMBERBLOCKSy = 3

INTERFACE = 1

BGCOLOR = WHITE


#---PLACES----------------------------------------------------------

WATER = BLUE
LAND = GREEN
YOU = RED
THE_OTHER = YELLOW

#----------------------------------------------------------------------

pygame.init()
DISPLAYSURF = pygame.display.set_mode(((BLOCKSIZEx * (NUMBERBLOCKSx)), (BLOCKSIZEy * (NUMBERBLOCKSy + INTERFACE))))
pygame.display.set_caption('Gaule')

DISPLAYSURF.fill(BGCOLOR)

#------------------------------------------------------------------

def main():
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    
    mousex = 0
    mousey = 0
    
    theMap = createMap()
    
    while True: # main game loop
        mouseClicked = False
        
        drawMap(theMap)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        blockx, blocky = getBlockAtPixel(mousex, mousey)
        if blockx != None and blocky != None and mouseClicked:
            print '{}, {}'.format(blockx, blocky)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def leftTopCoordsOfBlock(blockx, blocky):
    # Convert map coordinates to pixel coordinates.
    left = blockx * BLOCKSIZEx
    top = blocky * BLOCKSIZEy
    return (left, top)

def getBlockAtPixel(x, y):
    for blockx in range(NUMBERBLOCKSx):
        for blocky in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(blockx, blocky)
            blockRect = pygame.Rect(left, top, BLOCKSIZEx, BLOCKSIZEy)
            if blockRect.collidepoint(x, y):
                return (blockx, blocky)
    return (None, None)



def getColor(theMap, blockx, blocky):
    # color value for x, y spot is stored in TheMap[x][y]['faction']
    return theMap[blockx][blocky]['faction']

def drawMap(theMap):
    # Draws all the blocks.
    for blockx in range(NUMBERBLOCKSx):
        for blocky in range(NUMBERBLOCKSy):
            left, top = leftTopCoordsOfBlock(blockx, blocky)
            color = getColor(theMap, blockx, blocky)
            pygame.draw.rect(DISPLAYSURF, color, (left, top, BLOCKSIZEx, BLOCKSIZEy))
    
main()
