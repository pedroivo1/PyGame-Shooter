import pygame
from .settings import *
from .entities.soldier import Player, Enemy
from .entities.Items import ItemBox
from .entities.tiles import Tile, ExitTile

class World:
    def __init__(self, game):
        self.game = game
        self.obstacle_group = pygame.sprite.Group()   # Colidem (0 a 8)
        self.decoration_group = pygame.sprite.Group() # Decoração (11 a 14)
        self.water_group = pygame.sprite.Group()      # Água mortal (9 e 10)
        self.exit_group = pygame.sprite.Group()       # Saída (20)

    def process_data(self, data, groups):
        player = None
        
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                
                if tile >= 0:
                    img_x = x * TILE_SIZE
                    img_y = y * TILE_SIZE

                    # --- CAMADA FÍSICA (Chão/Paredes) ---
                    if 0 <= tile <= 8:
                        tile_obj = Tile(self.game, img_x, img_y, tile)
                        self.obstacle_group.add(tile_obj)
                    
                    # --- CAMADA ÁGUA (Mortal) ---
                    elif tile == 9 or tile == 10:
                        tile_obj = Tile(self.game, img_x, img_y, tile)
                        self.water_group.add(tile_obj)

                    # --- CAMADA DECORATIVA ---
                    elif 11 <= tile <= 14:
                        tile_obj = Tile(self.game, img_x, img_y, tile)
                        self.decoration_group.add(tile_obj)

                    # --- ENTIDADES ---
                    elif tile == 15: # Player Verde
                        player = Player(self.game, img_x, img_y, TILE_SIZE*5.8, 'green', 20, 5, groups['player_bullets'])
                        groups['player_group'].add(player)

                    elif tile == 16: # Inimigo Vermelho
                        enemy = Enemy(self.game, img_x, img_y, TILE_SIZE*4.5, 'red', groups['enemy_bullets'])
                        groups['enemy_group'].add(enemy)

                    elif tile == 17: # Ammo Box
                        ItemBox(self.game, 'ammo_box', img_x, img_y, groups['item_box_group'])
                    
                    elif tile == 18: # Grenade Box
                        ItemBox(self.game, 'grenade_box', img_x, img_y, groups['item_box_group'])

                    elif tile == 19: # Health Box
                        ItemBox(self.game, 'health_box', img_x, img_y, groups['item_box_group'])

                    # --- SAÍDA ---
                    elif tile == 20:
                        exit_tile = ExitTile(self.game, img_x, img_y, tile)
                        self.exit_group.add(exit_tile)

        return player