#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scripts.game import Game
from scripts.level import Level

if __name__ == "__main__":
    g = Game()
    
    start_level = Level(g)
    start_level.enter_state()
    
    g.run()
