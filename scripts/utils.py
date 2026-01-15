import pygame
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define o diretório raiz usando Pathlib
ROOT_DIR = Path(__file__).parent.parent
BASE_IMG_PATH = ROOT_DIR / 'data' / 'images'
BASE_SND_PATH = ROOT_DIR / 'data' / 'audios'

def load_image(path: str | Path, scale: float = 1.0) -> pygame.Surface:
    full_path = BASE_IMG_PATH / path
    try:
        img = pygame.image.load(full_path).convert_alpha()
        if scale != 1.0:
            new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
            img = pygame.transform.scale(img, new_size)
        return img
    except FileNotFoundError:
        logger.error(f"File not found: {full_path}")
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))
        return surf

def load_images(path: str, scale: float = 1.0) -> list[pygame.Surface]:
    folder_path = BASE_IMG_PATH / path
    if not folder_path.exists():
        logger.error(f"Folder not found: {folder_path}")
        return []

    images = []
    # Usa Pathlib para listar os arquivos .png
    files = list(folder_path.glob('*.png'))
    
    # Ordenação Híbrida (Numérica se possível, Alfabética se falhar)
    try:
        files.sort(key=lambda x: int(x.stem)) # x.stem é propriedade do Pathlib (nome sem extensão)
    except ValueError:
        files.sort()

    for file_path in files:
        rel_path = file_path.relative_to(BASE_IMG_PATH)
        images.append(load_image(rel_path, scale))
        
    return images

def load_sound(path: str, volume: float = 1.0) -> pygame.mixer.Sound | None:
    full_path = BASE_SND_PATH / path
    try:
        sound = pygame.mixer.Sound(full_path)
        sound.set_volume(volume)
        return sound
    except FileNotFoundError:
        logger.error(f"Audio file not found: {full_path}")
        return None

class AnimationManager:
    def __init__(self, animations: dict, frame_duration: float = 0.12, action='idle'):
        self.animations = animations 
        self.frame_duration = frame_duration 
        self.action = action
        self.frame = 0
        self.timer = 0.0

    def update(self, dt: float, loop: bool = True) -> bool:
        finished = False
        self.timer += dt

        if self.timer >= self.frame_duration:
            self.timer %= self.frame_duration
            next_frame = self.frame + 1
            
            if next_frame >= len(self.animations[self.action]):
                if loop:
                    self.frame = 0
                else:
                    self.frame = len(self.animations[self.action]) - 1
                    finished = True
            else:
                self.frame = next_frame

        return finished

    def set_action(self, action: str):
        if action != self.action:
            self.action = action
            self.frame = 0
            self.timer = 0

    def get_image(self) -> pygame.Surface:
        return self.animations[self.action][self.frame]

def draw_text(text, font, color, x, y, surface):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

class Button():
    def __init__(self, x, y, image, scale=1.0):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

# --- SISTEMA DE SAVE/LOAD COM PATHLIB ---
SAVE_FILE = ROOT_DIR / 'save.json'

def load_progress():
    # Verifica se existe usando .exists() do Pathlib
    if not SAVE_FILE.exists():
        data = {'max_level': 1}
        try:
            # Abre o arquivo usando .open() do Pathlib
            with SAVE_FILE.open('w') as f:
                json.dump(data, f)
            return 1
        except Exception as e:
            logger.error(f"Erro ao criar save: {e}")
            return 1
    
    try:
        with SAVE_FILE.open('r') as f:
            data = json.load(f)
            return data.get('max_level', 1)
    except Exception as e:
        logger.error(f"Erro ao ler save: {e}")
        return 1

def save_progress(level_completed):
    current_max = load_progress()
    next_level = level_completed + 1
    
    if next_level > current_max:
        data = {'max_level': next_level}
        try:
            with SAVE_FILE.open('w') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Erro ao salvar progresso: {e}")