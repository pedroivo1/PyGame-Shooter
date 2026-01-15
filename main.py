#!/usr/bin/env python3
# Author: https://github.com/pedroivo1

from scripts.game import Game
from scripts.states import MainMenu


if __name__ == "__main__":
    g = Game()

    start_menu = MainMenu(g)
    start_menu.enter_state()

    g.run()
