from __future__ import division

import pygame
from math import pi
from random import random

from .arena import Arena, ARENA_MARKINGS_COLOR, ARENA_MARKINGS_WIDTH

from ..markers import Token
from ..vision import MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER

class GoldToken(Token):
    def __init__(self, arena, marker_number):
        super(GoldToken, self).__init__(arena, marker_number,
                                        marker_type=MARKER_TOKEN_GOLD, damping=10)

    @property
    def surface_name(self):
        return 'sr/token_gold_grabbed.png' if self.grabbed else 'sr/token.png'


class SilverToken(Token):
    def __init__(self, arena, marker_number):
        super(SilverToken, self).__init__(arena, marker_number,
                                          marker_type=MARKER_TOKEN_SILVER, damping=10)

    @property
    def surface_name(self):
        return 'sr/token_silver_grabbed.png' if self.grabbed else 'sr/token_silver.png'

class SunnySideUpArena(Arena):
    size = (19, 10)
    start_locations = [( -8, -4)]

    start_headings = [pi/2]

    zone_size = 1

    def __init__(self, objects=None, wall_markers=True):
        super(SunnySideUpArena, self).__init__(objects, wall_markers)

	count=0
	for i in range(38):
            token = GoldToken(self, count)
            token.location = (-9, -4.5+i*0.25)
            self.objects.append(token)
            count+1
	
        for i in range(23):
            token = GoldToken(self, count)
            token.location = (-7, -2.75+i*0.25)
            self.objects.append(token)
            count+1
        
        #for i in range(55):
        #    token = Token(self, i, damping=10)
        #    token.location = (-6.75+i*0.25, 3)
        #    self.objects.append(token)
	
        #for i in range(71):
        #    token = Token(self, i, damping=10)
        #    token.location = (-8.75+i*0.25, 5)
        #    self.objects.append(token) 
            
        for i in range(13):
             token = GoldToken(self, count)
             token.location = (-6.75+i*0.25, 3)
             self.objects.append(token)
             count+1
	
        for i in range(29):
            token = GoldToken(self, count)
            token.location = (-8.75+i*0.25, 5)
            self.objects.append(token) 
            count+1
            
        for i in range(16):
            token = GoldToken(self, count)
            token.location = (-3.5, -1+i*0.25)
            self.objects.append(token) 
            count+1
            
        for i in range(16):
            token = GoldToken(self, count)
            token.location = (-1.5, 1+i*0.25)
            self.objects.append(token) 
            count+1
            
        
        for i in range(11):
            token = GoldToken(self, count)
            token.location = (-1.25+i*0.25, 0.75)
            self.objects.append(token)
            count+1
            
        for i in range(27):
            token = GoldToken(self, count)
            token.location = (-3.25+i*0.25, -1.25)
            self.objects.append(token)
            count+1
      
        
        for i in range(16):
            token = GoldToken(self, count)
            token.location = (3.5, -1+i*0.25)
            self.objects.append(token)
            count+1 
            
        for i in range(16):
            token = GoldToken(self, count)
            token.location = (1.5, 1+i*0.25)
            self.objects.append(token) 
            count+1
            
        for i in range(13):
             token = GoldToken(self, count)
             token.location = (3.75+i*0.25, 3)
             self.objects.append(token)
             count+1
	
        for i in range(29):
            token = GoldToken(self, count)
            token.location = (1.75+i*0.25, 5)
            self.objects.append(token)
            count+1
            
        count = 0
            
        for i in range(55):
            token = GoldToken(self, count)
            token.location = (-6.75+i*0.25, -3)
            self.objects.append(token)
            count+1
	
        for i in range(71):
            token = GoldToken(self, count)
            token.location = (-8.75+i*0.25, -4.75)
            self.objects.append(token)  
            count+1 
            
        for i in range(38):
            token = GoldToken(self, count)
            token.location = (9, -4.5+i*0.25)
            self.objects.append(token)
            count+1
	
        for i in range(23):
            token = GoldToken(self, count)
            token.location = (7, -2.75+i*0.25)
            self.objects.append(token) 
            count+1
            
        token=SilverToken(self,count)
        token.location = (-8, 0)
        self.objects.append(token) 
        count+1
        
        token=SilverToken(self,count)
        token.location = (-6, 3.75)
        self.objects.append(token) 
        count+1
        
        token=SilverToken(self,count)
        token.location = (-2.5, 1.25)
        self.objects.append(token) 
        count+1
        
        token=SilverToken(self,count)
        token.location = (1.5, -0.25)
        self.objects.append(token) 
        count+1
        
        token=SilverToken(self,count)
        token.location = (6, 3.75)
        self.objects.append(token) 
        count+1
        
        token=SilverToken(self,count)
        token.location = (8, 0.0)
        self.objects.append(token) 
        count+1
        
        token=SilverToken(self,count)
        token.location = (-4.0, -4.0)
        self.objects.append(token) 
        count+1
        

    def draw_background(self, surface, display):
        super(SunnySideUpArena, self).draw_background(surface, display)

        # Corners of the inside square
        top_left     = display.to_pixel_coord((self.left + self.zone_size, self.top + self.zone_size), self)
        top_right    = display.to_pixel_coord((self.right - self.zone_size, self.top + self.zone_size), self)
        bottom_right = display.to_pixel_coord((self.right - self.zone_size, self.bottom - self.zone_size), self)
        bottom_left  = display.to_pixel_coord((self.left + self.zone_size, self.bottom - self.zone_size), self)

        # Lines separating zones
        def line(start, end):
            pygame.draw.line(surface, ARENA_MARKINGS_COLOR, \
                             start, end, ARENA_MARKINGS_WIDTH)

        line((0, 0), top_left)
        line((display.size[0], 0), top_right)
        line(display.size, bottom_right)
        line((0, display.size[1]), bottom_left)

        # Square separating zones from centre
        pygame.draw.polygon(surface, ARENA_MARKINGS_COLOR, \
                            [top_left, top_right, bottom_right, bottom_left], 2)
