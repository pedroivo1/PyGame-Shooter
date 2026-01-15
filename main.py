#!/usr/bin/env python3
# Author: https://github.com/pedroivo1

from scripts.game import Game
from scripts.states import Level


if __name__ == "__main__":
    g = Game()

    start_level = Level(g)
    start_level.enter_state()

    g.run()
