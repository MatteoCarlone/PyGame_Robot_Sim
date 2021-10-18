from .game_object import GameObject
from .vision import create_marker_info_by_type, MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER, MARKER_ARENA

import pypybox2d

class Token(GameObject):
    grabbable = True

    @property
    def location(self):
        return self._body.position

    @location.setter
    def location(self, new_pos):
        if self._body is None:
            return # Slight hack: deal with the initial setting from the constructor
        self._body.position = new_pos

    @property
    def heading(self):
        return self._body.angle

    @heading.setter
    def heading(self, _new_heading):
        if self._body is None:
            return # Slight hack: deal with the initial setting from the constructor
        self._body.angle = _new_heading

    def __init__(self, arena, number, damping, marker_type=MARKER_TOKEN_GOLD):
        self._body = arena._physics_world.create_body(position=(0, 0),
                                                      angle=0,
                                                      linear_damping=damping,
                                                      angular_damping=damping,
                                                      type=pypybox2d.body.Body.DYNAMIC)
        super(Token, self).__init__(arena)
        self.marker_info = create_marker_info_by_type(marker_type, number)
        self.grabbed = False
        WIDTH = 0.09
        self._body.create_polygon_fixture([(-WIDTH, -WIDTH),
                                           ( WIDTH, -WIDTH),
                                           ( WIDTH,  WIDTH),
                                           (-WIDTH,  WIDTH)],
                                          density=1,
                                          restitution=0.2,
                                          friction=0.3)

    def grab(self):
        self.grabbed = True

    def release(self):
        self.grabbed = False

    @property
    def surface_name(self):
        return 'sr/token{0}.png'.format('_grabbed' if self.grabbed else '')

class WallMarker(GameObject):
    surface_name = 'sr/wall_marker.png'

    def __init__(self, arena, number, location=(0,0), heading=0):
        super(WallMarker, self).__init__(arena)
        self.marker_info = create_marker_info_by_type(MARKER_ARENA, number)
        self.location = location
        self.heading = heading

