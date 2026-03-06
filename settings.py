# Основные параметры экрана
SCREEN_SIZE = 800
FPS = 60

# Размеры мира (200x200 = 40 000 тайлов)
W_TILES = 200
H_TILES = 200
CELL_SIZE = 16

# Камера
MIN_ZOOM = 0.2  # Еще сильнее отдалили, чтобы видеть гигантский мир
MAX_ZOOM = 2.0
ZOOM_STEP = 0.1

# Шум Перлина (Сделали еще плавнее)
NOISE_SCALE = 100.0  
NOISE_OCTAVES = 4   
NOISE_PERSISTENCE = 0.5
NOISE_LACUNARITY = 2.0

# Пороги биомов (Подняли воду на ~10%, чтобы ее стало больше)
THRESHOLD_DEEP_WATER = -0.35
THRESHOLD_WATER = -0.15 # Было -0.2
THRESHOLD_SAND = -0.05  # Было -0.1
THRESHOLD_PLAIN = 0.5
THRESHOLD_MOUNTAIN = 0.8

# ID Тайлов и Оверлеев
TILE_DEEP_WATER = 0
TILE_WATER = 1
TILE_SAND = 2
TILE_PLAIN = 3
TILE_MOUNTAIN = 4
TILE_SNOW = 5
OVERLAY_NONE = 0
OVERLAY_FOREST = 1
