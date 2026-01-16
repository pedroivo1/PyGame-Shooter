import pygame
import csv
import os
import sys
import subprocess

# --- TENTATIVA DE IMPORTAR SETTINGS ---
try:
    from scripts.settings import *
    print("Configurações importadas de scripts.settings")
except ImportError:
    print("Settings não encontrado. Usando valores padrão.")
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TILE_SIZE = 32
    ROWS = 16
    MAX_COLS = 150

# --- CONFIGURAÇÕES DO EDITOR ---
SIDE_MARGIN = 300
LOWER_MARGIN = 100
EDITOR_WIDTH = SCREEN_WIDTH + SIDE_MARGIN
EDITOR_HEIGHT = SCREEN_HEIGHT + LOWER_MARGIN
FPS = 60
LEVEL_HEIGHT = ROWS * TILE_SIZE

# Cores
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
BG_COLOR = (30, 30, 30)
GRID_COLOR = (200, 200, 200)
PINK = (255, 50, 150)

# --- INICIALIZAÇÃO ---
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((EDITOR_WIDTH, EDITOR_HEIGHT))
pygame.display.set_caption('Level Editor - Robust Mode')

# --- VARIÁVEIS GLOBAIS ---
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
current_level_file = "" 
sidebar_scroll = 0 # NOVO: Controle de rolagem da barra lateral

font = pygame.font.SysFont('Futura', 24)

# --- ASSETS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TILES_DIR = os.path.join(BASE_DIR, 'data', 'images', 'tiles')
BG_DIR = os.path.join(BASE_DIR, 'data', 'images', 'background')

img_list = []

# --- FUNÇÃO DE ORDENAÇÃO SEGURA ---
def natural_sort_key(filename):
    """Ordena números como números e textos como textos, sem crashar."""
    name, _ = os.path.splitext(filename)
    if name.isdigit():
        return (0, int(name)) # Tipo 0: Números vêm primeiro
    return (1, name) # Tipo 1: Strings vêm depois

try:
    # Usa a nova chave de ordenação
    tile_files = sorted(os.listdir(TILES_DIR), key=natural_sort_key)
except FileNotFoundError:
    print(f"ERRO: Pasta {TILES_DIR} não encontrada.")
    tile_files = []

print("--- Carregando Tiles ---")
for filename in tile_files:
    if filename.endswith(".png"):
        try:
            img = pygame.image.load(os.path.join(TILES_DIR, filename)).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            img_list.append(img)
            print(f"OK: {filename}")
        except Exception as e:
            print(f"ERRO ao carregar {filename}: {e}")
print(f"Total carregado: {len(img_list)} tiles.")
print("------------------------")

bg_img = None
try:
    if os.path.exists(BG_DIR):
        bg_files = [f for f in os.listdir(BG_DIR) if f.endswith('.png')]
        if bg_files:
            bg_img = pygame.image.load(os.path.join(BG_DIR, bg_files[0])).convert_alpha()
            bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    pass

# --- CLASSE BOTÃO (Atualizada para Scroll) ---
class Button():
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        # rect guarda a posição "absoluta" dentro da lista (sem considerar o scroll visual)
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface, scroll_y=0):
        action = False
        pos = pygame.mouse.get_pos()
        
        # Ajustamos a posição visual Y subtraindo o scroll
        draw_y = self.rect.y - scroll_y
        draw_rect = pygame.Rect(self.rect.x, draw_y, self.rect.width, self.rect.height)

        # Checa colisão considerando o scroll visual
        # Só ativa se estiver visível na tela (dentro da altura do editor)
        if 0 < draw_y < EDITOR_HEIGHT:
            if draw_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    action = True
                    self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
            surface.blit(self.image, (self.rect.x, draw_y))
            return action, draw_rect # Retorna o rect desenhado para fazer o outline
            
        return False, None

# --- DADOS ---
world_data = []
def reset_level():
    global world_data
    world_data = []
    for row in range(ROWS):
        r = [-1] * MAX_COLS
        world_data.append(r)
    for tile in range(0, MAX_COLS):
        world_data[ROWS - 1][tile] = 0

