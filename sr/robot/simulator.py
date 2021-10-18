from __future__ import division

import threading
import pygame

from .arenas import PiratePlunderArena, CTFArena, SunnySideUpArena, ABCArena, CalderaArena, TwoColoursArena
from .display import Display

DEFAULT_GAME = 'caldera'

GAMES = {'caldera': CalderaArena,
         'pirate-plunder': PiratePlunderArena,
         'ctf': CTFArena,
         'sunny-side-up': SunnySideUpArena,
         'abc': ABCArena,
         'two-colours': TwoColoursArena
        }

class Simulator(object):
    def __init__(self, config={}, size=(8, 8), frames_per_second=30, background=True):
        try:
            game_name = config['game']
            del config['game']
        except KeyError:
            game_name = DEFAULT_GAME
        game = GAMES[game_name]
        self.arena = game(**config)

        self.display = Display(self.arena)

        self.background = background
        self.frames_per_second = frames_per_second

        if self.background:
            self._loop_thread = threading.Thread(target=self._main_loop, args=(frames_per_second,))
            self._loop_thread.setDaemon(True)
            self._loop_thread.start()

    def run(self):
        if self.background:
            raise RuntimeError('Simulator runs in the background. Try passing background=False')
        self._main_loop(self.frames_per_second)

    def _main_loop(self, frames_per_second):
        clock = pygame.time.Clock()

        while True:
            if any(event.type == pygame.QUIT
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                    for event in pygame.event.get()):
                break

            self.display.tick(1/frames_per_second)
            clock.tick(frames_per_second)

        pygame.quit()
