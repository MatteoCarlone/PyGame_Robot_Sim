from math import pi

from .arena import Arena, draw_corner_zones

from ..markers import Token
from ..vision import MARKER_TOKEN_A, MARKER_TOKEN_B, MARKER_TOKEN_C

def token_positions(separation):
    """
    Iterate over a 3x3 grid of positions, centered at the middle of the arena
    and with the given separation.

    Positions are yielded top-to-bottom, left-to-right.
    """
    offsets = (-separation, 0, separation)
    for x_pos in offsets:
        for y_pos in offsets:
            yield x_pos, y_pos

class ABCArena(Arena):
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
        super(ABCArena, self).__init__(objects, wall_markers)

        # Positions are top-to-bottom, left-to-right
        positions = token_positions(separation=1.5)
        token_types = [
            (MARKER_TOKEN_A, 0),
            (MARKER_TOKEN_B, 0),
            (MARKER_TOKEN_A, 1),
            (MARKER_TOKEN_B, 1),
            (MARKER_TOKEN_C, 0),
            (MARKER_TOKEN_B, 2),
            (MARKER_TOKEN_A, 2),
            (MARKER_TOKEN_B, 3),
            (MARKER_TOKEN_A, 3),
        ]

        for pos, (marker_type, offset) in zip(positions, token_types):
            token = Token(self, offset, damping=10, marker_type=marker_type)
            token.location = pos
            self.objects.append(token)

    def draw_background(self, surface, display):
        super(ABCArena, self).draw_background(surface, display)

        draw_corner_zones(self, display, surface)