reset_level()

# --- ANTI-CRASH LINUX ---
def run_dialog_script(script_type):
    global screen
    pygame.display.quit()
    if script_type == 'open':
        py_code = """import tkinter as tk; from tkinter import filedialog; root = tk.Tk(); root.withdraw(); print(filedialog.askopenfilename(title="Abrir Nível", filetypes=[("CSV", "*.csv")]));"""
    else:
        py_code = """import tkinter as tk; from tkinter import filedialog; root = tk.Tk(); root.withdraw(); print(filedialog.asksaveasfilename(title="Salvar Nível", defaultextension=".csv", filetypes=[("CSV", "*.csv")]));"""
    
    path = None
    try:
        result = subprocess.run([sys.executable, "-c", py_code], capture_output=True, text=True)
        path = result.stdout.strip()
    except Exception as e:
        print(f"Erro no subprocesso: {e}")

    pygame.display.init()
    screen = pygame.display.set_mode((EDITOR_WIDTH, EDITOR_HEIGHT))
    pygame.display.set_caption('Level Editor - Robust Mode')
    
    if path and path != "": return path
    return None

def open_file_dialog(): return run_dialog_script('open')
def save_file_dialog(): return run_dialog_script('save')

# --- CARREGAMENTO DE NÍVEL ---
def load_level_data(path):
    global world_data, scroll
    if not os.path.exists(path): return False
    try:
        new_data = []
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                new_data.append([int(tile) for tile in row])
        
        # Blindagem de Tamanho
        current_rows = len(new_data)
        if current_rows < ROWS:
            for _ in range(ROWS - current_rows):
                new_data.append([-1] * MAX_COLS)
        
        for r in range(len(new_data)):
            if len(new_data[r]) < MAX_COLS:
                new_data[r].extend([-1] * (MAX_COLS - len(new_data[r])))
        
        world_data = new_data
        scroll = 0
        return True
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
    return False

