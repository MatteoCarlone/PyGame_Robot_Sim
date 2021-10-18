from __future__ import division

from math import ceil, cos, pi, sin

import pygame

from .arena import ARENA_FLOOR_COLOR, ARENA_MARKINGS_COLOR, ARENA_MARKINGS_WIDTH, Arena, draw_corner_zones
from ..markers import Token


# Perform a clockwise rotate around 0,0.
def rotate(x, y, radians):
    return (x * cos(radians) + y * -sin(radians)), (x * sin(radians) + y * cos(radians))


PLATFORM_COLOUR = (0x68, 0x75, 0x91)

class CalderaArena(Arena):
    start_locations = [(-3.6, -3.6),
                       (3.6, -3.6),
                       (3.6, 3.6),
                       (-3.6, 3.6)]

    start_headings = [0.25 * pi,
                      0.75 * pi,
                      -0.75 * pi,
                      -0.25 * pi]

    def __init__(self, objects=None, wall_markers=True):
        super(CalderaArena, self).__init__(objects, wall_markers)
        self._init_tokens()

    def _init_tokens(self):
        token_ids = [28, 29, 30, 31]

        token_locations_offsets_from_zone = [(0.5, 1.3),
                                             (0.5, 1.5),
                                             (0.5, 1.7),
                                             (0.5, 1.9),
                                             (0.5, 2.1),]

        for zone in range(0, 4):
            for i, location in enumerate(token_locations_offsets_from_zone):
                rotated_location = rotate(location[0] - 4, location[1] - 4, (pi / 2) * zone)
                token = Token(self, token_ids[zone], damping=10)
                token.location = rotated_location
                self.objects.append(token)

    def draw_background(self, surface, display):
        super(CalderaArena, self).draw_background(surface, display)

        def line(start, end):
            pygame.draw.line(surface, ARENA_MARKINGS_COLOR,
                             display.to_pixel_coord(start), display.to_pixel_coord(end),
                             ARENA_MARKINGS_WIDTH)

        def line_symmetric(start, end):
            """
            Draw a line, double reflected on the X and Y axis
            (creating 8 lines)
            """
            start_x, start_y = start
            end_x, end_y = end
            line((start_x, start_y), (end_x, end_y))
            line((-start_x, start_y), (-end_x, end_y))
            line((-start_x, -start_y), (-end_x, -end_y))
            line((start_x, -start_y), (end_x, -end_y))
            line((start_y, start_x), (end_y, end_x))
            line((-start_y, start_x), (-end_y, end_x))
            line((-start_y, -start_x), (-end_y, -end_x))
            line((start_y, -start_x), (end_y, -end_x))

        # Starting zones
        self.starting_zone_side = 1
        draw_corner_zones(self, display, surface, shape='Square')


        # Grid
        square_width = 1.200
        start_pos = (-3, -3)
        grid_dimensions = (5, 5)
        quartered_grid_dims = (int(ceil(grid_dimensions[0]/2)), int(ceil(grid_dimensions[1]/2)))

        def to_grid_pos(grid_x, grid_y):
            return (start_pos[0] + grid_x * square_width,
                    start_pos[1] + grid_y * square_width)

        # Raised platform
        # (These positions are in grid cell locations)
        platform_outer_start = to_grid_pos(1, 1)
        platform_outer_end = to_grid_pos(4, 4)
        platform_inner_start = to_grid_pos(2, 2)
        platform_inner_end = to_grid_pos(3, 3)

        outer_platform = (
            (platform_outer_start[0], platform_outer_start[1]),
            (platform_outer_start[0], platform_outer_end[1]),
            (platform_outer_end[0],   platform_outer_end[1]),
            (platform_outer_end[0],   platform_outer_start[1]),
        )

        inner_platform = (
            (platform_inner_start[0], platform_inner_start[1]),
            (platform_inner_start[0], platform_inner_end[1]),
            (platform_inner_end[0],   platform_inner_end[1]),
            (platform_inner_end[0],   platform_inner_start[1]),
        )

        outer_platform = tuple([display.to_pixel_coord(p, self) for p in outer_platform])
        pygame.draw.polygon(surface, PLATFORM_COLOUR, outer_platform, 0)

        inner_platform = tuple([display.to_pixel_coord(p, self) for p in inner_platform])
        pygame.draw.polygon(surface, ARENA_FLOOR_COLOR, inner_platform, 0)

        # Redraw the motif on top
        self.draw_motif(surface, display)

        for x in range(quartered_grid_dims[0]):
            for y in range(quartered_grid_dims[1]):
                # Line to the right from the grid pos
                pos_a = (start_pos[0]+(x*square_width), start_pos[1]+(y*square_width))
                pos_b = (start_pos[0]+((x+1)*square_width), start_pos[1]+(y*square_width))
                line_symmetric(pos_a, pos_b)


