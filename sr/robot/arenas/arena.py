from __future__ import division

from math import pi

import pygame

from ..display import get_surface
from ..markers import WallMarker

import threading

import pypybox2d

MARKERS_PER_WALL = 7

ARENA_FLOOR_COLOR = (0x12, 0x2B, 0x5E)
ARENA_MARKINGS_COLOR = (0xD0, 0xD0, 0xD0)
ARENA_MARKINGS_WIDTH = 3

CORNER_COLOURS = (
    (0x00, 0xff, 0x00),
    (0xff, 0x66, 0x00),
    (0xff, 0x00, 0xff),
    (0xff, 0xff, 0x00),
)

def towards_zero(point, dist):
    if point < 0:
        return point + dist
    else:
        return point - dist

def apply_transparency(foreground, background, opacity):
    def helper(fore, back):
        return back + (fore-back)*opacity
    return tuple(map(helper, foreground, background))

def fade_to_white(colour, opacity = 0.6):
    white = (0xff,) * 3
    return apply_transparency(colour, white, opacity)

def lerp(delta, a, b):
    return delta*b + (1-delta)*a

def draw_corner_zones(arena, display, surface, shape='Triangular'):
    """
    Draw corner zones for the given arena onto the given display.
    """

    def get_coord(x, y):
        return display.to_pixel_coord((x, y), arena)

    # Lines separating zones
    def line(start, end):
        pygame.draw.line(surface, ARENA_MARKINGS_COLOR, \
                         start, end, ARENA_MARKINGS_WIDTH)

    def starting_zone(corner_pos):
        x, y = corner_pos
        length = arena.starting_zone_side
        a = get_coord(towards_zero(x, length), y)
        b = get_coord(x, towards_zero(y, length))
        c = (a[0], b[1])

        line(a, c)
        line(b, c)

    def scoring_zone(corner_pos, colour, shape):
        x, y = corner_pos
        if shape is 'Triangular':
            length = arena.scoring_zone_side
            a = get_coord(towards_zero(x, length), y)
            b = get_coord(x, towards_zero(y, length))
            c = get_coord(x, y)
            pygame.draw.polygon(surface, colour, (a, b, c), 0)
        elif shape is 'Square':
            length = arena.starting_zone_side
            a = get_coord(towards_zero(x, length), y)
            b = get_coord(x, y)
            c = get_coord(x, towards_zero(y, length))
            d = get_coord(towards_zero(x, length), towards_zero(y, length))
            pygame.draw.polygon(surface, colour, (a, b, c, d), 0)

    for i, pos in enumerate(arena.corners):
        colour = fade_to_white(CORNER_COLOURS[i])
        scoring_zone(pos, colour, shape=shape)
        starting_zone(pos)

class Arena(object):
    size = (8, 8)
    start_locations = [(0, 0)]
    start_headings = [0]

    motif_name = 'sr/sr_round_flat.png'

    @property
    def left(self):
        return -self.size[0] / 2
    @property
    def right(self):
        return self.size[0] / 2
    @property
    def top(self):
        return -self.size[1] / 2
    @property
    def bottom(self):
        return self.size[1] / 2

    @property
    def corners(self):
        yield (self.left, self.top)
        yield (self.right, self.top)
        yield (self.right, self.bottom)
        yield (self.left, self.bottom)

    def _populate_wall(self, left, right, count, start, angle):
        left_bound_x, left_bound_y = left
        right_bound_x, right_bound_y = right
        for i in range(count):
            delta = (i + 1) / (count + 1)
            x = lerp(delta, left_bound_x, right_bound_x)
            y = lerp(delta, left_bound_y, right_bound_y)
            identifier = start + i
            self.objects.append(WallMarker(self, identifier, (x, y), angle))

    def _populate_wall_markers(self):
        # Left wall
        self._populate_wall(left = (self.left, self.bottom), right = (self.left, self.top),
                            count = MARKERS_PER_WALL, start = 3*MARKERS_PER_WALL, angle = 0)
        # Right wall
        self._populate_wall(left = (self.right, self.top), right = (self.right, self.bottom),
                            count = MARKERS_PER_WALL, start = MARKERS_PER_WALL, angle = pi)
        # Bottom wall
        self._populate_wall(left = (self.right, self.bottom), right = (self.left, self.bottom),
                            count = MARKERS_PER_WALL, start = 2*MARKERS_PER_WALL, angle = pi / 2)
        # Top wall
        self._populate_wall(left = (self.left, self.top), right = (self.right, self.top),
                            count = MARKERS_PER_WALL, start = 0, angle = 3*pi / 2)

    def _init_physics(self):
        self._physics_world = pypybox2d.world.World(gravity=(0, 0))
        # Global lock for simulation
        self.physics_lock = threading.RLock()
        # Create the arena wall
        WALL_WIDTH = 2
        WALL_SETTINGS = {'restitution': 0.2, 'friction': 0.3}

        wall_right = self._physics_world.create_body(position=(self.right, 0),
                                                     type=pypybox2d.body.Body.STATIC)
        wall_right.create_polygon_fixture([(WALL_WIDTH, self.top - WALL_WIDTH),
                                           (WALL_WIDTH, self.bottom + WALL_WIDTH),
                                           (0, self.bottom + WALL_WIDTH),
                                           (0, self.top - WALL_WIDTH)],
                                          **WALL_SETTINGS)

        wall_left = self._physics_world.create_body(position=(self.left, 0),
                                                    type=pypybox2d.body.Body.STATIC)
        wall_left.create_polygon_fixture([(-WALL_WIDTH, self.top - WALL_WIDTH),
                                          (0, self.top - WALL_WIDTH),
                                          (0, self.bottom + WALL_WIDTH),
                                          (-WALL_WIDTH, self.bottom + WALL_WIDTH)],
                                         **WALL_SETTINGS)

        wall_top = self._physics_world.create_body(position=(0, self.top),
                                                   type=pypybox2d.body.Body.STATIC)
        wall_top.create_polygon_fixture([(self.left, 0),
                                         (self.left, -WALL_WIDTH),
                                         (self.right, -WALL_WIDTH),
                                         (self.right, 0)],
                                        **WALL_SETTINGS)

        wall_bottom = self._physics_world.create_body(position=(0, self.bottom),
                                                   type=pypybox2d.body.Body.STATIC)
        wall_bottom.create_polygon_fixture([(self.left, 0),
                                            (self.right, 0),
                                            (self.right, WALL_WIDTH),
                                            (self.left, WALL_WIDTH)],
                                           **WALL_SETTINGS)

    def __init__(self, objects=None, wall_markers=True):
        self._init_physics()
        self.objects = objects if objects is not None else []
        if wall_markers:
            self._populate_wall_markers()

    ## Public Methods ##

    def contains_point(self, x, y):
        if not (self.left < x < self.right):
            return False, 0, max(self.left, min(x, self.right))
        elif not (self.top < y < self.bottom):
            return False, 1, max(self.top, min(y, self.bottom))
        else:
            return True, None, None

    def tick(self, time_passed):
        with self.physics_lock:
            self._physics_world.step(time_passed,
                                     vel_iters=8,
                                     pos_iters=3)
        for obj in self.objects:
            if hasattr(obj, "tick"):
                obj.tick(time_passed)

    def draw_motif(self, surface, display):
        # Motif
        motif = get_surface(self.motif_name)
        x, y = display.to_pixel_coord((0, 0), self)
        w, h = motif.get_size()
        surface.blit(motif, (x - w / 2, y - h / 2))

    def draw_background(self, surface, display):
        surface.fill(ARENA_FLOOR_COLOR)
        self.draw_motif(surface, display)