# --- UI SETUP ---
def create_text_button_img(text, w, h, color):
    surf = pygame.Surface((w, h))
    surf.fill(color)
    txt_surf = font.render(text, True, (0,0,0))
    text_rect = txt_surf.get_rect(center=(w//2, h//2))
    surf.blit(txt_surf, text_rect)
    return surf

save_img = create_text_button_img("SAVE", 100, 40, GREEN)
load_img = create_text_button_img("LOAD", 100, 40, (100, 100, 255))
save_as_img = create_text_button_img("SAVE AS", 100, 40, (200, 200, 50))
eraser_img = create_text_button_img("DEL", TILE_SIZE, TILE_SIZE, PINK)

# Botões Fixos (Não rolam)
save_button = Button(SCREEN_WIDTH // 2 - 160, EDITOR_HEIGHT - 80, save_img, 1)
save_as_button = Button(SCREEN_WIDTH // 2 - 50, EDITOR_HEIGHT - 80, save_as_img, 1)
load_button = Button(SCREEN_WIDTH // 2 + 60, EDITOR_HEIGHT - 80, load_img, 1)

# Botões que Rolam (Tiles)
eraser_button = Button(SCREEN_WIDTH + 50, 50, eraser_img, 1)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    # Começa depois do botão da borracha
    tile_button = Button(SCREEN_WIDTH + (50 * (button_col + 1)) + 50, 50 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = -1 # Volta para o inicio e deixa espaço para a borracha/layout

# --- DESENHO ---
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BG_COLOR)
    if bg_img:
        for x in range(5):
            screen.blit(bg_img, ((x * SCREEN_WIDTH) - scroll * 0.5, 0))

def draw_grid():
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, GRID_COLOR, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, LEVEL_HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, GRID_COLOR, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0 and tile < len(img_list):
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# --- MAIN LOOP ---
run = True
while run:
    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    # Sidebar Fundo
    pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH, 0, SIDE_MARGIN, EDITOR_HEIGHT))
    
    # --- ÁREA ROLÁVEL ---
    # Botão Borracha (também rola)
    eraser_clicked, eraser_rect = eraser_button.draw(screen, sidebar_scroll)
    if eraser_clicked: current_tile = -1
    
    # Botões Tiles
    for i, btn in enumerate(button_list):
        clicked, rect = btn.draw(screen, sidebar_scroll)
        if clicked:
            current_tile = i
        
        # Destaque do Tile Selecionado (precisa acompanhar o scroll)
        if i == current_tile and rect:
             pygame.draw.rect(screen, GREEN, rect, 3)

    # Destaque Borracha
    if current_tile == -1 and eraser_rect:
        pygame.draw.rect(screen, RED, eraser_rect, 3)

    # --- ÁREA FIXA (UI Inferior) ---
    # Desenha um fundo preto embaixo para os botões de Save/Load não ficarem transparentes
    pygame.draw.rect(screen, BG_COLOR, (0, EDITOR_HEIGHT - 100, EDITOR_WIDTH, 100))
    
    filename = os.path.basename(current_level_file) if current_level_file else "Novo Arquivo"
    status_tile = "BORRACHA" if current_tile == -1 else f"Tile ID: {current_tile}"
    
    draw_text(f'Arquivo: {filename}', font, WHITE, 10, EDITOR_HEIGHT - 95)
    draw_text(f'Ferramenta: {status_tile}', font, WHITE, 10, EDITOR_HEIGHT - 65)
    
    if save_button.draw(screen)[0]:
        path = current_level_file if current_level_file else save_file_dialog()
        if path:
            current_level_file = path
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for row in world_data:
                    writer.writerow(row)

    if save_as_button.draw(screen)[0]:
        path = save_file_dialog()
        if path:
            current_level_file = path
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for row in world_data:
                    writer.writerow(row)

    if load_button.draw(screen)[0]:
        path = open_file_dialog()
        if path:
            current_level_file = path
            load_level_data(path)

    # --- INPUTS ---
    if scroll_left and scroll > 0: scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH: scroll += 5 * scroll_speed

    pos = pygame.mouse.get_pos()
    
    # MOUSE NO GRID (Ignora se mouse estiver na sidebar)
    if pos[0] < SCREEN_WIDTH and pos[1] < LEVEL_HEIGHT:
        grid_x = (pos[0] + scroll) // TILE_SIZE
        grid_y = pos[1] // TILE_SIZE

        if 0 <= grid_y < len(world_data) and 0 <= grid_x < len(world_data[0]):
            if pygame.mouse.get_pressed()[0] == 1:
                if world_data[grid_y][grid_x] != current_tile:
                    world_data[grid_y][grid_x] = current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                world_data[grid_y][grid_x] = -1
            if pygame.mouse.get_pressed()[1] == 1:
                got = world_data[grid_y][grid_x]
                if got != -1: current_tile = got

            # Preview
            if current_tile == -1:
                s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                s.fill(PINK); s.set_alpha(100)
                screen.blit(s, (grid_x * TILE_SIZE - scroll, grid_y * TILE_SIZE))
            elif current_tile < len(img_list):
                ghost = img_list[current_tile].copy()
                ghost.set_alpha(100)
                screen.blit(ghost, (grid_x * TILE_SIZE - scroll, grid_y * TILE_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        
        # --- ROLAGEM DO MOUSE NA SIDEBAR ---
        if event.type == pygame.MOUSEWHEEL:
            # Só rola se o mouse estiver na área da direita (Sidebar)
            mouse_x, _ = pygame.mouse.get_pos()
            if mouse_x > SCREEN_WIDTH:
                sidebar_scroll -= event.y * 20 # Velocidade do scroll
                # Limites do scroll
                if sidebar_scroll < 0: sidebar_scroll = 0
                # Limite inferior aproximado (altura total dos botões)
                max_scroll = (len(button_list) // 3 + 2) * 50
                if sidebar_scroll > max_scroll: sidebar_scroll = max_scroll

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a: scroll_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: scroll_right = True
            if event.key == pygame.K_LSHIFT: scroll_speed = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a: scroll_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: scroll_right = False
            if event.key == pygame.K_LSHIFT: scroll_speed = 1

    pygame.display.update()

pygame.quit()