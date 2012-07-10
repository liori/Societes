#!/usr/bin/python
# -*- coding:utf-8 -*-

#---COLORS-------------------------------------------------------------

#           R   G    B

WHITE =  ( 255, 255, 255)
BLUE =   (   0,   0, 255)
GREEN =  (   0, 255,   0)
RED =    ( 255,   0,   0)
YELLOW = ( 255, 220,  50)

#---PLACES----------------------------------------------------------

WATER = BLUE
LAND = GREEN
YOU = RED
THE_OTHER = YELLOW

#-------------------------------------------------------------------

def createMap():
    # Create the map
    
    # Regions
    R00 = {'land': False, 'faction': WATER, 'pop': 0, 'agrable_level': 0, 'prey_level': 0, 'fish_level': 3, 'flint_tonne': 0}
    R01 = {'land': False, 'faction': WATER, 'pop': 0, 'agrable_level': 0, 'prey_level': 0, 'fish_level': 5, 'flint_tonne': 0}
    R02 = {'land': True, 'faction': YOU, 'pop': 120, 'agrable_level': 3, 'prey_level': 2, 'fish_level': 2, 'flint_tonne': 2000}
    R10 = {'land': False, 'faction': WATER, 'pop': 0, 'agrable_level': 0, 'prey_level': 0, 'fish_level': 4, 'flint_tonne': 0}
    R11 = {'land': True, 'faction': YOU, 'pop': 100, 'agrable_level': 2, 'prey_level': 3, 'fish_level': 1, 'flint_tonne': 100}
    R12 = {'land': True, 'faction': YOU, 'pop': 100, 'agrable_level': 3, 'prey_level': 3, 'fish_level': 1, 'flint_tonne': 230}
    R20 = {'land': True, 'faction': THE_OTHER, 'pop': 100, 'agrable_level': 2, 'prey_level': 3, 'fish_level': 3, 'flint_tonne': 3500}
    R21 = {'land': True, 'faction': THE_OTHER, 'pop': 130, 'agrable_level': 4, 'prey_level': 2, 'fish_level': 3, 'flint_tonne': 500}
    R22 = {'land': True, 'faction': THE_OTHER, 'pop': 100, 'agrable_level': 4, 'prey_level': 2, 'fish_level': 1, 'flint_tonne': 100}
    
    # Columns of regions
    col0 = R00, R01, R02
    col1 = R10, R11, R12
    col2 = R20, R21, R22
    
    theMap = col0, col1, col2,
    
    return theMap