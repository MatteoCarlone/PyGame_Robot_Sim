from __future__ import division

from math import pi

from .arena import Arena, draw_corner_zones

from ..markers import Token

def token_positions(separation):
    offsets = (-separation, 0, separation)
    for x_pos in offsets:
        for y_pos in offsets:
            yield x_pos, y_pos

class SunnySideUpArena(Arena):
    start_locations = [(-3.6, -3.6),
                       ( 3.6, -3.6),
                       ( 3.6,  3.6),
                       (-3.6,  3.6)]

    start_headings = [0.25*pi,
                      0.75*pi,
                      -0.75*pi,
                      -0.25*pi]

    starting_zone_side = 1
    scoring_zone_side = 2

    def __init__(self, objects=None, wall_markers=True):
        super(SunnySideUpArena, self).__init__(objects, wall_markers)

        for i, pos in enumerate(token_positions(separation = 1.5)):
            token = Token(self, i, damping=10)
            token.location = pos
            self.objects.append(token)

    def draw_background(self, surface, display):
        super(SunnySideUpArena, self).draw_background(surface, display)

        draw_corner_zones(self, display, surface)
