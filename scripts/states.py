import pygame
import csv
from abc import ABC, abstractmethod
from .settings import *
from .world import World 
from .utils import Button

class State(ABC):
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    @abstractmethod
    def update(self, dt, actions): pass

    @abstractmethod
    def draw(self, surface): pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()

class Level(State):
    def __init__(self, game, level_index=1):
        super().__init__(game)
        self.level_index = level_index
        
        # --- AJUSTE DE ALINHAMENTO DOS BOTÕES ---
        # Calculamos o centro da tela
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        # Espaçamento entre os botões (quanto maior, mais afastados)
        button_gap = 80 
        
        # Opção Vertical (Um em cima do outro)
        self.restart_btn = Button(center_x, center_y - button_gap, self.game.assets['restart_btn'], 3)
        self.exit_btn = Button(center_x, center_y + button_gap, self.game.assets['exit_btn'], 1)

        self.player_bullet_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()
        self.item_box_group = pygame.sprite.Group()
        
        level_data = []
        try:
            with open(f'data/levels/level{self.level_index}_data.csv', newline='') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    level_data.append(list(map(int, row)))
        except FileNotFoundError:
            print(f"Erro: Nível {self.level_index} não encontrado.")
            self.game.running = False
            return

        self.scroll = 0
        self.level_width = len(level_data[0]) * TILE_SIZE

        self.world = World(game)
        groups_dict = {
            'player_group': self.player_group,
            'enemy_group': self.enemy_group,
            'player_bullets': self.player_bullet_group,
            'enemy_bullets': self.enemy_bullet_group,
            'item_box_group': self.item_box_group
        }
        self.player = self.world.process_data(level_data, groups_dict)

    def update(self, dt, actions):
        if not self.player: return

        # --- Lógica de Game Over ---
        if not self.player.alive_:
            # Se o player morreu, checa os cliques nos botões
            if self.restart_btn.draw(self.game.screen): # Truque: verifica clique sem desenhar de verdade no update
                # Reinicia o nível
                self.game.state_stack.pop()
                new_level = Level(self.game, self.level_index)
                new_level.enter_state()
            
            if self.exit_btn.draw(self.game.screen):
                self.game.running = False
            
            # Retorna aqui para NÃO atualizar o resto do jogo (congela a tela)
            return
        # ---------------------------

        # Câmera
        if self.player.rect.centerx > SCREEN_WIDTH / 2 and self.player.rect.centerx < (self.level_width - SCREEN_WIDTH / 2):
            self.scroll += (self.player.rect.centerx - self.scroll - SCREEN_WIDTH / 2) * 0.1
        
        if self.scroll < 0: self.scroll = 0
        elif self.scroll > self.level_width - SCREEN_WIDTH: self.scroll = self.level_width - SCREEN_WIDTH

        self.player_group.update(dt, actions, self.world.obstacle_group, self.world.water_group)
        self.player_bullet_group.update(dt)
        self.player.grenade_group.update(dt, self.world.obstacle_group)
        self.player.explosion_group.update(dt)

        self.enemy_group.update(dt, self.player, self.world.obstacle_group)
        self.enemy_bullet_group.update(dt)
        self.item_box_group.update(self.player)

        self._check_collisions()
        self._check_level_complete()

    def _check_level_complete(self):
        if pygame.sprite.spritecollide(self.player, self.world.exit_group, False):
            self.level_index += 1
            if self.level_index <= MAX_LEVELS:
                self.game.state_stack.pop() 
                new_level = Level(self.game, self.level_index)
                new_level.enter_state()
            else:
                print("JOGO ZERADO!")
                # Aqui poderia ir para um menu ou fechar
                self.game.running = False

    def _check_collisions(self):
        hits = pygame.sprite.groupcollide(self.enemy_group, self.player_bullet_group, False, True)
        for enemy in hits:
            enemy.take_damage(25)

        exp_hits = pygame.sprite.groupcollide(self.player.explosion_group, self.enemy_group, False, False)
        for explosion, enemies_hit in exp_hits.items():
            for enemy in enemies_hit:
                if enemy not in explosion.hit_list:
                    enemy.take_damage(explosion.damage)
                    explosion.hit_list.append(enemy)

        player_hit = pygame.sprite.groupcollide(self.player.explosion_group, self.player_group, False, False)
        for explosion in player_hit:
             if self.player not in explosion.hit_list:
                 self.player.take_damage(explosion.damage)
                 explosion.hit_list.append(self.player)
        
        if pygame.sprite.spritecollide(self.player, self.enemy_bullet_group, True): # type: ignore
            self.player.take_damage(10)

    def draw_scrolled(self, surface, group):
        for sprite in group:
            surface.blit(sprite.image, (sprite.rect.x - self.scroll, sprite.rect.y))

    def draw(self, surface):
        surface.fill((144, 201, 120))
        
        self.draw_scrolled(surface, self.world.decoration_group)
        self.draw_scrolled(surface, self.world.water_group)
        self.draw_scrolled(surface, self.world.exit_group)
        self.draw_scrolled(surface, self.world.obstacle_group)
        self.draw_scrolled(surface, self.item_box_group)
        
        self.draw_scrolled(surface, self.player_group)
        self.draw_scrolled(surface, self.enemy_group)
        
        self.draw_scrolled(surface, self.player_bullet_group)
        self.draw_scrolled(surface, self.player.grenade_group)
        self.draw_scrolled(surface, self.player.explosion_group)
        self.draw_scrolled(surface, self.enemy_bullet_group)

        if self.player:
            self.player.draw_ui(surface, self.scroll) 
            
            for i in range(self.player.ammo):
                x = 10 + i*11
                surface.blit(self.game.assets['bullet'], (x, 35))
            for i in range(self.player.grenade):
                x = 10 + i*15
                surface.blit(self.game.assets['grenade'], (x, 62))
        
        # --- Desenha Game Over ---
        if not self.player.alive_:
            self.restart_btn.draw(surface)
            self.exit_btn.draw(surface)
        # -------------------------

        for enemy in self.enemy_group:
            enemy.draw_ui(surface, self.scroll)

        if DEBUG:
            for group in [self.world.obstacle_group, self.world.water_group, self.player_group, self.enemy_group]:
                for sprite in group:
                    rect_copy = sprite.rect.copy()
                    rect_copy.x -= self.scroll
                    pygame.draw.rect(surface, (255, 255, 255), rect_copy, 1)