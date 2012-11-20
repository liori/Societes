#!/usr/bin/python
# -*- coding:utf-8 -*-

import pygame, sys, Image
from pygame.locals import *
import map1

#---COLORS-------------------------

#             R    G    B   Alpha

WHITE =     ( 255, 255, 255)
BLACK =     (   0,   0,   0)
BLUE =      (   0,   0, 255)
GREEN =     (   0, 255,   0)
RED =       ( 255,   0,   0)
YELLOW =    ( 255, 250,  60)
ORANGE =    ( 255, 150,  30)
BROWN =     ( 150,  50,   0)

INVISIBLE = (   0,   0,   0,   0)

#------------------------------------------

# These variables won’t change

FPS = 30

FONT = 'freesansbold.ttf'
FONTSIZE = 16

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'


#---DRAWING THE SCREEN AND INTERFACE-------------------------

SCREENSIZEx = 1000
SCREENSIZEy = 600

HALFSCREENx = int(SCREENSIZEx / 2)
HALFSCREENy = int(SCREENSIZEy / 2)

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

#----------------------------------------------------------------------

pygame.init()

#----------------------------------------------------------------------

def main():
    global FPSCLOCK, INVISIBLESURF, VISIBLESURF
    FPSCLOCK = pygame.time.Clock()
    
    mousex = 0
    mousey = 0
    
    fontObj = pygame.font.Font(FONT, FONTSIZE)
    
    # Map information
    # TODO: do wtf is the actual map (map needed as it’s a relique from old code)
    theMap = map1.createMap()
    
    # Calculate stuff about the faction
    pop = 0 #TODO
    
    # Make the screen.
    INVISIBLESURF = pygame.Surface((SCREENSIZEx, SCREENSIZEy))
    VISIBLESURF = pygame.display.set_mode((SCREENSIZEx, SCREENSIZEy))
    pygame.display.set_caption('Sociétés')
    
    # The map image
    invisibleMap = pygame.image.load('invisible_map.png')
    visibleMap = pygame.image.load('visible_map.png')
    
    slideTo = False # As of now, the map didn’t slide.
    mapx = 0
    mapy = 0
    
    mapInfo = 'osef' #TODO
    
    mainLoop(mapInfo, invisibleMap, visibleMap, mousex, mousey, fontObj, mapx, mapy, slideTo)
    
#---MAIN LOOP--------------------------------------------------------------

def mainLoop(mapInfo, invisibleMap, visibleMap, mousex, mousey, fontObj, mapx, mapy, slideTo):
    while True: # main game loop
        mouseClicked = False
        
        
        
        # The map sliding.
        if slideTo:
            if slideTo == UP:
                mapy = mapy - 30
            elif slideTo == DOWN:
                mapy = mapy + 30
            elif slideTo == LEFT:
                mapx = mapx - 30
            elif slideTo == RIGHT:
                mapx = mapx + 30
        slideTo = False
        
        INVISIBLESURF.blit(invisibleMap, ((mapx, mapy)))
        VISIBLESURF.blit(visibleMap, ((mapx, mapy)))
        
        pop = 0 #TODO
        
        # Draw the interface
        drawInterface(fontObj, pop)
        
        
        # What happens?
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouseClicked = True
                mousex, mousey = event.pos
            elif event.type == KEYUP: # camera moving
                if event.key == K_RIGHT:
                    slideTo = LEFT
                elif event.key == K_LEFT:
                    slideTo = RIGHT
                elif event.key == K_DOWN:
                    slideTo = UP
                elif event.key == K_UP:
                    slideTo = DOWN


        # Where did you click? Was it on a region? What region?
        smth = getSomethingAtPixel(mousex, mousey, mapx, mapy, OUTTERFINISHBUTTONPOSx, OUTTERFINISHBUTTONPOSy, OUTTERFINISHBUTTONSIZE)
        
        if mouseClicked:
            print '{}'.format(smth)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
   
   
#----------------------------
     
def getSomethingAtPixel(x, y, mapx, mapy, OUTTERFINISHBUTTONPOSx, OUTTERFINISHBUTTONPOSy, OUTTERFINISHBUTTONSIZE):
    
    smth = INVISIBLESURF.get_at((x, y))
    return (smth)
    
    nextButtonRect = pygame.Rect(OUTTERFINISHBUTTONPOSx, OUTTERFINISHBUTTONPOSy, OUTTERFINISHBUTTONSIZE, OUTTERFINISHBUTTONSIZE)
    if nextButtonRect.collidepoint(x, y):
        return ('finishButtonClick')
  
  
  
        
#----INTERFACE DRAWING--------------

def drawInterface(fontObj, pop):
    # Draw the interface.
    # It’s used in main.
    interfaceZone()
    finishButton()
    someText(fontObj, pop)

def interfaceZone():
    InterfaceRect = pygame.draw.rect(INVISIBLESURF, INTERFACEZONECOLOR, (0, (SCREENSIZEy - INTERFACESIZEy), INTERFACESIZEx, INTERFACESIZEy))

def finishButton():
    OutterFinishButton = pygame.draw.rect(INVISIBLESURF, OUTTERFINISHBUTTONCOLOR, (OUTTERFINISHBUTTONPOSx, OUTTERFINISHBUTTONPOSy, OUTTERFINISHBUTTONSIZE, OUTTERFINISHBUTTONSIZE))
    InnerFinishButton = pygame.draw.rect(INVISIBLESURF, INNERFINISHBUTTONCOLOR, (INNERFINISHBUTTONPOSx, INNERFINISHBUTTONPOSy, INNERFINISHBUTTONSIZE, INNERFINISHBUTTONSIZE))

def someText(fontObj, pop):
    popTextSurface = fontObj.render('Population: {}'.format(pop), True, WHITE, INVISIBLE)
    popTextRect = popTextSurface.get_rect()
    popTextRect.right = POPTEXTRIGHT
    popTextRect.top = POPTEXTTOP
        
#---------------------------

main()
