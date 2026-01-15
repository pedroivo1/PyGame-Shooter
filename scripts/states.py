import pygame
import csv
from abc import ABC, abstractmethod
from .settings import *
from .world import World 
from .utils import Button, load_progress, save_progress

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

class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.max_level = load_progress()
        
        btn_size = 60       
        gap = 20            
        max_width = 640     
        
        cols = max_width // (btn_size + gap)
        if cols == 0: cols = 1 

        total_rows = (MAX_LEVELS + cols - 1) // cols 
        
        block_width = cols * btn_size + (cols - 1) * gap
        if MAX_LEVELS < cols: 
             block_width = MAX_LEVELS * btn_size + (MAX_LEVELS - 1) * gap
             
        block_height = total_rows * btn_size + (total_rows - 1) * gap

        start_x = (SCREEN_WIDTH - block_width) // 2 + (btn_size // 2)
        start_y = (SCREEN_HEIGHT - block_height) // 2 + (btn_size // 2)

        self.level_btns = []
        
        for i in range(1, MAX_LEVELS + 1):
            img = self.create_level_img(i, btn_size)
            
            idx = i - 1
            row = idx // cols
            col = idx % cols
            
            x_pos = start_x + col * (btn_size + gap)
            y_pos = start_y + row * (btn_size + gap)
            
            btn = Button(x_pos, y_pos, img, 1)
            
            self.level_btns.append({
                'btn': btn,
                'level': i,
                'locked': self.max_level < i
            })

    def create_level_img(self, number, size):
        surf = pygame.Surface((size, size))
        surf.fill((255, 255, 255))
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, size, size), 4)
        
        text_surf = self.game.font.render(str(number), True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(size//2, size//2))
        surf.blit(text_surf, text_rect)
        
        return surf

    def update(self, dt, actions):
        self.max_level = load_progress()
        for item in self.level_btns:
            item['locked'] = self.max_level < item['level']

        for item in self.level_btns:
            if not item['locked']:
                if item['btn'].draw(self.game.screen):
                    new_level = Level(self.game, item['level'])
                    new_level.enter_state()

    def draw(self, surface):
        surface.fill(D_GRAY) 
        
        title = self.game.font.render(f"SELECIONE O NIVEL", True, WHITE)
        title_y = self.level_btns[0]['btn'].rect.top - 60
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, title_y))

        for item in self.level_btns:
            if item['locked']:
                item['btn'].draw(surface) 
                overlay = pygame.Surface((item['btn'].rect.width, item['btn'].rect.height))
                overlay.set_alpha(180)
                overlay.fill((50, 50, 50)) 
                surface.blit(overlay, item['btn'].rect.topleft)
            else:
                item['btn'].draw(surface)


class Level(State):
    def __init__(self, game, level_index=1):
        super().__init__(game)
        self.level_index = level_index
        
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        button_gap = 80 
        
        self.restart_btn = Button(center_x, center_y - button_gap, self.game.assets['restart_btn'], 3)
        self.exit_btn = Button(center_x, center_y + button_gap, self.game.assets['exit_btn'], 1)

        # --- MUDANÇA 1: BOTÃO VOLTAR NO TOPO ---
        # Coloca o botão onde antes ficava a vida (10, 5 é uma margem segura)
        # Ajuste a escala (0.8) conforme o tamanho da sua imagem
        self.back_btn = Button(20, 25, self.game.assets['back_btn'], 0.6) 

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
            self.exit_state()
            return

        self.scroll = 0
        if level_data:
            self.level_width = len(level_data[0]) * TILE_SIZE
        else:
             self.level_width = SCREEN_WIDTH

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
        # Checa botão voltar
        if self.back_btn.draw(self.game.screen):
            self.exit_state()
            return

        if not self.player: return

        if not self.player.alive_:
            if self.restart_btn.draw(self.game.screen):
                self.game.state_stack.pop()
                new_level = Level(self.game, self.level_index)
                new_level.enter_state()
            
            if self.exit_btn.draw(self.game.screen):
                self.exit_state() 
            return

        # Lógica da Câmera
        if self.level_width < SCREEN_WIDTH:
            self.scroll = 0
        else:
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
            save_progress(self.level_index)
            self.level_index += 1
            if self.level_index <= MAX_LEVELS:
                self.game.state_stack.pop() 
                new_level = Level(self.game, self.level_index)
                new_level.enter_state()
            else:
                print("JOGO ZERADO!")
                self.exit_state() 

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
            # --- MUDANÇA 2: DESCER A HUD ---
            # O draw_ui já foi ajustado no soldier.py para desenhar a vida em Y=50
            self.player.draw_ui(surface, self.scroll) 
            
            # Ajustamos balas e granadas para ficarem ABAIXO da barra de vida
            # Vida está em Y=50 e tem altura aprox 20px -> Fim em Y=70
            
            # Munição (agora em Y=75)
            for i in range(self.player.ammo):
                x = 10 + i*11
                surface.blit(self.game.assets['bullet'], (x, 75))
            
            # Granadas (agora em Y=100)
            for i in range(self.player.grenade):
                x = 10 + i*15
                surface.blit(self.game.assets['grenade'], (x, 100))
        
        # O botão voltar é desenhado por último (interface)
        self.back_btn.draw(surface)

        if not self.player.alive_:
            self.restart_btn.draw(surface)
            self.exit_btn.draw(surface)

        for enemy in self.enemy_group:
            enemy.draw_ui(surface, self.scroll)

        if DEBUG:
            for group in [self.world.obstacle_group, self.world.water_group, self.player_group, self.enemy_group]:
                for sprite in group:
                    rect_copy = sprite.rect.copy()
                    rect_copy.x -= self.scroll
                    pygame.draw.rect(surface, (255, 255, 255), rect_copy, 1)