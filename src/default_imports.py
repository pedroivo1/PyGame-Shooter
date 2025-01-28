from src import ultils

width, height = ultils.get_screen_size()

config_data = {
    'screen': {
        'width': int(width*0.9),
        'height': int(height*0.9),
        'fps': 60,
        'scale': 2,
        'title': 'Shooter'
    },
    'physic': {
        'gravity': 0.75
    }
}
