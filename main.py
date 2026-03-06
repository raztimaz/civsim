import pygame as pg
import random
from noise import pnoise2
from settings import *


def get_color_surface(color, alpha=255):
    surf = pg.Surface((CELL_SIZE, CELL_SIZE), pg.SRCALPHA)
    surf.fill((*color, alpha))
    return surf.convert_alpha()


class Tile:
    __slots__ = ('type', 'overlay')

    def __init__(self, t_type=TILE_PLAIN, overlay=OVERLAY_NONE):
        self.type = t_type
        self.overlay = overlay


class World:
    def __init__(self, w, h, seed=None):
        self.w, self.h = w, h
        self.seed = seed if seed is not None else random.randint(0, 999999)
        self.tiles = [[Tile(TILE_DEEP_WATER, OVERLAY_NONE) for _ in range(h)] for _ in range(w)]
        self.full_surf = pg.Surface((w * CELL_SIZE, h * CELL_SIZE))
        self.view_surf = None
        
        self.textures = [
            get_color_surface((10, 20, 80)),    # Deep Water
            get_color_surface((40, 100, 200)),  # Water
            get_color_surface((230, 210, 160)), # Sand
            get_color_surface((50, 140, 50)),   # Plain
            get_color_surface((110, 110, 110)), # Mountain
            get_color_surface((240, 240, 240))  # Snow
        ]
        
        self.overlays = [
            None, 
            get_color_surface((20, 70, 20), 160)  # Forest
        ]
        
        self.generate()
        self.render_all()

    def generate(self):
        off_x = self.seed % 10000
        off_y = (self.seed // 1000) % 10000

        for x in range(self.w):
            for y in range(self.h):
                val = pnoise2((x + off_x) / NOISE_SCALE, 
                              (y + off_y) / NOISE_SCALE, 
                              octaves=NOISE_OCTAVES)

                if val < THRESHOLD_DEEP_WATER:
                    self.tiles[x][y].type = TILE_DEEP_WATER
                elif val < THRESHOLD_WATER:
                    self.tiles[x][y].type = TILE_WATER
                elif val < THRESHOLD_SAND:
                    self.tiles[x][y].type = TILE_SAND
                elif val < THRESHOLD_PLAIN:
                    self.tiles[x][y].type = TILE_PLAIN
                    m_val = pnoise2((x + off_x + 777) / 25.0, 
                                    (y + off_y + 777) / 25.0)
                    if m_val > 0.22:
                        self.tiles[x][y].overlay = OVERLAY_FOREST
                elif val < THRESHOLD_MOUNTAIN:
                    self.tiles[x][y].type = TILE_MOUNTAIN
                else:
                    self.tiles[x][y].type = TILE_SNOW

    def render_all(self):
        for y in range(self.h):
            for x in range(self.w):
                t = self.tiles[x][y]
                pos = (x * CELL_SIZE, y * CELL_SIZE)
                self.full_surf.blit(self.textures[t.type], pos)
                if t.overlay > 0:
                    self.full_surf.blit(self.overlays[t.overlay], pos)

    def update_view(self, zoom):
        nw = int(self.w * CELL_SIZE * zoom)
        nh = int(self.h * CELL_SIZE * zoom)
        self.view_surf = pg.transform.smoothscale(self.full_surf, (nw, nh))


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pg.time.Clock()
    
    world = World(W_TILES, H_TILES)
    zoom = 0.3
    world.update_view(zoom)
    
    cam_x, cam_y = 0, 0
    dragging = False

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3: dragging = True
                elif event.button == 4:
                    zoom = min(zoom + ZOOM_STEP, MAX_ZOOM)
                    world.update_view(zoom)
                elif event.button == 5:
                    zoom = max(zoom - ZOOM_STEP, MIN_ZOOM)
                    world.update_view(zoom)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 3: dragging = False
            elif event.type == pg.MOUSEMOTION and dragging:
                dx, dy = event.rel
                cam_x += dx
                cam_y += dy

        vw, vh = world.view_surf.get_size()
        
        # Если карта больше экрана — ограничиваем движение, иначе — центрируем
        if vw > SCREEN_SIZE:
            cam_x = min(0, max(cam_x, SCREEN_SIZE - vw))
        else:
            cam_x = (SCREEN_SIZE - vw) // 2
            
        if vh > SCREEN_SIZE:
            cam_y = min(0, max(cam_y, SCREEN_SIZE - vh))
        else:
            cam_y = (SCREEN_SIZE - vh) // 2

        screen.fill((10, 10, 15)) # Глубокий темный фон
        screen.blit(world.view_surf, (cam_x, cam_y))
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()


if __name__ == "__main__":
    main()
