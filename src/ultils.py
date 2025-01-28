import ctypes

def get_screen_size():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)  # 0 é a largura da tela
    screen_height = user32.GetSystemMetrics(1)  # 1 é a altura da tela
    return screen_width, screen_height
